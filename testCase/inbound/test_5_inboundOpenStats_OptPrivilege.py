#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对打开状态的收货单（分别包括有明细项及无明细项的）进行各项功能操作验证，包括生效、收货、创建上架单、
取消收货、失效、作废、查询收货记录、修改供应商
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
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'inboundOpenStats_OptPrivilege')


@paramunittest.parametrized(*casexls)
class testinboundActive(unittest.TestCase):
    def setParameters(self, case_name, case_name_ch, method, path, query):
        self.case_name = str(case_name)
        self.case_name_ch = str(case_name_ch)
        self.query = str(query)
        self.path = str(path)
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()

        receiptOrderId_Subclasses = ms().getvalue('WMS.ReceiptOrder', 'receiptOrderId')
        receiptOrderId_noSubclasses = ms().getvalue('WMS.ReceiptOrder', 'receiptOrderId2')

        if self.case_name in ('inboundOpenStats_active1', 'inboundOpenStats_manualCreateMoveDoc1',
                              'inboundOpenStats_cancelReceive1', 'inboundOpenStats_unActive1',
                              'inboundOpenStats_cancel1'):
            spilpath = os.path.split(self.path)  # 拆分路径，将最后部分拆分出来，返回元祖
            # 将拆分后的路径的前面部分和从数据库获取到的receiptOrderId重新组成一个列表,第一个值后面必须以/结尾，否则后续拼凑后的路径会不正确
            spilpathlist = [spilpath[0]+'/', str(receiptOrderId_noSubclasses[0][0])]
            # spilpath[-1] = str(ms().getvalue('WMS.ReceiptOrder', 'receiptOrderId')[0])
            self.path = str(os.path.join(spilpathlist[0], spilpathlist[1]))  # 用列表的两部分拼凑成新路径
            self.headers['Content-Length'] = '0'  # 将headers中的'Content-Type'值改为0，用于请求体为空的接口
        elif self.case_name in ('inboundOpenStats_active2', 'inboundOpenStats_manualCreateMoveDoc2',
                                'inboundOpenStats_cancelReceive2', 'inboundOpenStats_unActive2',
                                'inboundOpenStats_cancel2'):
            spilpath = os.path.split(self.path)  # 拆分路径，将最后部分拆分出来，返回元祖
            # 将拆分后的路径的前面部分和从数据库获取到的receiptOrderId重新组成一个列表,第一个值后面必须以/结尾，否则后续拼凑后的路径会不正确
            spilpathlist = [spilpath[0] + '/', str(receiptOrderId_Subclasses[0][0])]
            self.path = str(os.path.join(spilpathlist[0], spilpathlist[1]))  # 用列表的两部分拼凑成新路径
            self.headers['Content-Length'] = '0'  # 将headers中的'Content-Type'值改为0，用于请求体为空的接口
        elif self.case_name == 'inboundOpenStats_receive2':
            self.query = eval(query)
            # 获取打开状态的收货单的收货明细
            ReceiptOrderItemcur = ms().get_all(
                ms().ExecQuery("SELECT b.Id,b.ExpectedPkgQuantity,b.CreatorId FROM WMS.ReceiptOrder a "
                               "INNER JOIN WMS.ReceiptOrderItem b ON a.Id = b.ReceiptOrderId "
                               "AND a.XStatus='OPEN'"))
            LocationIdcur = ms().getvalue('WMS.Location', 'LocationId')  # 获取货位类型为‘收货’的库位
            self.query['ReceiptOrderItemId'] = str(ReceiptOrderItemcur[0][0])
            self.query['ReceivedPkgQuantity'] = str(ReceiptOrderItemcur[0][1])
            self.query['LocationId'] = str(ms().transformNone(LocationIdcur[0][0]))
            self.query['Pallet'] = 'TP' + str(ms().getvalue('sequencetest', 'VALUE')[0][0])
            self.query['WorkerId'] = str(ReceiptOrderItemcur[0][2])
        elif self.case_name == 'inboundOpenStats_queryReceiverRecords1':
            self.query = eval(query)
            self.query['condition']['receiptOrderId']['='] = str(receiptOrderId_noSubclasses[0][0])
        elif self.case_name == 'inboundOpenStats_queryReceiverRecords2':
            self.query = eval(query)
            self.query['condition']['receiptOrderId']['='] = str(receiptOrderId_Subclasses[0][0])
        elif self.case_name == 'inboundOpenStats_correctSupplier1':
            supplierIdcur = ms().getvalue('WMS.Orgnization', 'supplierId')
            spilpath = os.path.split(self.path)  # 拆分路径，将最后部分拆分出来，返回元祖
            # 将拆分后的路径的前面部分和从数据库获取到的supplierId和receiptOrderCode重新组成一个列表,第一个值后面必须以/结尾，否则后续拼凑后的路径会不正确
            self.spilpathlist = [spilpath[0] + '/', str(supplierIdcur[0][0])+'?'+'receiptOrderCode=' +
                                 str(receiptOrderId_noSubclasses[0][9])]
            self.path = str(os.path.join(self.spilpathlist[0], self.spilpathlist[1]))  # 用列表的两部分拼凑成新路径
            self.headers['Content-Length'] = '0'  # 将headers中的'Content-Type'值改为0，用于请求体为空的接口
        elif self.case_name == 'inboundOpenStats_correctSupplier2':
            supplierIdcur = ms().getvalue('WMS.Orgnization', 'supplierId')
            spilpath = os.path.split(self.path)  # 拆分路径，将最后部分拆分出来，返回元祖
            # 将拆分后的路径的前面部分和从数据库获取到的supplierId和receiptOrderCode重新组成一个列表,第一个值后面必须以/结尾，否则后续拼凑后的路径会不正确
            self.spilpathlist1 = [spilpath[0] + '/', str(supplierIdcur[0][0])+'?'+'receiptOrderCode=' +
                                  str(receiptOrderId_Subclasses[0][9])]
            self.path = str(os.path.join(self.spilpathlist1[0], self.spilpathlist1[1]))  # 用列表的两部分拼凑成新路径
            self.headers['Content-Length'] = '0'  # 将headers中的'Content-Type'值改为0，用于请求体为空的接口

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
            if self.case_name == 'inboundOpenStats_active1':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertIsNot(True, info,
                                 '测试不通过，对打开状态、无收货明细的收货单进行生效时，生效成功了，应生效不成功，接口没有正确的对应处理机制！')
            elif self.case_name == 'inboundOpenStats_active2':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertIs(True, info, '测试不通过，对打开状态、有收货明细的收货单进行生效时，接口没有返回true！')
            elif self.case_name == 'inboundOpenStats_receive2':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('收货时只有状态为生效和收货中的入库单可以收货!', info['error']['message'],
                                 '对打开状态、有收货明细的收货单进行收货时，接口没有正确的对应处理机制！')
            elif self.case_name == 'inboundOpenStats_manualCreateMoveDoc1':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('请先收货，再创建上架单！', info['error']['message'],
                                 '对打开状态、无收货明细的收货单进行收货时，接口没有正确的对应处理机制！')
            elif self.case_name == 'inboundOpenStats_manualCreateMoveDoc2':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('请先收货，再创建上架单！',
                                 info['error']['message'],
                                 '对打开状态、有收货明细的收货单进行创建上架单时，接口没有正确的对应处理机制！')
            elif self.case_name == 'inboundOpenStats_cancelReceive1':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('取消收货时入库单状态:OPEN错误',
                                 info['error']['message'],
                                 '对打开状态、无收货明细的收货单进行取消收货时，接口没有正确的对应处理机制！')
            elif self.case_name == 'inboundOpenStats_cancelReceive2':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('取消收货时入库单状态:OPEN错误',
                                 info['error']['message'],
                                 '对打开状态、有收货明细的收货单进行取消收货时，接口没有正确的对应处理机制！')
            elif self.case_name == 'inboundOpenStats_unActive1':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('该单据不是生效状态，无法失效！',
                                 info['error']['message'],
                                 '对打开状态、无收货明细的收货单进行失效操作时，接口没有正确的对应处理机制！')
            elif self.case_name == 'inboundOpenStats_unActive2':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('该单据不是生效状态，无法失效！',
                                 info['error']['message'],
                                 '对打开状态、有收货明细的收货单进行失效操作时，接口没有正确的对应处理机制！')
            elif self.case_name == 'inboundOpenStats_cancel1':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertIs(True, info, '测试不通过，对打开状态、无收货明细的收货单进行作废时，接口没有返回true！')
            elif self.case_name == 'inboundOpenStats_cancel2':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertIs(True, info, '测试不通过，对打开状态、有收货明细的收货单进行作废时，接口没有返回true！')
            elif self.case_name == 'inboundOpenStats_queryReceiverRecords1':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual(0, info['totalCount'], '测试不通过，对打开状态的收货单进行收货记录查询，应没有记录！')
            elif self.case_name == 'inboundOpenStats_queryReceiverRecords2':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual(0, info['totalCount'], '测试不通过，对打开状态的收货单进行收货记录查询，应没有记录！')
            elif self.case_name == 'inboundOpenStats_correctSupplier1':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                sqltext = "SELECT SupplierId FROM WMS.ReceiptOrder WHERE XCode='%s'" % str(self.spilpathlist[1][-14:])
                SupplierIdcur = ms().get_all(ms().ExecQuery(sqltext))  # 查询数据库该收货单当前的供应商
                self.assertFalse(any(x for x in (self.assertEqual(0, info, '修改供应商不成功，接口返回不正确！'),
                                                 self.assertEqual(str(self.spilpathlist[1][0:36]),
                                                                  str(SupplierIdcur[0][0]),
                                                                  '修改供应商不成功，数据库该收货单的供应商不是用户修改的供应商！'))))
            elif self.case_name == 'inboundOpenStats_correctSupplier2':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                sqltext = "SELECT SupplierId FROM WMS.ReceiptOrder WHERE XCode='%s'" % str(self.spilpathlist1[1][-14:])
                SupplierIdcur = ms().get_all(ms().ExecQuery(sqltext))  # 查询数据库该收货单当前的供应商
                self.assertFalse(any(x for x in (self.assertEqual(1, info, '修改供应商不成功，接口返回不正确！'),
                                                 self.assertEqual(str(self.spilpathlist1[1][0:36]),
                                                                  str(SupplierIdcur[0][0]),
                                                                  '修改供应商不成功，数据库该收货单的供应商不是用户修改的供应商！'))))


if __name__ == '__main__':
    unittest.main()




