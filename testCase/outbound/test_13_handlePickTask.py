#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人工或半自动拣货时，WMS拣货确认
    从数据库查询获取中间件出库任务报完成，WMS尚未拣货的任务，将查询到的任务数据组成列表作为拣货确认接口参数
    根据不同参数依次调用接口进行拣货确认
    【断言】拣货后的该托盘的物料数量是否等于拣货前的数量减去拣货数量，如果是，断言成功
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
import random
import json
import time


url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'handlePickTask')


@paramunittest.parametrized(*casexls)
class testhandlePickTask(unittest.TestCase):

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

        sqltext1 = "SELECT Id, MovedPkgQuantity, Pallet FROM WMS.WmsTask " \
                   "WHERE Type='MV_PICKTICKET_PICKING' AND Status='WORKING' AND MovedPkgQuantity>0 "
        cur1 = ms().get_all(ms().ExecQuery(sqltext1))  # 从数据库查询获取中间件出库任务已执行完成，但wms尚未拣货的任务
        self.taskidlist = []
        self.MovedPkgQtylist = []
        self.Palletlist = []
        if cur1[0][0] is not None:  # 如果能从数据库获取到任务数据，将查询到字段数据添加到列表作为后续接口调用的参数
            for i in range(len(cur1)):
                self.taskidlist.append(cur1[i][0])
                self.MovedPkgQtylist.append(cur1[i][1])  # 直接用本次任务实际移库数量即该托盘实际的物料数量，而非用户发货单实际需求数量
                self.Palletlist.append(cur1[i][2])
        print('待拣货的任务id：', self.taskidlist)
        print('待拣货的任务的物料移位数量：', self.MovedPkgQtylist)
        print('待拣货的任务的托盘：', self.Palletlist)

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testhandlePickTask(self):
        self.checkResult()

    def tearDown(self):
        print('测试结束，输出log完结\n\n')
        ms().closeDB()  # 关闭数据库连接

    def checkResult(self):
        new_url = url + ':44349' + self.path
        if self.case_name == 'handlePickTask':
            print(self.case_name)

            for m in range(len(self.taskidlist)):  # 循环组建请求体进行确认拣货
                self.query['TaskId'] = str(self.taskidlist[m])
                self.query['MovedPkgQty'] = str(self.MovedPkgQtylist[m])
                print('确认拣货接口请求体为：', self.query)
                sqltext2 = "SELECT PackageQuantity FROM WMS.InventoryDetail WHERE Pallet ='%s'" % self.Palletlist[m]
                cur2 = ms().get_all(ms().ExecQuery(sqltext2))  # 获取拣货前该托盘物料数量
                beforPackageQuantity = cur2[0][0]
                try:
                    info = RunMain().run_main(self.method, headers=self.headers, url=new_url,
                                              data=json.dumps(self.query))
                except Exception as e:
                    print('接口调用异常：', e)
                    raise Exception
                else:
                    print('拣货完成，返回:', info)
                    # 查询数据库库存，检查本次任务中的托盘在出库口的地面库存中的物料数量是否等于拣货前数量减去拣货数量
                    cur3 = ms().get_all(ms().ExecQuery(sqltext2))  # 获取拣货后该托盘物料数量
                    afterPackageQuantity = cur3[0][0]
                    self.assertEqual(afterPackageQuantity, beforPackageQuantity-self.MovedPkgQtylist[m],
                                     '拣货后数量不等于拣货前数量减去拣货数量！')


if __name__ == '__main__':
    unittest.main(verbosity=2)
