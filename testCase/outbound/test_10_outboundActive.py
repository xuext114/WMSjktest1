#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生效最新一个状态为打开，有发货明细的发货单
"""

import ast
import os
import unittest
from common.configHttp import RunMain
import paramunittest
from testFile import geturlParams
from testFile import readExcel
from testFile.readyaml import readyaml
from common.configDb import MSSQL as ms


url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'outboundActive')


@paramunittest.parametrized(*casexls)
class testoutboundActive(unittest.TestCase):
    def setParameters(self, case_name, method, path, query):
        self.case_name = str(case_name)
        spilpath = os.path.split(path)  # 拆分路径，将最后部分拆分出来，返回元祖
        # 将拆分后的路径的前面部分和从数据库获取到的receiptOrderId重新组成一个列表,第一个值后面必须以/结尾，否则后续拼凑后的路径会不正确
        spilpathlist = [spilpath[0]+'/', str(ms().getvalue('WMS.ShipOrder', 'ShipOrderId')[0][0])]
        # spilpath[-1] = str(ms().getvalue('WMS.ReceiptOrder', 'receiptOrderId')[0])
        self.path = str(os.path.join(spilpathlist[0], spilpathlist[1]))  # 用列表的两部分拼凑成新路径
        self.query = str(query)
        self.method = str(method)
        headers1 = readyaml().get_headerIncloudToken()
        headers1['Content-Length'] = '0'  # 将headers中的'Content-Type'值改为0，用于请求体为空的接口
        self.headers = headers1

        # ms().closeDB()  # 关闭数据库连接
        self.query = str(self.query).encode('utf-8')


    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testoutboundActive(self):
        self.checkResult()

    def tearDown(self):
        print('测试结束，输出log完结\n\n')
        ms().closeDB()  # 关闭数据库连接

    def checkResult(self):
        new_url = url + ':44349' + self.path
        print(new_url)
        info = RunMain().run_main(self.method, headers=self.headers, url=new_url)
        print('生效发货单，结果返回：', info)
        if self.case_name == 'outboundActive':
            self.assertIs(info, True)


if __name__ == '__main__':
    # testinboundActive(unittest.TestCase)
    unittest.main()

