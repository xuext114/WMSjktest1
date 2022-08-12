#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""编辑最新的、打开状态的某个收货主单据
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
from decimal import Decimal
import uuid

url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'updatereceiptOrder')


@paramunittest.parametrized(*casexls)
class testupdatereceiptOrder(unittest.TestCase):
    def setParameters(self, case_name, case_name_ch, method, path, query):
        self.case_name = str(case_name)
        self.case_name_ch = str(case_name_ch)
        self.path = str(path)
        self.query = eval(query)
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()
        self.querylist = []
        # 从数据库查询到可用于进行编辑的入库单
        cur = ms().getvalue('WMS.ReceiptOrder', 'receiptOrderId')
        cur2 = ms().getvalue('WMS.ReceiptOrder', 'receiptOrderId2')
        # 从数据库查询可用于修改单据类型的单据类型id
        billTypecur = ms().get_all(ms().ExecQuery("SELECT id FROM WMS.BillType WHERE XType='RECEIVE' ORDER BY newid()"))

        if case_name == 'updatereceiptOrder':  # 从数据库查询状态为打开、有收货明细的收货单的信息赋值给请求体参数
            self.query['creator'] = str(ms().transformNone(cur[0][3]))
            self.query['lastModifier'] = str(ms().transformNone(cur[0][6]))
            self.query['id'] = str(ms().transformNone(cur[0][0]))
            self.query['lastModificationTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 修改更新时间
            self.query['lastModifierId'] = str(ms().transformNone(cur[0][5]))
            self.query['creationTime'] = cur[0][1].strftime("%Y-%m-%d %H:%M:%S")
            self.query['creatorId'] = str(ms().transformNone(cur[0][2]))
            self.query['whId'] = str(ms().transformNone(cur[0][7]))
            self.query['ownerId'] = str(ms().transformNone(cur[0][10]))
            self.query['supplierId'] = str(ms().transformNone(cur[0][11]))
            self.query['xCode'] = str(ms().transformNone(cur[0][9]))
            self.query['billTypeId'] = str(ms().transformNone(billTypecur[0][0]))  # 修改单据类型
            self.query['xStatus'] = ms().transformNone(cur[0][12])
            self.query['shelvesStatus'] = str(ms().transformNone(cur[0][13]))
            self.query['expectedPkgQuantity'] = float(cur[0][14])
            self.query['receivedPkgQuantity'] = float(cur[0][15])
            self.query['movedPkgQuantity'] = float(cur[0][16])
            self.query['tolocationId'] = str(ms().transformNone(cur[0][17]))
            self.query['relatedBill1'] = str(ms().transformNone(cur[0][50]))
            self.query['relatedBill2'] = str(ms().transformNone(cur[0][51]))
            self.query['relatedBill3'] = str(ms().transformNone(cur[0][52]))
            self.query['orderDate'] = cur[0][49].strftime("%Y-%m-%d")
            self.query['estimateDate'] = "9999-12-31 23:59:59"  # 修改预计到货时间
            self.query['startReceivedDate'] = str(ms().transformNone(cur[0][53]))
            self.query['endReceivedDate'] = str(ms().transformNone(cur[0][46]))
            self.query['fromName'] = str(ms().transformNone(cur[0][48]))
            self.query['contactCountry'] = str(ms().transformNone(cur[0][39]))
            self.query['contactProvince'] = str(ms().transformNone(cur[0][44]))
            self.query['contactCity'] = str(ms().transformNone(cur[0][38]))
            self.query['contactAddress'] = ''  # 修改联系地址为空
            self.query['contactPostcode'] = str(ms().transformNone(cur[0][43]))
            self.query['contactName'] = str(ms().transformNone(cur[0][54]))
            self.query['contactMobile'] = str(ms().transformNone(cur[0][42]))
            self.query['contactTelephone'] = str(ms().transformNone(cur[0][45]))
            self.query['contactFax'] = str(ms().transformNone(cur[0][41]))
            self.query['contactEmail'] = str(ms().transformNone(cur[0][40]))
            self.query['operateStatus'] = str(ms().transformNone(cur[0][18]))
            self.query['erpStatus'] = str(ms().transformNone(cur[0][19]))
            self.query['isOffLine'] = str(ms().transformNone(cur[0][20]))
            self.query['trusteeBy'] = str(ms().transformNone(cur[0][21]))
            self.query['qcBy'] = str(ms().transformNone(cur[0][22]))
            self.query['storekeeper'] = str(ms().transformNone(cur[0][23]))
            self.query['tradingCompany'] = str(ms().transformNone(cur[0][24]))
            self.query['relationCode'] = str(ms().transformNone(cur[0][25]))
            self.query['comments'] = '自动化测试-修改收货单主单据备注信息！'  # 修改备注信息
            self.query['str1'] = '自动化测试-修改扩展字段1'  # 修改扩展字段1
            self.query['str2'] = str(ms().transformNone(cur[0][28]))
            self.query['str3'] = str(ms().transformNone(cur[0][29]))
            self.query['str4'] = str(ms().transformNone(cur[0][30]))
            self.query['str5'] = str(ms().transformNone(cur[0][31]))
            self.query['str6'] = str(ms().transformNone(cur[0][32]))
            self.query['str7'] = str(ms().transformNone(cur[0][33]))
            self.query['str8'] = str(ms().transformNone(cur[0][34]))
            self.query['str9'] = str(ms().transformNone(cur[0][35]))
            self.query['str10'] = str(ms().transformNone(cur[0][36]))
        elif self.case_name == 'updatereceiptOrder_parametersNotnull':  # 从数据库查询状态为打开、没有收货明细的收货单的信息赋值给请求体参数
            self.query['id'] = str(ms().transformNone(cur2[0][0]))
            self.query['creatorId'] = str(ms().transformNone(cur2[0][2]))
            self.query['lastModifierId'] = str(ms().transformNone(cur2[0][5]))
            self.query['lastModificationTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.query['creationTime'] = cur2[0][1].strftime("%Y-%m-%d %H:%M:%S")
            self.query['billTypeId'] = str(ms().transformNone(billTypecur[0][0]))
            self.query['expectedPkgQuantity'] = float(cur2[0][14])
            self.query['receivedPkgQuantity'] = float(cur2[0][15])
            self.query['movedPkgQuantity'] = float(cur2[0][16])
        else:
            self.query['id'] = str(ms().transformNone(cur[0][0]))
            self.query['lastModificationTime'] = cur[0][4].strftime("%Y-%m-%d %H:%M:%S")
            self.query['creationTime'] = cur[0][1].strftime("%Y-%m-%d %H:%M:%S")
            self.query['whId'] = str(ms().transformNone(cur[0][7]))
            self.query['ownerId'] = str(ms().transformNone(cur[0][10]))
            self.query['supplierId'] = str(ms().transformNone(cur[0][11]))
            self.query['xCode'] = str(ms().transformNone(cur[0][9]))
            self.query['billTypeId'] = str(ms().transformNone(cur[0][8]))
            self.query['xStatus'] = ms().transformNone(cur[0][12])
            self.query['shelvesStatus'] = str(ms().transformNone(cur[0][13]))
            self.query['expectedPkgQuantity'] = float(cur[0][14])
            self.query['receivedPkgQuantity'] = float(cur[0][15])
            self.query['movedPkgQuantity'] = float(cur[0][16])
            self.query['tolocationId'] = str(ms().transformNone(cur[0][17]))
            self.query['relatedBill1'] = str(ms().transformNone(cur[0][50]))
            self.query['relatedBill2'] = str(ms().transformNone(cur[0][51]))
            self.query['relatedBill3'] = str(ms().transformNone(cur[0][52]))
            self.query['orderDate'] = cur[0][49].strftime("%Y-%m-%d")
            self.query['estimateDate'] = cur[0][47].strftime("%Y-%m-%d %H:%M:%S")
            self.query['startReceivedDate'] = str(ms().transformNone(cur[0][53]))
            self.query['endReceivedDate'] = str(ms().transformNone(cur[0][46]))
            self.query['fromName'] = str(ms().transformNone(cur[0][48]))
            self.query['contactCountry'] = str(ms().transformNone(cur[0][39]))
            self.query['contactProvince'] = str(ms().transformNone(cur[0][44]))
            self.query['contactCity'] = str(ms().transformNone(cur[0][38]))
            self.query['contactAddress'] = ''  # 修改联系地址为空
            self.query['contactPostcode'] = str(ms().transformNone(cur[0][43]))
            self.query['contactName'] = str(ms().transformNone(cur[0][54]))
            self.query['contactMobile'] = str(ms().transformNone(cur[0][42]))
            self.query['contactTelephone'] = str(ms().transformNone(cur[0][45]))
            self.query['contactFax'] = str(ms().transformNone(cur[0][41]))
            self.query['contactEmail'] = str(ms().transformNone(cur[0][40]))
            self.query['operateStatus'] = str(ms().transformNone(cur[0][18]))
            self.query['erpStatus'] = str(ms().transformNone(cur[0][19]))
            self.query['isOffLine'] = str(ms().transformNone(cur[0][20]))
            self.query['trusteeBy'] = str(ms().transformNone(cur[0][21]))
            self.query['qcBy'] = str(ms().transformNone(cur[0][22]))
            self.query['storekeeper'] = str(ms().transformNone(cur[0][23]))
            self.query['tradingCompany'] = str(ms().transformNone(cur[0][24]))
            self.query['relationCode'] = str(ms().transformNone(cur[0][25]))
            self.query['comments'] = '自动化测试-修改收货单主单据备注信息！'  # 修改备注信息
            self.query['str1'] = '自动化测试-修改扩展字段1'
            self.query['str2'] = str(ms().transformNone(cur[0][28]))
            self.query['str3'] = str(ms().transformNone(cur[0][29]))
            self.query['str4'] = str(ms().transformNone(cur[0][30]))
            self.query['str5'] = str(ms().transformNone(cur[0][31]))
            self.query['str6'] = str(ms().transformNone(cur[0][32]))
            self.query['str7'] = str(ms().transformNone(cur[0][33]))
            self.query['str8'] = str(ms().transformNone(cur[0][34]))
            self.query['str9'] = str(ms().transformNone(cur[0][35]))
            self.query['str10'] = str(ms().transformNone(cur[0][36]))
            if case_name == 'updatereceiptOrder_receiptOrderId_null':
                self.query['id'] = ''
            elif case_name == 'updatereceiptOrder_billTypeId_null':
                self.query['billTypeId'] = ''
            elif case_name == 'updatereceiptOrder_receivedPkgQuantity_null':
                self.query['receivedPkgQuantity'] = ''
            elif case_name == 'updatereceiptOrder_orderDate_notdata':
                self.query['orderDate'] = 'abc'
            elif case_name == 'updatereceiptOrder_contactAddress_overlength':
                self.query['contactAddress'] = '测试联系地址长度测试联系地址长度测试联系地址长度2测试联系地址长度测试联系地址长度测试' \
                                               '联系地址长度2测试联系地址长度测试联系地址长度测试联系地址长度2测试联系地址长度测试联' \
                                               '系地址长度测试联系地址长度2测试联系地址长度测试联系地址长度测试联系地址长度2测试联系' \
                                               '地址长度测试联系地址长度测试联系地址长度2测试联系地址长度测试联系地址长度测试联系地址' \
                                               '长度2测试联系地址长度测试联系地址长度测试联系地址长度2测试联系地址长度测试联系地址长' \
                                               '度测试联系地址长度1测试联系地址长度测试联系地址长度测试联系地址长度22'
            elif case_name == 'updatereceiptOrder_receiptOrderId_error':
                self.query['id'] = uuid.uuid1()
            elif case_name == 'updatereceiptOrder_str1_specialcharacter':
                self.query['str1'] = '「【】±+-×÷∧∨∑∏∪∩∈√⊥∥∠∝≤誇_?*,.;[]()#@$%^!~<>0.99自动化ab'


        # elif case_name == 'updatereceiptOrder_parametersNotnull':
        #     self.query['creator'] = ''
        #     self.query['lastModifier'] = ''
        #     self.query['id'] = str(ms().transformNone(cur[0][0]))
        #     self.query['lastModificationTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #     self.query['lastModifierId'] = ''
        #     self.query['creationTime'] = cur[0][1].strftime("%Y-%m-%d %H:%M:%S")
        #     self.query['creatorId'] = ''
        #     self.query['whId'] = ''
        #     self.query['ownerId'] = ''
        #     self.query['supplierId'] = ''
        #     self.query['xCode'] = ''
        #     self.query['billTypeId'] = str(ms().transformNone(billTypecur[0][0]))
        #     self.query['xStatus'] = ''
        #     self.query['shelvesStatus'] = ''
        #     self.query['expectedPkgQuantity'] = float(cur[0][14])
        #     self.query['receivedPkgQuantity'] = float(cur[0][15])
        #     self.query['movedPkgQuantity'] = float(cur[0][16])
        #     self.query['tolocationId'] = ''
        #     self.query['relatedBill1'] = ''
        #     self.query['relatedBill2'] = ''
        #     self.query['relatedBill3'] = ''
        #     self.query['orderDate'] = ''
        #     self.query['estimateDate'] = ''
        #     self.query['startReceivedDate'] = ''
        #     self.query['endReceivedDate'] = ''
        #     self.query['fromName'] = ''
        #     self.query['contactCountry'] = ''
        #     self.query['contactProvince'] = ''
        #     self.query['contactCity'] = ''
        #     self.query['contactAddress'] = ''
        #     self.query['contactPostcode'] = ''
        #     self.query['contactName'] = ''
        #     self.query['contactMobile'] = ''
        #     self.query['contactTelephone'] = ''
        #     self.query['contactFax'] = ''
        #     self.query['contactEmail'] = ''
        #     self.query['operateStatus'] = ''
        #     self.query['erpStatus'] = ''
        #     self.query['isOffLine'] = ''
        #     self.query['trusteeBy'] = ''
        #     self.query['qcBy'] = ''
        #     self.query['storekeeper'] = ''
        #     self.query['tradingCompany'] = ''
        #     self.query['relationCode'] = ''
        #     self.query['comments'] = ''
        #     self.query['str1'] = ''
        #     self.query['str2'] = ''
        #     self.query['str3'] = ''
        #     self.query['str4'] = ''
        #     self.query['str5'] = ''
        #     self.query['str6'] = ''
        #     self.query['str7'] = ''
        #     self.query['str8'] = ''
        #     self.query['str9'] = ''
        #     self.query['str10'] = ''

        self.query = str(self.query).encode('utf-8')

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testupdatereceiptOrder(self):
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
            if self.case_name == 'updatereceiptOrder':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                try:
                    # 断言接口返回的信息中的'xStatus'值是否是’OPEN‘，否则抛出断言错误
                    self.assertEqual("OPEN", info['xStatus'])
                except AssertionError as e:
                    print('接口未正常返回数据！', e)
                    raise AssertionError
                else:
                    self.query = eval(self.query)
                    # 从数据库查询刚刚新建的收货单信息
                    ReceiptOrder = ms().get_all(
                        ms().ExecQuery("SELECT BillTypeId, OwnerId, SupplierId, XStatus, ShelvesStatus, "
                                       "ExpectedPkgQuantity, Comments, Str1, Str2, Str3, Str4, ContactAddress, "
                                       "ContactMobile, OrderDate, EstimateDate, ContactName, FromName, ContactPostcode "
                                       "FROM WMS.ReceiptOrder WHERE XCode= '%s'" % info['xCode']))
                    # 断言接口传参的数据与接口返回的数据是否一致，接口传参的数据与新建的收货单的信息时是否一致，任一一个不相等，断言失败

                    self.assertFalse(any(x for x in (self.assertEqual(self.query['id'], info['id'],
                                                                      '修改收货单，接口返回的收货单id与传参的收货单id不一致！'),
                                                     self.assertEqual(self.query['ownerId'], info['ownerId'],
                                                                      '修改收货单，接口返回的货主id与传参的货主id不一致！'),
                                                     self.assertEqual(self.query['supplierId'], info['supplierId'],
                                                                      '修改收货单，接口返回的供应商id与传参的供应商id不一致！'),
                                                     self.assertEqual(self.query['billTypeId'], info['billTypeId'],
                                                                      '修改收货单，接口返回的单据类型id与传参的单据类型id不一致！'),
                                                     self.assertEqual('OPEN', info['xStatus'],
                                                                      '修改收货单，接口返回的单据状态与接口定义的默认返回的单据状态不一致！'),
                                                     self.assertEqual(self.query['expectedPkgQuantity'], info['expectedPkgQuantity'],
                                                                      '修改收货单，接口返回的期望数量与传参的期望数量不一致！'),
                                                     self.assertEqual(self.query['receivedPkgQuantity'], info['receivedPkgQuantity'],
                                                                      '修改收货单，接口返回的收货数量与传参的收货数量不一致！'),
                                                     self.assertEqual(self.query['movedPkgQuantity'], info['movedPkgQuantity'],
                                                                      '修改收货单，接口返回的移动数量与传参的移动数量不一致！'),
                                                     self.assertEqual(self.query['relatedBill1'], info['relatedBill1'],
                                                                      '修改收货单，接口返回的相关单据与传参的相关单据不一致！'),
                                                     self.assertEqual(
                                                         datetime.datetime.strptime(self.query['orderDate'],
                                                                                    '%Y-%m-%d'),
                                                         datetime.datetime.strptime(info['orderDate'],
                                                                                    '%Y-%m-%dT%H:%M:%S'),
                                                         '修改收货单，接口返回的订单日期与传参的订单日期不一致！'),
                                                     self.assertEqual(
                                                         datetime.datetime.strptime(self.query['estimateDate'],
                                                                                    '%Y-%m-%d %H:%M:%S'),
                                                         datetime.datetime.strptime(info['estimateDate'],
                                                                                    '%Y-%m-%dT%H:%M:%S'),
                                                         '修改收货单，接口传参的预计到货日期与接口返回的预计到货日期不一致！'),
                                                     self.assertEqual(self.query['fromName'], info['fromName'],
                                                                      '修改收货单，接口传参的发货人与接口返回的发货人日期不一致！'),
                                                     self.assertEqual(self.query['contactAddress'],
                                                                      info['contactAddress'],
                                                                      '修改收货单，接口传参的联系人地址与接口返回的联系人地址不一致！'),
                                                     self.assertEqual(self.query['contactPostcode'],
                                                                      info['contactPostcode'],
                                                                      '修改收货单，接口传参的邮编与接口返回的邮编不一致！'),
                                                     self.assertEqual(self.query['contactName'], info['contactName'],
                                                                      '修改收货单，接口传参的联系人姓名与接口返回的联系人姓名不一致！'),
                                                     self.assertEqual(self.query['contactMobile'],
                                                                      info['contactMobile'],
                                                                      '修改收货单，接口传参的联系人电话与接口返回的联系人电话不一致！'),
                                                     self.assertEqual(self.query['comments'], info['comments'],
                                                                      '修改收货单，接口传参的备注信息与接口返回的备注信息不一致！'),
                                                     self.assertEqual(self.query['str1'], info['str1'],
                                                                      '修改收货单，接口传参的扩展字段1与接口返回的扩展字段1不一致！'),
                                                     self.assertEqual(self.query['str2'], info['str2'],
                                                                      '修改收货单，接口传参的扩展字段2与接口返回的扩展字段2不一致！'),
                                                     self.assertEqual(self.query['str3'], info['str3'],
                                                                      '修改收货单，接口传参的扩展字段3与接口返回的扩展字段3不一致！'),
                                                     self.assertEqual(self.query['str4'], info['str4'],
                                                                      '修改收货单，接口传参的扩展字段4与接口返回的扩展字段4不一致！'),
                                                     self.assertEqual(self.query['ownerId'], str(ReceiptOrder[0][1]),
                                                                      '修改收货单，接口传参的货主id与修改后的收货单的货主id不一致！'),
                                                     self.assertEqual(self.query['supplierId'], str(ReceiptOrder[0][2]),
                                                                      '修改收货单，接口传参的供应商id与修改后的收货单的供应商id不一致！'),
                                                     self.assertEqual(self.query['billTypeId'], str(ReceiptOrder[0][0]),
                                                                      '修改收货单，接口传参的单据类型id与修改后的收货单的单据类型id不一致！'),
                                                     self.assertEqual('OPEN', ReceiptOrder[0][3],
                                                                      '修改收货单，接口传参的单据状态与修改后的收货单的单据状态不一致！'),
                                                     self.assertEqual('UNPUTAWAY', ReceiptOrder[0][4],
                                                                      '修改收货单，接口传参的上架状态与修改后的收货单的上架状态不一致！'),
                                                     self.assertEqual(self.query['expectedPkgQuantity'], float(ReceiptOrder[0][5]),
                                                                      '修改收货单，接口传参的期望数量与修改后的收货单的期望数量不一致！'),
                                                     self.assertEqual(
                                                         datetime.datetime.strptime(self.query['orderDate'],
                                                                                    '%Y-%m-%d'),
                                                         ReceiptOrder[0][13],
                                                         '修改收货单，接口传参的订单日期与修改后的收货单的订单日期不一致！'),
                                                     self.assertEqual(
                                                         datetime.datetime.strptime(self.query['estimateDate'],
                                                                                    '%Y-%m-%d %H:%M:%S'),
                                                         ReceiptOrder[0][14],
                                                         '修改收货单，接口传参的到货日期与修改后的收货单的到货日期不一致！'),
                                                     self.assertEqual(self.query['fromName'], ReceiptOrder[0][16],
                                                                      '修改收货单，接口传参的发货人姓名与修改后的收货单的发货人姓名不一致！'),
                                                     self.assertEqual(self.query['contactAddress'],
                                                                      ReceiptOrder[0][11],
                                                                      '修改收货单，接口传参的联系地址与修改后的收货单的联系地址不一致！'),
                                                     self.assertEqual(self.query['contactPostcode'],
                                                                      ReceiptOrder[0][17],
                                                                      '修改收货单，接口传参的邮编与修改后的收货单的邮编不一致！'),
                                                     self.assertEqual(self.query['contactName'], ReceiptOrder[0][15],
                                                                      '修改收货单，接口传参的联系人与修改后的收货单的联系人不一致！'),
                                                     self.assertEqual(self.query['contactMobile'],
                                                                      ReceiptOrder[0][12],
                                                                      '修改收货单，接口传参的联系电话与修改后的收货单的联系电话不一致！'),
                                                     self.assertEqual(self.query['comments'], ReceiptOrder[0][6],
                                                                      '修改收货单，接口传参的备注信息与修改后的收货单的备注信息不一致！'),
                                                     self.assertEqual(self.query['str1'], ReceiptOrder[0][7],
                                                                      '修改收货单，接口传参的扩展字段1与修改后的收货单的扩展字段1不一致！'),
                                                     self.assertEqual(self.query['str2'], ReceiptOrder[0][8],
                                                                      '修改收货单，接口传参的扩展字段2与修改后的收货单的扩展字段2不一致！'),
                                                     self.assertEqual(self.query['str3'], ReceiptOrder[0][9],
                                                                      '修改收货单，接口传参的扩展字段3与修改后的收货单的扩展字段3不一致！'),
                                                     self.assertEqual(self.query['str4'], ReceiptOrder[0][10],
                                                                      '修改收货单，接口传参的扩展字段4与修改后的收货单的扩展字段4不一致！')
                                                     )))
            elif self.case_name == 'updatereceiptOrder_parametersNotnull':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                try:
                    # 判断断言接口返回的信息中的'ReceiptOrderId'值是否与接口调用时的传参一致，否则抛出断言错误
                    self.assertEqual(self.query['id'], info['id'])
                except AssertionError as e:
                    print('接口未正常返回数据！', e)
                    raise AssertionError
                else:
                    # 从数据库查询刚刚新建的收货单信息
                    ReceiptOrder = ms().get_all(
                        ms().ExecQuery("SELECT BillTypeId, OwnerId, SupplierId, XStatus, ShelvesStatus, "
                                       "ExpectedPkgQuantity, Comments, Str1, Str2, Str3, Str4, ContactAddress, "
                                       "ContactMobile, OrderDate, EstimateDate, ContactName, FromName, ContactPostcode "
                                       "FROM WMS.ReceiptOrder WHERE id= '%s'" % info['id']))
                    # 断言接口传参的数据与接口返回的数据是否一致，接口传参的数据与新建的收货单的信息时是否一致，任一一个不相等，断言失败
                    self.assertFalse(any(x for x in (self.assertEqual(self.query['id'], info['id'],
                                                                      '修改收货单，接口返回的收货单id与传参的收货单id不一致！'),
                                                     self.assertEqual(None, info['ownerId'],
                                                                      '修改收货单，接口返回的货主id与传参的货主id不一致！'),
                                                     self.assertEqual(None, info['supplierId'],
                                                                      '修改收货单，接口返回的供应商id与传参的供应商id不一致！'),
                                                     self.assertEqual(self.query['billTypeId'], info['billTypeId'],
                                                                      '修改收货单，接口返回的单据类型id与传参的单据类型id不一致！'),
                                                     self.assertEqual('', info['xStatus'],
                                                                      '修改收货单，接口返回的单据状态与接口定义的默认返回的单据状态不一致！'),
                                                     self.assertEqual(self.query['expectedPkgQuantity'], info['expectedPkgQuantity'],
                                                                      '修改收货单，接口返回的期望数量与传参的期望数量不一致！'),
                                                     self.assertEqual(self.query['receivedPkgQuantity'], info['receivedPkgQuantity'],
                                                                      '修改收货单，接口返回的收货数量与传参的收货数量不一致！'),
                                                     self.assertEqual(self.query['movedPkgQuantity'], info['movedPkgQuantity'],
                                                                      '修改收货单，接口返回的移动数量与传参的移动数量不一致！'),
                                                     self.assertEqual(self.query['relatedBill1'], info['relatedBill1'],
                                                                      '修改收货单，接口返回的相关单据与传参的相关单据不一致！'),
                                                     self.assertEqual(None, info['orderDate'],
                                                                      '修改收货单，接口返回的订单日期与传参的订单日期不一致！'),
                                                     self.assertEqual(None, info['estimateDate'],
                                                                      '修改收货单，接口传参的预计到货日期与接口返回的预计到货日期不一致！'),
                                                     self.assertEqual(self.query['fromName'], info['fromName'],
                                                                      '修改收货单，接口传参的发货人与接口返回的发货人日期不一致！'),
                                                     self.assertEqual(self.query['contactAddress'],
                                                                      info['contactAddress'],
                                                                      '修改收货单，接口传参的联系人地址与接口返回的联系人地址不一致！'),
                                                     self.assertEqual(self.query['contactPostcode'],
                                                                      info['contactPostcode'],
                                                                      '修改收货单，接口传参的邮编与接口返回的邮编不一致！'),
                                                     self.assertEqual(self.query['contactName'], info['contactName'],
                                                                      '修改收货单，接口传参的联系人姓名与接口返回的联系人姓名不一致！'),
                                                     self.assertEqual(self.query['contactMobile'],
                                                                      info['contactMobile'],
                                                                      '修改收货单，接口传参的联系人电话与接口返回的联系人电话不一致！'),
                                                     self.assertEqual(self.query['comments'], info['comments'],
                                                                      '修改收货单，接口传参的备注信息与接口返回的备注信息不一致！'),
                                                     self.assertEqual(self.query['str1'], info['str1'],
                                                                      '修改收货单，接口传参的扩展字段1与接口返回的扩展字段1不一致！'),
                                                     self.assertEqual(self.query['str2'], info['str2'],
                                                                      '修改收货单，接口传参的扩展字段2与接口返回的扩展字段2不一致！'),
                                                     self.assertEqual(self.query['str3'], info['str3'],
                                                                      '修改收货单，接口传参的扩展字段3与接口返回的扩展字段3不一致！'),
                                                     self.assertEqual(self.query['str4'], info['str4'],
                                                                      '修改收货单，接口传参的扩展字段4与接口返回的扩展字段4不一致！'),
                                                     self.assertEqual(None, ReceiptOrder[0][1],
                                                                      '修改收货单，接口传参的货主id与修改后的收货单的货主id不一致！'),
                                                     self.assertEqual(None, ReceiptOrder[0][2],
                                                                      '修改收货单，接口传参的供应商id与修改后的收货单的供应商id不一致！'),
                                                     self.assertEqual(self.query['billTypeId'], str(ReceiptOrder[0][0]),
                                                                      '修改收货单，接口传参的单据类型id与修改后的收货单的单据类型id不一致！'),
                                                     self.assertEqual('', ReceiptOrder[0][3],
                                                                      '修改收货单，接口传参的单据状态与修改后的收货单的单据状态不一致！'),
                                                     self.assertEqual(self.query['expectedPkgQuantity'], float(ReceiptOrder[0][5]),
                                                                      '修改收货单，接口传参的期望数量与修改后的收货单的期望数量不一致！'),
                                                     self.assertEqual(None, ReceiptOrder[0][13],
                                                                      '修改收货单，接口传参的订单日期与修改后的收货单的订单日期不一致！'),
                                                     self.assertEqual(None, ReceiptOrder[0][14],
                                                                      '修改收货单，接口传参的到货日期与修改后的收货单的到货日期不一致！'),
                                                     self.assertEqual(self.query['fromName'], ReceiptOrder[0][16],
                                                                      '修改收货单，接口传参的发货人姓名与修改后的收货单的发货人姓名不一致！'),
                                                     self.assertEqual(self.query['contactAddress'],
                                                                      ReceiptOrder[0][11],
                                                                      '修改收货单，接口传参的联系地址与修改后的收货单的联系地址不一致！'),
                                                     self.assertEqual(self.query['contactPostcode'],
                                                                      ReceiptOrder[0][17],
                                                                      '修改收货单，接口传参的邮编与修改后的收货单的邮编不一致！'),
                                                     self.assertEqual(self.query['contactName'], ReceiptOrder[0][15],
                                                                      '修改收货单，接口传参的联系人与修改后的收货单的联系人不一致！'),
                                                     self.assertEqual(self.query['contactMobile'],
                                                                      ReceiptOrder[0][12],
                                                                      '修改收货单，接口传参的联系电话与修改后的收货单的联系电话不一致！'),
                                                     self.assertEqual(self.query['comments'], ReceiptOrder[0][6],
                                                                      '修改收货单，接口传参的备注信息与修改后的收货单的备注信息不一致！'),
                                                     self.assertEqual(self.query['str1'], ReceiptOrder[0][7],
                                                                      '修改收货单，接口传参的扩展字段1与修改后的收货单的扩展字段1不一致！'),
                                                     self.assertEqual(self.query['str2'], ReceiptOrder[0][8],
                                                                      '修改收货单，接口传参的扩展字段2与修改后的收货单的扩展字段2不一致！'),
                                                     self.assertEqual(self.query['str3'], ReceiptOrder[0][9],
                                                                      '修改收货单，接口传参的扩展字段3与修改后的收货单的扩展字段3不一致！'),
                                                     self.assertEqual(self.query['str4'], ReceiptOrder[0][10],
                                                                      '修改收货单，接口传参的扩展字段4与修改后的收货单的扩展字段4不一致！')
                                                     )))
            elif self.case_name == 'updatereceiptOrder_receiptOrderId_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('收货单id为空！', info['error'][
                    'message'], '修改收货单主单据，收货单id为空时，接口没有正确的对应处理机制！')
            elif self.case_name == 'updatereceiptOrder_billTypeId_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('单据类型id为空！', info['error'][
                    'message'], '修改收货单主单据，单据类型id为空时，接口没有正确的对应处理机制！')
            elif self.case_name == 'updatereceiptOrder_receivedPkgQuantity_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('收货数量为空！', info['error'][
                    'message'], '修改收货单主单据，收货数量为空时，接口没有正确的对应处理机制！')
            elif self.case_name == 'updatereceiptOrder_orderDate_notdata':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('订单日期值不是日期类型！', info['error'][
                    'message'], '修改收货单主单据，orderDate参数不是日期类型时，接口没有正确的对应处理机制！')
            elif self.case_name == 'updatereceiptOrder_contactAddress_overlength':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('联系地址字符长度过长！', info['error'][
                    'message'], '修改收货单主单据，contactAddress参数长度超数据库字段长度时，接口没有正确的对应处理机制！')
            elif self.case_name == 'updatereceiptOrder_receiptOrderId_error':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('收货单id错误！', info['error'][
                    'message'], '修改收货单主单据，收货单id错误时，接口没有正确的对应处理机制！')
            elif self.case_name == 'updatereceiptOrder_str1_specialcharacter':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                self.assertEqual(self.query['str1'], info['str1'], '修改收货单主单据，接口传参的str1与接口返回的str1不一致！')


if __name__ == '__main__':
    unittest.main()



