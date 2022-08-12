#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对更新时间最早的打开状态的收货单（有收货明细）进行生效和对更新时间最早的生效状态的收货单进行失效操作
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
import uuid


url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'ActiveAndUnactiveReceiptOrder')


@paramunittest.parametrized(*casexls)
class testinboundActive(unittest.TestCase):
    def setParameters(self, case_name, case_name_ch, method, path, query):
        self.case_name = str(case_name)
        self.case_name_ch = str(case_name_ch)
        self.query = str(query)
        self.path = str(path)
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()
        self.headers['Content-Length'] = '0'  # 将headers中的'Content-Type'值改为0，用于请求体为空的接口

        # 从数据库查询获取更新时间最早的打开状态且有收货明细的收货单
        openStatsReceiptOrderId = ms().get_all(
            ms().ExecQuery("SELECT Id FROM WMS.ReceiptOrder a WHERE XStatus ='OPEN'"
                           "AND EXISTS(SELECT ReceiptOrderId FROM WMS.ReceiptOrderItem b "
                           "WHERE a.Id=b.ReceiptOrderId)ORDER BY a.LastModificationTime "))
        # 从数据库查询获取更新时间最早的生效状态的收货单
        activeStatsReceiptOrderId = ms().get_all(
            ms().ExecQuery("SELECT Id FROM WMS.ReceiptOrder a WHERE XStatus ='ACTIVE' "
                           "ORDER BY LastModificationTime"))

        if self.case_name =='ActiveReceiptOrder':
            spilpath = os.path.split(self.path)  # 拆分路径，将最后部分拆分出来，返回元祖
            # 将拆分后的路径的前面部分和从数据库获取到的receiptOrderId重新组成一个列表,第一个值后面必须以/结尾，否则后续拼凑后的路径会不正确
            self.spilpathlist1 = [spilpath[0]+'/', str(openStatsReceiptOrderId[0][0])]
            self.path = str(os.path.join(self.spilpathlist1[0], self.spilpathlist1[1]))  # 用列表的两部分拼凑成新路径
        elif self.case_name == 'ActiveReceiptOrder_idError':
            spilpath = os.path.split(self.path)  # 拆分路径，将最后部分拆分出来，返回元祖
            # 将拆分后的路径的前面部分和随机获得的uuid重新组成一个列表,第一个值后面必须以/结尾，否则后续拼凑后的路径会不正确
            spilpathlist = [spilpath[0] + '/', str(uuid.uuid1())]
            self.path = str(os.path.join(spilpathlist[0], spilpathlist[1]))  # 用列表的两部分拼凑成新路径
        elif self.case_name == 'UnactiveReceiptOrder':
            spilpath = os.path.split(self.path)  # 拆分路径，将最后部分拆分出来，返回元祖
            # 将拆分后的路径的前面部分和从数据库获取到的receiptOrderId重新组成一个列表,第一个值后面必须以/结尾，否则后续拼凑后的路径会不正确
            self.spilpathlist2 = [spilpath[0] + '/', str(activeStatsReceiptOrderId[0][0])]
            self.path = str(os.path.join(self.spilpathlist2[0], self.spilpathlist2[1]))  # 用列表的两部分拼凑成新路径
        elif self.case_name == 'UnactiveReceiptOrder_idError':
            spilpath = os.path.split(self.path)  # 拆分路径，将最后部分拆分出来，返回元祖
            # 将拆分后的路径的前面部分和随机获得的uuid重新组成一个列表,第一个值后面必须以/结尾，否则后续拼凑后的路径会不正确
            spilpathlist = [spilpath[0] + '/', str(uuid.uuid1())]
            self.path = str(os.path.join(spilpathlist[0], spilpathlist[1]))  # 用列表的两部分拼凑成新路径
        elif self.case_name in ('ActiveReceiptOrder2', 'ActiveReceiptOrder3',
                                'ActiveReceiptOrder4', 'ActiveReceiptOrder5'):
            spilpath = os.path.split(self.path)  # 拆分路径，将最后部分拆分出来，返回元祖
            # 将拆分后的路径的前面部分和从数据库获取到的receiptOrderId重新组成一个列表,第一个值后面必须以/结尾，否则后续拼凑后的路径会不正确
            self.spilpathlist1 = [spilpath[0] + '/', str(openStatsReceiptOrderId[0][0])]
            self.path = str(os.path.join(self.spilpathlist1[0], self.spilpathlist1[1]))  # 用列表的两部分拼凑成新路径

        self.query = str(self.query).encode('utf-8')

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testinboundActive(self):
        self.checkResult()

    def tearDown(self):
        print('测试结束，输出log完结\n\n')
        ms().closeDB()  # 关闭数据库连接

    def checkResult(self):
        new_url = url + ':44349' + self.path
        try:
            info = RunMain().run_main(self.method, headers=self.headers, url=new_url, data=self.query)
        except Exception as e:
            print('接口调用异常：', e)
            raise Exception
        else:
            if self.case_name == 'ActiveReceiptOrder':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                # 查询数据库该收货单当前的状态
                sqltext = "SELECT XStatus FROM WMS.ReceiptOrder WHERE Id ='%s'" % str(self.spilpathlist1[1])
                Xstats = ms().get_all(ms().ExecQuery(sqltext))
                self.assertFalse(any(x for x in (self.assertIs(True, info,
                                                               '测试不通过，对打开状态、有收货明细的收货单进行生效时，接口没有返回true！'),
                                                 self.assertEqual('ACTIVE', Xstats[0][0],
                                                                  '对打开状态的收货单进行生效后，数据库中该收货单状态不是ACTIVE！'))))
            elif self.case_name == 'ActiveReceiptOrder_idError':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('不存在该Id的入库单据，请查证后再试！', info['error']['message'],
                                 '对打开状态、有收货明细的收货单进行生效，收货单id错误时，接口没有正确的对应处理机制！')
            elif self.case_name == 'UnactiveReceiptOrder':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                # 查询数据库该收货单当前的状态
                sqltext = "SELECT XStatus FROM WMS.ReceiptOrder WHERE Id ='%s'" % str(self.spilpathlist2[1])
                Xstats = ms().get_all(ms().ExecQuery(sqltext))
                self.assertFalse(any(x for x in (self.assertIs(True, info,
                                                               '测试不通过，对生效状态的收货单进行失效时，接口没有返回true！'),
                                                 self.assertEqual('OPEN', Xstats[0][0],
                                                                  '对生效状态的收货单进行失效后，数据库中该收货单状态不是OPEN！'))))
            elif self.case_name == 'UnactiveReceiptOrder_idError':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('不存在该Id的入库单据，请查证后再试！', info['error']['message'],
                                 '对生效状态、有收货明细的收货单进行生效，收货单id错误时，接口没有正确的对应处理机制！')


if __name__ == '__main__':
    unittest.main()


