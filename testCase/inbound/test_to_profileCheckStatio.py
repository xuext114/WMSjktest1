#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从入口到外形检测任务断言，包括五个场景：
profileCheckStation_locError：入库口错误时，请求去外形检测任务
to_profileCheckStation：正常外形检测任务下发（托盘：所有在地面库存receive中，
且不在任务中、不在架上库存中的托盘；入库口：ShipConfig.yaml中’入口到外形检测‘任务中ship包括的入口）
profileCheckStation_palletMoving：对当前已经在库存架上的托盘再次下发去外形检测任务
profileCheckStation_palletInventory：对当前已经在库存架上的托盘再次下发去外形检测任务
profileCheckStation_palletNoreceive：对当前还未进行收货的托盘下发去外形检测任务
"""

import ast
import unittest
from common.configHttp import RunMain
import paramunittest
from testFile import geturlParams, getpathInfo
# import urllib.parse
from testFile import readExcel
from testFile.readyaml import readyaml
from common.configDb import MSSQL as ms, Mongo as mg
from copy import copy
import random
import os
import yaml

path = getpathInfo.get_Path()
url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'to_profileCheckStation')


@paramunittest.parametrized(*casexls)
class testto_profileCheckStation(unittest.TestCase):

    def isNone(self, value):
        """
        判断某个值是否为None，如果为None，返回空字符，如果不为None，返回本身
        :param value:
        :return:
        """
        if value is None:
            return ''
        else:
            return value

    def setParameters(self, case_name, method, path, query):
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = ast.literal_eval(str(query))
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()
        del self.headers['Content-Length']  # get请求，hearders中需要删除此项

        # 从sql.xml获取语句查询获取收货完成，不在任务上架、移位、盘点、下架等任务中，在receive点库存中的托盘
        cur = ms().getvalue('WMS.ReceiptOrder', 'Pallet')

        # 获得不在移动任务也不在上下架、盘点等任务中的托盘列表Palletlist
        self.Palletlist = []
        self.MovingPalletlist = []
        for m in range(len(cur)):  # 根据初步查询到的托盘数进行循环
            # 根据获取到托盘到mongo中查询是否有该托盘正在移动中的任务，如入口到外形检测任务
            doc = mg().MongoExecquery('GSMiddleWare', 'TaskBase').find({'Pallets': str(cur[m][0])})
            if mg().ResultisNotNone(doc) is False:  # 如果查询结果为None，则将该托盘添加到Palletlist中
                self.Palletlist.append(str(cur[m][0]))  # 得到最终不在移动任务也不在上下架、盘点等任务中的托盘列表Palletlist
            else:
                # 如果查询结果不为None，表示该托盘正在进行移位任务，如入口到外形检测，则将该托盘添加到MovingPalletlist中
                self.MovingPalletlist.append(str(cur[m][0]))

        # 获取正在移动或上架、下架、盘点等任务中的托盘列表MovingPalletlist
        Palletcur = ms().getvalue('WMS.WmsTask', 'Pallet')
        TaskPalletlist = []
        for j in range(len(Palletcur)):
            if Palletcur[j][0] is None:
                TaskPalletlist = []
            else:
                TaskPalletlist.append(Palletcur[j][0])
        self.MovingPalletlist.extend(TaskPalletlist)

        # 随机获取一个当前库存中，在架的托盘palletInventory
        Palletcur1 = ms().getvalue('WMS.InventoryDetail', 'Pallet')
        self.palletInventory = self.isNone(Palletcur1[0][0])

        # 获取入口到外形检测的检测点、异常口配置信息列表
        self.profileCheckShipConfig = readyaml().readyaml('ShipConfig.yaml')['request']['入口到外形检测']
        self.shiplist = []
        self.profileChecklist = []
        self.CheckStationReturnlist = []
        for m in range(len(self.profileCheckShipConfig)):
            ship = self.profileCheckShipConfig[m]['ship']
            profileCheckStation = self.profileCheckShipConfig[m]['profileCheckStation']
            profileCheckStationReturn = self.profileCheckShipConfig[m]['profileCheckStationReturn']
            self.shiplist.append(ship)
            self.profileChecklist.append(profileCheckStation)
            self.CheckStationReturnlist.append(profileCheckStationReturn)

        # while循环实现：如果外形检测入库口的数量小于待上架托盘数，则填充入库口列表的值与托盘数一致
        num = 0
        while len(self.shiplist) < len(self.Palletlist):
            self.shiplist.append(self.shiplist[num])
            self.profileChecklist.append(self.profileChecklist[num])
            num = num+1

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testto_profileCheckStation(self):
        self.checkResult()

        # 获取到当前mongodb中存在的入口到外形检测的任务情况，写入yaml文件，以供test_6_cfm_profileCheckStation.py使用
        doc1 = mg().MongoExecquery('GSMiddleWare', 'TaskBase').find({'TaskType': '入口到外形检测'})
        tasklist = []
        for taskdoc in doc1:
            tasklist.append(taskdoc)
        ypath = os.path.join(path, 'testFile', 'profileCheckTasklist.yaml')
        q = tasklist
        # # 写入到yaml文件
        with open(ypath, 'w', encoding='utf-8') as f:
            yaml.dump(q, f, allow_unicode=True)

    def tearDown(self):
        print('测试结束，输出log完结\n\n')
        ms().closeDB()  # 关闭数据库连接

    def checkResult(self):
        new_url = url + ':9877' + self.path

        # 用一个错误的入库口下发去外形检测的任务
        if self.case_name == 'profileCheckStation_locError':
            self.query['pallet'] = str(self.isNone(self.Palletlist[0]))  # 从已收货完成且不在任务中也不在架上库存中的托盘列表中选一个以用来测试
            try:
                info = RunMain().run_main(self.method, headers=self.headers, url=new_url, data=self.query)
                print(self.query)
                print('在一个错误的入库口下发去外形检测的任务，返回：', info)
            except Exception as e:
                print('接口调用异常：', e)
            else:
                # 用一个错误的入库口下发去外形检测的任务时，接口返回断言不能为True（即任务发起不能成功）
                self.assertEqual(info['error']['code'], 'Exception', '在一个错误的入库口下发去外形检测的任务，任务应该不能下发成功' )

        # 入口到外形检测正常任务发起
        elif self.case_name == 'to_profileCheckStation':
            querylist = []
            # 根据需要上架的托盘数循环获取请求体
            for i in range(len(self.Palletlist)):
                self.query['pallet'] = str(self.isNone(self.Palletlist[i]))
                self.query['fromLocCode'] = str(self.shiplist[i])
                newquery = str(copy(self.query)).encode('utf-8')
                querylist.append(newquery)
            print(querylist)

            # # 将最终将会产生的入口到外形检测任务数量写入到yaml中，以便于test_6_cfm_profileCheckStation在查询获取
            # # 入口到外形检测的任务数时，作为判断test_5_to_profileCheckStatio是否执行完成的标准
            # a = 4  # len(querylist)
            # ypath = os.path.join(path, 'testFile', 'profileCheckTasklist.yaml')
            # q = {'tasklength': a}
            # # 写入到yaml文件
            # with open(ypath, 'w', encoding='utf-8') as f:
            #     yaml.dump(q, f, allow_unicode=True)

            for n in range(len(querylist)):  # len(querylist) 根据querylist长度决定请求几次
                try:
                    info = RunMain().run_main(self.method, headers=self.headers, url=new_url, data=eval(querylist[n]))
                    # 在mongodb中查询该托盘是否有任务类型为‘入口到外形检测’、目标位置与入库口对应的的正在执行的任务
                    newdoc = mg().MongoExecquery('GSMiddleWare', 'TaskBase').find({"$and": [
                        {'Pallets': self.Palletlist[n]}, {'TaskType': '入口到外形检测'},
                        {'ToLocationCode': self.profileChecklist[n]}]})
                    print(querylist[n])
                    print('任务正常下发返回：', info)
                except Exception as e:
                    print('接口调用异常：', e)
                else:
                    self.assertTrue(mg().ResultisNotNone(newdoc))  # 判断mongodb查询结果进行断言

        # 入口到外形检测，托盘当前有任务
        elif self.case_name == 'profileCheckStation_palletMoving' and self.MovingPalletlist:
            self.query['pallet'] = str(self.MovingPalletlist[0])
            self.query['fromLocCode'] = str(random.choice(self.shiplist))  # 从入库口列表中随机取一个元素作为本次任务下发的入库口
            try:
                info = RunMain().run_main(self.method, headers=self.headers, url=new_url, data=self.query)
                print(self.query)
                print('发起的任务中托盘当前有正在执行的任务，返回：', info)
            except Exception as e:
                print('接口调用异常：', e)
            else:
                self.assertEqual(info['error']['code'], 'Exception', '用正在执行的任务的托盘下发去外形检测成功，应不成功')  # 对已经有正在执行的任务的托盘进行外形检测请求时，接口返回断言

        # 入口到外形检测，托盘当前在架上库存中
        elif self.case_name == 'profileCheckStation_palletInventory' and self.palletInventory:

            self.query['pallet'] = str(self.palletInventory)
            self.query['fromLocCode'] = str(random.choice(self.shiplist))  # 从入库口列表中随机取一个元素作为本次任务下发的入库口
            try:

                info = RunMain().run_main(self.method, headers=self.headers, url=new_url, data=self.query)
                print(self.query)
                print('发起的任务中托盘在当前在架库存中，返回：', info)
            except Exception as e:
                print('接口调用异常：', e)
            else:
                # 对已经有正在执行的任务的托盘再次进行去外形检测请求时，接口返回断言不能为True（即任务发起不能成功）
                self.assertIsNot(info, True, msg='对已经在架上的托盘发起再次外形检测任务成功，应不能正常下发')

        # 发起的任务中托盘当前并未收货
        elif self.case_name == 'profileCheckStation_palletNoreceive':
            self.query['fromLocCode'] = str(random.choice(self.shiplist))  # 从入库口列表中随机取一个元素作为本次任务下发的入库口
            try:
                info = RunMain().run_main(self.method, headers=self.headers, url=new_url, data=self.query)
                print(self.query)
                print('发起的任务中托盘当前并未收货，返回：', info)
            except Exception as e:
                print('接口调用异常：', e)
            else:
                # 对还没有进行收货的托盘下发去外形检测请求时，接口返回断言不能为True（即任务发起不能成功）
                self.assertEqual(info['error']['code'], 'Exception')


if __name__ == '__main__':
    testto_profileCheckStation(unittest.TestCase)