#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import unittest
from common.configHttp import RunMain
import paramunittest
from testFile import geturlParams
# import urllib.parse
from testFile import readExcel
from testFile.readyaml import readyaml
from common.configDb import MSSQL as ms
from testFile.readSql import get_sql
import time
import json


url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'shipOrder')


@paramunittest.parametrized(*casexls)
class testShipOrder(unittest.TestCase):
    def setParameters(self, case_name, method, path, query):
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = ast.literal_eval(query)
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()

        self.query['ownerId'] = str(ms().getvalue('WMS.Orgnization', 'ownerId')[0][0])
        self.query['customerId'] = str(ms().getvalue('WMS.Orgnization', 'ownerId')[0][0])
        self.query['billTypeId'] = str(ms().getvalue('WMS.BillType', 'SHIP_billTypeId')[0][0])
        self.query['dockId'] = str(ms().getvalue('WMS.Dock', 'dockId')[0][0])
        self.query['receivedBy'] = str(ms().getvalue('WMS.Orgnization', 'ownerId')[0][1])
        self.query['dockId'] = str(ms().getvalue('WMS.Dock', 'dockId')[0][0])
        # self.query['whId'] = '00000000-0000-0000-0000-000000000000'
        self.query['isOffLine'] = False
        print(self.query)

        # self.query = str(self.query)

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testShipOrder(self):
        self.checkResult()

    def tearDown(self):
        print('测试结束，输出log完结\n\n')
        ms().closeDB()  # 关闭数据库连接

    def checkResult(self):
        new_url = url + ':44349' + self.path
        info = RunMain().run_main(self.method, headers=self.headers, url=new_url, data=json.dumps(self.query))
        print('新建返货单，返回：', info)
        if self.case_name == 'creatshipOrder':
            self.assertEqual(info['xStatus'], "OPEN")


if __name__ == '__main__':
    unittest.main()




