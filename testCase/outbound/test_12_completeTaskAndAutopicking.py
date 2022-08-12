#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
出库任务完成确认：
从mongodb查询当前正在执行的移库、出库、入库任务--->
    判断-如果没有查询到任何数据--->抛出ValueError
    判断-如果有查询到数据--->While循环（正在执行的任务数大于0时）
        分别获取移库、入库、及出库任务数据列表
        依次确认移库任务，若确认失败，跳出循环，若确认成功，【断言】库存中移库任务的目标库位中是否有该托盘物料，有则断言成功
        依次确认入库任务，若确认失败，跳出循环，若确认成功，【断言】库存中入库任务的目标库位中是否有该托盘物料，有则断言成功
        依次确认出库任务，若确认失败，跳出循环，若确认成功，【断言】库存中出库任务的起始货位中是否有该托盘物料，没有则断言成功
        重新在mongodb查询当前正在执行的移库、出库、入库任务，用于While循环判断，若有，继续循环
    循环结束后，判断-mongodb当前是否还有未确认的移库、出库、入库任务，包括打开的及正在执行的，若有，【断言】失败，有任务未被确认
"""

import ast
import unittest
from common.configHttp import RunMain
import paramunittest
from testFile import geturlParams
# import urllib.parse
from testFile import readExcel
from testFile.readyaml import readyaml
from common.configDb import MSSQL as ms, Mongo as mg, Rds as rd
from testFile.readSql import get_sql
import json
import time


url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'completeTaskAndAutopicking')


@paramunittest.parametrized(*casexls)
class testcompleteTaskAndAutopicking(unittest.TestCase):
    def setParameters(self, case_name, method, path, query):
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = ast.literal_eval(query)
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()
        self.taskdata=[]

    # def get_workingtask(self, doc):
    #     d1 = []
    #     for docelement in self.doc1:
    #         d1.append(docelement)
    #     return d1

        # # 数据库获取当前已生效及分配库存的发货单
        # cur1 = ms().get_all(ms().ExecQuery("SELECT id, XCode FROM WMS.ShipOrder "
        #                                    "WHERE XStatus='WORKING' AND AlloactedPkgQuantity>0 "
        #                                    "ORDER BY CreationTime DESC"))

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testcompleteTaskAndAutopicking(self):
        self.checkResult()

    def tearDown(self):
        print('测试结束，输出log完结\n\n')
        ms().closeDB()  # 关闭数据库连接

    def checkResult(self):
        new_url = url + ':9877' + self.path
        if self.case_name == 'completeTaskAndPicking':
            # if self.case_name == 'completeTaskAndPicking':
            # 获取从mongodb的GSMiddleWare库的MiddlewareTask集合中来源的正在执行的所有出库、入库、移库任务
            doc1 = mg().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({
                "$and": [{'TaskStatus': 'WORKING'}, {
                    'TaskType': {'$in': ['MV_PICKTICKET_PICKING', 'MV_PUTAWAY', 'MV_MOVE']}}]})

            # 根据从MiddlewareTask集合中查询到的TaskCode获取更详细任务信息用以给接口传参
            for a in mg().get_mongodata(doc1):
                doc2 = mg().MongoExecquery('GSMiddleWare', 'TaskBase').find({'TaskCode': a['TaskCode']})
                self.taskdata.append(mg().get_mongodata(doc2))
            print('当前正在在执行状态的出入库、移库任务信息：', self.taskdata)
            if len(self.taskdata) == 0:
                raise ValueError('未查询到正在执行的出库、入库或移库任务，请确认当前是否有需要确认出/入/移库的任务！')
            else:
                while len(self.taskdata) > 0:  # 只要还有working状态的出库、移库任务，就持续循环
                    taskCodelist1 = []
                    taskTypelist1 = []
                    fromlist1 = []
                    tolist1 = []
                    TPlist1 = []
                    taskCodelist2 = []
                    taskTypelist2 = []
                    fromlist2 = []
                    tolist2 = []
                    TPlist2 = []
                    taskCodelist3 = []
                    taskTypelist3 = []
                    fromlist3 = []
                    tolist3 = []
                    TPlist3 = []
                    info = '0'
                    for l in self.taskdata:  # 获取参数列表
                        if l[0]['TaskType'] == 'MV_MOVE':  # 获取移动任务参数列表用以更新请求体
                            taskCodelist1.append(l[0]['TaskCode'])
                            taskTypelist1.append(l[0]['TaskType'])
                            fromlist1.append(l[0]['FromLocationCode'])
                            tolist1.append(l[0]['ToLocationCode'])
                            TPlist1.append(l[0]['Pallets'])
                        elif l[0]['TaskType'] == 'MV_PICKTICKET_PICKING':  # 获取出库任务参数列表用以更新请求体
                            taskCodelist2.append(l[0]['TaskCode'])
                            taskTypelist2.append(l[0]['TaskType'])
                            fromlist2.append(l[0]['FromLocationCode'])
                            tolist2.append(l[0]['ToLocationCode'])
                            TPlist2.append(l[0]['Pallets'])
                        elif l[0]['TaskType'] == 'MV_PUTAWAY':  # 获取入库任务参数列表用以更新请求体
                            taskCodelist3.append(l[0]['TaskCode'])
                            taskTypelist3.append(l[0]['TaskType'])
                            fromlist3.append(l[0]['FromLocationCode'])
                            tolist3.append(l[0]['ToLocationCode'])
                            TPlist3.append(l[0]['Pallets'])
                    print('移库任务编号列表：', taskCodelist1)
                    print('出库任务编号列表：', taskCodelist2)
                    print('入库任务编号列表：', taskCodelist3)
                    # if self.case_name =='completeTask_Move':
                    for i in range(len(taskCodelist1)):  # 用参数列表数据更新请求体
                        self.query['taskCode'] = taskCodelist1[i]
                        self.query['taskType'] = taskTypelist1[i]
                        self.query['from'] = fromlist1[i]
                        self.query['to'] = tolist1[i]
                        self.query['containerCodes'][0] = TPlist1[i]
                        print('确认移库任务的接口请求体为：', self.query)
                        try:  # 调用移库任务确认完成接口
                            info = RunMain().run_main(self.method, headers=self.headers, url=new_url,
                                                      data=json.dumps(self.query))
                        except Exception as e:
                            print('接口调用异常：', e)
                            info = None
                            break  # 如果接口调用异常，则退出for循环
                        else:
                            print('移库任务完成，返回:', info)
                            # 查询数据库库存，目标库位的托盘是否为本次移库的托盘，以检验是否移库成功
                            sqltext1 = """SELECT a.Pallet  FROM WMS.InventoryDetail a
    INNER JOIN WMS.Location b ON a.LocationId=b.Id AND b.LocType='STORAGE'
    WHERE a.Pallet='{0}' AND a.LocationCode='{1}' AND a.PackageQuantity>0 """.format(TPlist1[i], tolist1[i])
                            cur1 = ms().get_all(ms().ExecQuery(sqltext1))
                            self.assertEqual(cur1[0][0], TPlist1[i], '数据库没有查到移库后的库存信息，确认移库任务后，库存没有更新！')

                    #elif self.case_name == 'completeTask_Putway':
                    for i in range(len(taskCodelist3)):  # 用参数列表数据更新请求体
                        self.query['taskCode'] = taskCodelist3[i]
                        self.query['taskType'] = taskTypelist3[i]
                        self.query['from'] = fromlist3[i]
                        self.query['to'] = tolist3[i]
                        self.query['containerCodes'][0] = TPlist3[i]
                        print('确认入库任务的接口请求体为：', self.query)
                        try:  # 调用入库任务确认完成接口
                            info = RunMain().run_main(self.method, headers=self.headers, url=new_url,
                                                      data=json.dumps(self.query))
                        except Exception as e:
                            print('接口调用异常：', e)
                            info = None
                            break  # 如果接口调用异常，则退出for循环
                        else:
                            print('入库任务完成，返回:', info)
                            # 查询数据库库存，目标库位的托盘是否为本次入库的托盘，以检验是否入库成功
                            sqltext2 = """SELECT a.Pallet  FROM WMS.InventoryDetail a
                INNER JOIN WMS.Location b ON a.LocationId=b.Id AND b.LocType='STORAGE'
                WHERE a.Pallet='{0}' AND a.LocationCode='{1}' AND a.PackageQuantity>0 """.format(TPlist3[i], tolist3[i])
                            cur1 = ms().get_all(ms().ExecQuery(sqltext2))
                            self.assertEqual(cur1[0][0], TPlist3[i], '数据库没有查到入库后的库存信息，确认入库任务后，库存没有更新！')

                    # elif self.case_name == 'completeTaskAndPicking':
                    for i in range(len(taskCodelist2)):  # 用参数列表数据更新请求体
                        self.query['taskCode'] = taskCodelist2[i]
                        self.query['taskType'] = taskTypelist2[i]
                        self.query['from'] = fromlist2[i]
                        self.query['to'] = tolist2[i]
                        self.query['containerCodes'][0] = TPlist2[i]
                        print('确认出库任务的接口请求体为：', self.query)
                        try:  # 调用出库任务确认完成接口
                            info = RunMain().run_main(self.method, headers=self.headers, url=new_url,
                                                      data=json.dumps(self.query))
                        except Exception as e:
                            print('接口调用异常：', e)
                            info = None
                            break  # 如果接口调用异常，则退出for循环
                        else:
                            print('出库任务完成，返回:', info)
                            # 查询数据库库存，移出库位的托盘是否为本次出库的托盘，以检验是否出库成功
                            sqltext3 = """SELECT a.Pallet  FROM WMS.InventoryDetail a
                INNER JOIN WMS.Location b ON a.LocationId=b.Id AND b.LocType='STORAGE'
                WHERE a.Pallet='{0}' AND a.LocationCode='{1}' AND a.PackageQuantity>0 """.format(TPlist2[i], fromlist2[i])
                            cur1 = ms().get_all(ms().ExecQuery(sqltext3))
                            self.assertNotEqual(cur1[0][0], TPlist2[i], '数据库在库存中查到了应该已经出库的托盘信息！')

                            # 清除该出库口的占位，特殊项目需要，标准版可注销掉
                            rd().GetRedisConnect().hdel('GSMiddleWare:lockStation', tolist2[i])
                    if info is None:  # 如果接口调用异常，则退出while循环
                        break
                    else:
                        print('每次while循环等待10秒钟，给下一轮任务下发到WCS的时间')
                        time.sleep(10)

                    print('************************重新获取taskdata出入库、移库任务数据***********************')
                    self.taskdata = []
                    # 获取从mongodb的GSMiddleWare库的MiddlewareTask集合中来源的正在执行的所有出库、入库、移库任务
                    doc1 = mg().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({
                        "$and": [{'TaskStatus': 'WORKING'}, {
                            'TaskType': {'$in': ['MV_PICKTICKET_PICKING', 'MV_PUTAWAY', 'MV_MOVE']}}]})
                    # 根据从MiddlewareTask集合中查询到的TaskCode获取更详细任务信息用以给接口传参
                    for a in mg().get_mongodata(doc1):
                        doc2 = mg().MongoExecquery('GSMiddleWare', 'TaskBase').find({'TaskCode': a['TaskCode']})
                        self.taskdata.append(mg().get_mongodata(doc2))
                    print('重新获取当前正在在执行状态的出入库、移库任务信息：', self.taskdata)

                doc3 = mg().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({
                        'TaskType': {'$in': ['MV_PICKTICKET_PICKING', 'MV_PUTAWAY', 'MV_MOVE']}})
                self.assertFalse(mg().get_mongodata(doc3), '还有未确认完成的任务！')


if __name__ == '__main__':
    unittest.main()