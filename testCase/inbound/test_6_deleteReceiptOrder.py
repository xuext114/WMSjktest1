#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""删除最新更新的、打开状态的收货主单据
"""

import ast
import unittest
from common.configHttp import RunMain
import paramunittest
from testFile import geturlParams
from testFile import readExcel
from testFile.readyaml import readyaml
from common.configDb import MSSQL as ms
import json
import datetime
import random
from copy import copy
import uuid

url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'deleteReceiptOrder')


@paramunittest.parametrized(*casexls)
class testdeleteReceiptOrder(unittest.TestCase):
    def setParameters(self, case_name, case_name_ch, method, path, query):
        self.case_name = str(case_name)
        self.case_name_ch = str(case_name_ch)
        self.path = str(path)
        self.query = eval(query)
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()
        self.querylist = []
        # 从数据库查询到可用于进行删除的入库单
        # 有收货明细，打开状态的收货单
        cur1 = ms().getvalue('WMS.ReceiptOrder', 'receiptOrderId')
        # 无收货明细，打开状态的收货单
        cur2 = ms().getvalue('WMS.ReceiptOrder', 'receiptOrderId2')

        if self.case_name == 'deleteReceiptOrder_nodetails':
            self.query['creator'] = str(ms().transformNone(cur2[0][3]))
            self.query['lastModifier'] = str(ms().transformNone(cur2[0][6]))
            self.query['id'] = str(ms().transformNone(cur2[0][0]))
            self.query['lastModificationTime'] = cur2[0][4].strftime("%Y-%m-%d %H:%M:%S")
            self.query['lastModifierId'] = str(ms().transformNone(cur2[0][5]))
            self.query['creationTime'] = cur2[0][1].strftime("%Y-%m-%d %H:%M:%S")
            self.query['creatorId'] = str(ms().transformNone(cur2[0][2]))
            self.query['whId'] = str(ms().transformNone(cur2[0][7]))
            self.query['ownerId'] = str(ms().transformNone(cur2[0][10]))
            self.query['supplierId'] = str(ms().transformNone(cur2[0][11]))
            self.query['xCode'] = str(ms().transformNone(cur2[0][9]))
            self.query['billTypeId'] = str(ms().transformNone(cur2[0][8]))
            self.query['xStatus'] = ms().transformNone(cur2[0][12])
            self.query['shelvesStatus'] = str(ms().transformNone(cur2[0][13]))
            self.query['expectedPkgQuantity'] = float(cur2[0][14])
            self.query['receivedPkgQuantity'] = float(cur2[0][15])
            self.query['movedPkgQuantity'] = float(cur2[0][16])
            self.query['tolocationId'] = str(ms().transformNone(cur2[0][17]))
            self.query['relatedBill1'] = str(ms().transformNone(cur2[0][50]))
            self.query['relatedBill2'] = str(ms().transformNone(cur2[0][51]))
            self.query['relatedBill3'] = str(ms().transformNone(cur2[0][52]))
            if cur1[0][49]:
                orderdate = cur2[0][49].strftime("%Y-%m-%d %H:%M:%S")
            else:
                orderdate = ''
            if cur1[0][47]:
                estimatedate = cur2[0][49].strftime("%Y-%m-%d %H:%M:%S")
            else:
                estimatedate = ''
            self.query['orderDate'] = orderdate
            self.query['estimateDate'] = estimatedate
            self.query['startReceivedDate'] = str(ms().transformNone(cur2[0][53]))
            self.query['endReceivedDate'] = str(ms().transformNone(cur2[0][46]))
            self.query['fromName'] = str(ms().transformNone(cur2[0][48]))
            self.query['contactCountry'] = str(ms().transformNone(cur2[0][39]))
            self.query['contactProvince'] = str(ms().transformNone(cur2[0][44]))
            self.query['contactCity'] = str(ms().transformNone(cur2[0][38]))
            self.query['contactAddress'] = str(ms().transformNone(cur2[0][37]))
            self.query['contactPostcode'] = str(ms().transformNone(cur2[0][43]))
            self.query['contactName'] = str(ms().transformNone(cur2[0][54]))
            self.query['contactMobile'] = str(ms().transformNone(cur2[0][42]))
            self.query['contactTelephone'] = str(ms().transformNone(cur2[0][45]))
            self.query['contactFax'] = str(ms().transformNone(cur2[0][41]))
            self.query['contactEmail'] = str(ms().transformNone(cur2[0][40]))
            self.query['operateStatus'] = str(ms().transformNone(cur2[0][18]))
            self.query['erpStatus'] = str(ms().transformNone(cur2[0][19]))
            self.query['isOffLine'] = str(ms().transformNone(cur2[0][20]))
            self.query['trusteeBy'] = str(ms().transformNone(cur2[0][21]))
            self.query['qcBy'] = str(ms().transformNone(cur2[0][22]))
            self.query['storekeeper'] = str(ms().transformNone(cur2[0][23]))
            self.query['tradingCompany'] = str(ms().transformNone(cur2[0][24]))
            self.query['relationCode'] = str(ms().transformNone(cur2[0][25]))
            self.query['comments'] = str(ms().transformNone(cur2[0][26]))
            self.query['str1'] = str(ms().transformNone(cur2[0][27]))
            self.query['str2'] = str(ms().transformNone(cur2[0][28]))
            self.query['str3'] = str(ms().transformNone(cur2[0][29]))
            self.query['str4'] = str(ms().transformNone(cur2[0][30]))
            self.query['str5'] = str(ms().transformNone(cur2[0][31]))
            self.query['str6'] = str(ms().transformNone(cur2[0][32]))
            self.query['str7'] = str(ms().transformNone(cur2[0][33]))
            self.query['str8'] = str(ms().transformNone(cur2[0][34]))
            self.query['str9'] = str(ms().transformNone(cur2[0][35]))
            self.query['str10'] = str(ms().transformNone(cur2[0][36]))

        elif self.case_name == 'deleteReceiptOrder_parametersNotnull':
            self.query['id'] = str(ms().transformNone(cur1[0][0]))
            self.query['billTypeId'] = str(ms().transformNone(cur1[0][8]))
            self.query['expectedPkgQuantity'] = float(cur1[0][14])
            self.query['receivedPkgQuantity'] = float(cur1[0][15])
            self.query['movedPkgQuantity'] = float(cur1[0][16])
            self.query['creationTime'] = cur1[0][1].strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.query['creator'] = str(ms().transformNone(cur1[0][3]))
            self.query['lastModifier'] = str(ms().transformNone(cur1[0][6]))
            self.query['id'] = str(ms().transformNone(cur1[0][0]))
            self.query['lastModificationTime'] = cur1[0][4].strftime("%Y-%m-%d %H:%M:%S")
            self.query['lastModifierId'] = str(ms().transformNone(cur1[0][5]))
            self.query['creationTime'] = cur1[0][1].strftime("%Y-%m-%d %H:%M:%S")
            self.query['creatorId'] = str(ms().transformNone(cur1[0][2]))
            self.query['whId'] = str(ms().transformNone(cur1[0][7]))
            self.query['ownerId'] = str(ms().transformNone(cur1[0][10]))
            self.query['supplierId'] = str(ms().transformNone(cur1[0][11]))
            self.query['xCode'] = str(ms().transformNone(cur1[0][9]))
            self.query['billTypeId'] = str(ms().transformNone(cur1[0][8]))
            self.query['xStatus'] = ms().transformNone(cur1[0][12])
            self.query['shelvesStatus'] = str(ms().transformNone(cur1[0][13]))
            self.query['expectedPkgQuantity'] = float(cur1[0][14])
            self.query['receivedPkgQuantity'] = float(cur1[0][15])
            self.query['movedPkgQuantity'] = float(cur1[0][16])
            self.query['tolocationId'] = str(ms().transformNone(cur1[0][17]))
            self.query['relatedBill1'] = str(ms().transformNone(cur1[0][50]))
            self.query['relatedBill2'] = str(ms().transformNone(cur1[0][51]))
            self.query['relatedBill3'] = str(ms().transformNone(cur1[0][52]))
            if cur1[0][49]:
                orderdate = cur1[0][49].strftime("%Y-%m-%d %H:%M:%S")
            else:
                orderdate = ''
            if cur1[0][47]:
                estimatedate = cur1[0][49].strftime("%Y-%m-%d %H:%M:%S")
            else:
                estimatedate = ''
            self.query['orderDate'] = orderdate
            self.query['estimateDate'] = estimatedate
            self.query['startReceivedDate'] = str(ms().transformNone(cur1[0][53]))
            self.query['endReceivedDate'] = str(ms().transformNone(cur1[0][46]))
            self.query['fromName'] = str(ms().transformNone(cur1[0][48]))
            self.query['contactCountry'] = str(ms().transformNone(cur1[0][39]))
            self.query['contactProvince'] = str(ms().transformNone(cur1[0][44]))
            self.query['contactCity'] = str(ms().transformNone(cur1[0][38]))
            self.query['contactAddress'] = str(ms().transformNone(cur1[0][37]))
            self.query['contactPostcode'] = str(ms().transformNone(cur1[0][43]))
            self.query['contactName'] = str(ms().transformNone(cur1[0][54]))
            self.query['contactMobile'] = str(ms().transformNone(cur1[0][42]))
            self.query['contactTelephone'] = str(ms().transformNone(cur1[0][45]))
            self.query['contactFax'] = str(ms().transformNone(cur1[0][41]))
            self.query['contactEmail'] = str(ms().transformNone(cur1[0][40]))
            self.query['operateStatus'] = str(ms().transformNone(cur1[0][18]))
            self.query['erpStatus'] = str(ms().transformNone(cur1[0][19]))
            self.query['isOffLine'] = str(ms().transformNone(cur1[0][20]))
            self.query['trusteeBy'] = str(ms().transformNone(cur1[0][21]))
            self.query['qcBy'] = str(ms().transformNone(cur1[0][22]))
            self.query['storekeeper'] = str(ms().transformNone(cur1[0][23]))
            self.query['tradingCompany'] = str(ms().transformNone(cur1[0][24]))
            self.query['relationCode'] = str(ms().transformNone(cur1[0][25]))
            self.query['comments'] = str(ms().transformNone(cur1[0][26]))
            self.query['str1'] = str(ms().transformNone(cur1[0][27]))
            self.query['str2'] = str(ms().transformNone(cur1[0][28]))
            self.query['str3'] = str(ms().transformNone(cur1[0][29]))
            self.query['str4'] = str(ms().transformNone(cur1[0][30]))
            self.query['str5'] = str(ms().transformNone(cur1[0][31]))
            self.query['str6'] = str(ms().transformNone(cur1[0][32]))
            self.query['str7'] = str(ms().transformNone(cur1[0][33]))
            self.query['str8'] = str(ms().transformNone(cur1[0][34]))
            self.query['str9'] = str(ms().transformNone(cur1[0][35]))
            self.query['str10'] = str(ms().transformNone(cur1[0][36]))
            if self.case_name == 'deleteReceiptOrder_receiptOrderId_null':
                self.query['id'] = ''
            elif self.case_name == 'deleteReceiptOrder_billTypeId_null':
                self.query['billTypeId'] = ''
            elif self.case_name == 'deleteReceiptOrder_expectedPkgQuantity_null':
                self.query['expectedPkgQuantity'] = ''
            elif self.case_name == 'deleteReceiptOrder_receiptOrderId_error':
                self.query['id'] = uuid.uuid1()
            elif self.case_name == 'deleteReceiptOrder_billTypeId_error':
                self.query['billTypeId'] = uuid.uuid1()

        self.query = str(self.query).encode('utf-8')

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testdeleteReceiptOrder(self):
        self.checkResult()

    def tearDown(self):
        print('测试结束....')
        ms().closeDB()  # 关闭数据库连接

    def checkResult(self):
        new_url = url + ':44349' + self.path
        try:
            info = RunMain().run_main(self.method, headers=self.headers, url=new_url, data=self.query)
        except Exception as e:
            print('接口调用异常：', e)
            raise Exception
        else:
            if self.case_name == 'deleteReceiptOrder_nodetails':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                # 查询数据库是否还有该收货单
                sqltext1 = "SELECT id FROM WMS.ReceiptOrder WHERE Id = '%s'" % self.query['id']
                ReceiptOrdercur = ms().get_all(ms().ExecQuery(sqltext1))
                self.assertFalse(any(x for x in (self.assertIs(info, True, '调用删除入库单接口，返回结果不是True！'),
                                                 self.assertFalse(ReceiptOrdercur[0][0], '调用接口删除的收货单还存在于数据库！'))))
            elif self.case_name == 'deleteReceiptOrder_parametersNotnull':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                # 查询数据库是否还有该收货单
                sqltext1 = "SELECT id FROM WMS.ReceiptOrder WHERE Id = '%s'" % self.query['id']
                # 查询数据库是否还有该收货单的收货明细
                sqltext2 = "SELECT id FROM WMS.ReceiptOrderItem WHERE ReceiptOrderId = '%s'" % self.query['id']
                ReceiptOrdercur = ms().get_all(ms().ExecQuery(sqltext1))
                ReceiptOrderItemcur = ms().get_all(ms().ExecQuery(sqltext2))
                self.assertFalse(any(x for x in (self.assertIs(info, True, '调用删除入库单接口，返回结果不是True！'),
                                                 self.assertFalse(ReceiptOrdercur[0][0], '调用接口删除的收货单还存在于数据库！'),
                                                 self.assertFalse(ReceiptOrderItemcur[0][0],
                                                                  '调用接口删除的所属收货单的明细项还存在于数据库！'))))
            elif self.case_name == 'deleteReceiptOrder_details':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                # 查询数据库是否还有该收货单
                sqltext1 = "SELECT id FROM WMS.ReceiptOrder WHERE Id = '%s'" % self.query['id']
                # 查询数据库是否还有该收货单的收货明细
                sqltext2 = "SELECT id FROM WMS.ReceiptOrderItem WHERE ReceiptOrderId = '%s'" % self.query['id']
                ReceiptOrdercur = ms().get_all(ms().ExecQuery(sqltext1))
                ReceiptOrderItemcur = ms().get_all(ms().ExecQuery(sqltext2))
                self.assertFalse(any(x for x in (self.assertIs(info, True, '调用删除入库单接口，返回结果不是True！'),
                                                 self.assertFalse(ReceiptOrdercur[0][0], '调用接口删除的收货单还存在于数据库！'),
                                                 self.assertFalse(ReceiptOrderItemcur[0][0],
                                                                  '调用接口删除的所属收货单的明细项还存在于数据库！'))))
            elif self.case_name == 'deleteReceiptOrder_receiptOrderId_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('收货单id为空！', info['error'][
                    'message'], '删除收货单时，收货单id为空时，接口没有正确的对应处理机制！')
            elif self.case_name == 'deleteReceiptOrder_billTypeId_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('单据类型id为空！', info['error'][
                    'message'], '删除收货单时，单据类型id为空时，接口没有正确的对应处理机制！')
            elif self.case_name == 'deleteReceiptOrder_expectedPkgQuantity_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('期望数量为空！', info['error'][
                    'message'], '删除收货单时，期望数量为空时，接口没有正确的对应处理机制！')
            elif self.case_name == 'deleteReceiptOrder_receiptOrderId_error':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('收货单id错误！', info['error'][
                    'message'], '删除收货单时，收货单id错误，接口没有正确的对应处理机制！')
            elif self.case_name == 'deleteReceiptOrder_billTypeId_error':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('单据类型id错误！', info['error'][
                    'message'], '删除收货单时，收货单id错误，接口没有正确的对应处理机制！')


if __name__ == '__main__':
    unittest.main()



