#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对当前正在进行入口到外形检测的任务确认成功或失败
后期待优化：通过读取配置的入库口与可入巷道的对应关系，在数据库查询对应入库口入库时对应巷道是否有可用库位，若没有可用库位，外形检测通过后，wms请求上架的任务会失败，中间件下发异常回退任务。
"""

import ast
import unittest
from common.configHttp import RunMain
import paramunittest
from testFile import geturlParams
# import urllib.parse
from testFile import readExcel
from testFile.readyaml import readyaml
from common.configDb import MSSQL as ms, Mongo as mg
from copy import copy
import math
import json
import time


url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'cfm_profileCheck')


# t = readyaml().readyaml('profileCheckTasklist.yaml')  # 读取从test_5_to_profileCheckStatio获取到的需要下发入口到外形检测的任务数据
# # 在mongodb的TaskBase集合中查找所有的TaskType为’入口到外形检测‘的任务个数
# docnum = mg().MongoExecquery('GSMiddleWare', 'TaskBase').find({'TaskType': '入口到外形检测'}).count()
# while docnum < t['tasklength']:  # 如果在mongodb中查询到任务数小于test_5_to_profileCheckStatio.py实际下发的任务数，那么继续查询
#     docnum = mg().MongoExecquery('GSMiddleWare', 'TaskBase').find({'TaskType': '入口到外形检测'}).count()
#     doc1 = mg().MongoExecquery('GSMiddleWare', 'TaskBase').find({'TaskType': '入口到外形检测'})

"""***********从ShipConfig.yaml获取入口到外形检测的检测点、异常口配置信息列表************"""
profileCheckShipConfig = readyaml().readyaml('ShipConfig.yaml')['request']['入口到外形检测']
shiplist = []
profileChecklist = []
CheckStationReturnlist = []
for p in range(len(profileCheckShipConfig)):
    ship = profileCheckShipConfig[p]['ship']
    profileCheckStation = profileCheckShipConfig[p]['profileCheckStation']
    profileCheckStationReturn = profileCheckShipConfig[p]['profileCheckStationReturn']
    shiplist.append(ship)
    profileChecklist.append(profileCheckStation)
    CheckStationReturnlist.append(profileCheckStationReturn)


@paramunittest.parametrized(*casexls)
class testcfm_profileCheckStation(unittest.TestCase):
    def setParameters(self, case_name, method, path, query):
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = ast.literal_eval(str(query))
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()
        self.querylist1 = []
        self.querylist2 = []

        def isNone(value):
            """
            判断某个值是否为None，如果为None，返回空字符，如果不为None，返回本身
            :param value:
            :return:
            """
            if value is None:
                return ''
            else:
                return value

        """**************获取需要作为确认‘入口到外形检测’任务接口的参数列表********************"""
        # 读取从test_5_to_profileCheckStatio获取到的需要下发入口到外形检测的任务数据
        self.profileCheckTasklist = readyaml().readyaml('profileCheckTasklist.yaml')
        self.TaskCodelist = []  # 从mongodb查询结果中获取'入口到外形检测'任务的code列表
        self.Fromlist = []  # 从mongodb查询结果中获取'入口到外形检测'任务的入库口列表
        self.Tolist = []  # 从mongodb查询结果中获取'入口到外形检测'任务的外形检测点列表
        self.Palletslist = []  # 从mongodb查询结果中获取'入口到外形检测'任务的托盘列表
        self.confirmresultlist = []  # 外形检测结果列表
        for Taskdoc in self.profileCheckTasklist:  # 根据在mongodb中查询到的正在执行的’入口到外形检测‘的任务循环
            self.TaskCodelist.append(str(Taskdoc["TaskCode"]))
            self.Fromlist.append(str(Taskdoc["FromLocationCode"]))
            self.Tolist.append(str(Taskdoc["ToLocationCode"]))
            self.Palletslist.append(Taskdoc["Pallets"])

        """ self.confirmresultlist.append("成功")
        if len(self.confirmresultlist) == 1:  # confirmresultlist只有一个元素即mongodb只有一个入口到外形检测正在执行的任务时，外形检测确认为’成功‘
            self.confirmresultlist[0] = '成功'
        elif len(self.confirmresultlist) > 1:
            for i in range(len(self.confirmresultlist)):  # confirmresultlist列表大于一个元素时，一半给成功，一般给失败
                if i < len(self.confirmresultlist)/2:
                    self.confirmresultlist[i] = '成功'
                else:
                    self.confirmresultlist[i] = '失败'  """

        """*******将获取到参数列表分别加入到请求体中，一半作为外形检测成功参数，一半作为外形检测失败参数，获取两个请求体列表********"""
        if len(self.TaskCodelist) == 1:
            self.query['taskCode'] = str(self.TaskCodelist[0])
            self.query['from'] = str(self.Fromlist[0])
            self.query['to'] = str(self.Tolist[0])
            self.query['containerCodes'] = [str(self.Palletslist[0])]
            self.query['additionalInfo']['外形检测'] = "成功"
            newquery = str(copy(self.query)).encode('utf-8')
            self.querylist1.append(newquery)
        elif len(self.TaskCodelist) > 1:  # 正在执行的入口到外形检测任务大于1个时，取一半数据作为外形检测成功参数，一半作为失败参数
            for m in range(len(self.TaskCodelist)-1):  # 除最后一条的入口到外形检测任务全部作为外形检测成功的测试数据
                # range(math.ceil(len(self.TaskCodelist) / 2)):  取一半入口到外形检测任务作为外形检测成功的测试数据
                self.query['taskCode'] = str(self.TaskCodelist[m])
                self.query['from'] = str(self.Fromlist[m])
                self.query['to'] = str(self.Tolist[m])
                self.query['containerCodes'] = [str(self.Palletslist[m])]
                self.query['additionalInfo']['外形检测'] = '成功'
                newquery = str(copy(self.query))  # .encode('utf-8')
                self.querylist1.append(newquery)
            for n in (-1,):  # 只取最后一个入口到外形检测任务作为外形检测失败的测试数据
                # range(math.ceil(len(self.TaskCodelist) / 2), len(self.TaskCodelist)):  取一半入口到外形检测任务作为外形检测失败的测试数据
                self.query['taskCode'] = str(self.TaskCodelist[n])
                self.query['from'] = str(self.Fromlist[n])
                self.query['to'] = str(self.Tolist[n])
                self.query['containerCodes'] = [str(self.Palletslist[n])]
                self.query['additionalInfo']['外形检测'] = '失败'
                newquery = str(copy(self.query))  # .encode('utf-8')
                self.querylist2.append(newquery)
            print('入口到外形检测移动任务确定‘成功’的请求体列表为：', self.querylist1)
            print('入口到外形检测移动任务确定‘失败’的请求体列表为：', self.querylist2)

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testcfm_profileCheckStation(self):
        self.checkResult()

    def tearDown(self):
        print('测试结束，输出log完结\n\n')
        ms().closeDB()  # 关闭数据库连接

    def checkResult(self):
        new_url = url + ':9877' + self.path

        if self.case_name == 'cfmyes_profileCheck':
            for j in range(len(self.querylist1)):  # 根据querylist1长度决定请求几次
                print('入口到外形检测确认成功的请求体：', self.querylist1[j])
                try:
                    info = RunMain().run_main(self.method, headers=self.headers, url=new_url, data=json.dumps(eval(self.querylist1[j])))
                    print("入口到外形检测任务，确认检测'成功'，返回：", info)
                except Exception as e:
                    print('接口调用异常：', e)
                else:
                    print('调用入口到外形检测确认成功接口后，等待3秒上架任务数据插入mongodb时间')
                    time.sleep(3)
                    # 在mongodb的MiddlewareTask集合中查找该托盘是否有任务类型为’MV_PUTAWAY‘、出发货位为该外形检测点的正在执行的上架任务
                    doc2 = mg().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({"$and": [
                        {'Pallet': self.Palletslist[j]}, {'TaskType': 'MV_PUTAWAY'}, {'FromLocCode': self.Tolist[j]}]})
                    self.assertTrue(mg().ResultisNotNone(doc2), '入口到外形检测确认成功后，在mongodb中没有托盘%s的上架任务' % self.Palletslist[j])

        elif self.case_name == 'cfmno_profileCheck':
            for k in range(len(self.querylist2)):  # 根据querylist2长度决定请求几次
                print('入口到外形检测确认失败的请求体：', self.querylist2[k])
                try:
                    info = RunMain().run_main(self.method, headers=self.headers, url=new_url, data=json.dumps(eval(self.querylist2[k])))
                    print('入口到外形检测任务，确认检测失败，返回：', info)
                except Exception as e:
                    print('接口调用异常：', e)
                else:
                    # 在mongodb的TaskBase集合中查找该托盘是否有任务类型为’外形检测异常回退‘的、目标货位为shipconfig.yaml文件中配置的对应回退位置的正在执行的任务
                    # doc2 = mg().MongoExecquery('GSMiddleWare', 'TaskBase').find({"$and": [
                    #     {'Pallets': self.Palletslist[k + math.ceil(len(self.Palletslist) / 2)]},
                    #     {'TaskType': '外形检测异常回退'},
                    #     {'ToLocationCode': CheckStationReturnlist[
                    #         profileChecklist.index(self.Tolist[k + math.ceil(len(self.Tolist) / 2)])]}]})
                    doc2 = mg().MongoExecquery('GSMiddleWare', 'TaskBase').find({"$and": [
                         {'Pallets': self.Palletslist[-1]}, {'TaskType': '外形检测异常回退'},
                         {'ToLocationCode': CheckStationReturnlist[
                             profileChecklist.index(self.Tolist[-1])]}]})  # 将入口到外形检测任务的最后一条数据作为外形检测失败测试数据时，用此doc
                    self.assertTrue(mg().ResultisNotNone(doc2), '入口到外形检测确认失败后，mongodb没有’外形检测异常回退‘任务')


if __name__ == '__main__':
    unittest.main(verbosity=2)
