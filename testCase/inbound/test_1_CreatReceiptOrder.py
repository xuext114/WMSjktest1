#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新建收货主单据，从参数必填校验、类型校验、格式校验、业务校验方面进行进行测试验证
"""

import ast
import unittest
from common.configHttp import RunMain
import paramunittest
from testFile import geturlParams
# import urllib.parse
from testFile import readExcel
from testFile.readyaml import readyaml
from common.configDb import MSSQL as ms
import datetime
from testFile.readSql import get_sql
import time
import uuid


url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'creatreceiptOrder')

@paramunittest.parametrized(*casexls)
class testcreatReceiptOrder(unittest.TestCase):
    def setParameters(self, case_name, case_name_ch, method, path, query):
        self.case_name = str(case_name)
        self.case_name_ch = str(case_name_ch)
        self.path = str(path)
        self.query = ast.literal_eval(str(query))
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()

        self.query['ownerId'] = str(ms().getvalue('WMS.Orgnization', 'ownerId')[0][0])
        self.query['supplierId'] = str(ms().getvalue('WMS.Orgnization', 'supplierId')[0][0])
        self.query['billTypeId'] = str(ms().getvalue('WMS.BillType', 'billTypeId')[0][0])

        # 订单日期设定为当前日前5天
        self.query['orderDate'] = str((datetime.datetime.now() - datetime.timedelta(days=5)).strftime('%Y-%m-%d'))
        # 预计到货日期设定为当前日前后5天
        self.query['estimateDate'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        if self.case_name == 'creatreceiptOrder_billTypeId&PkgQuantity_notnull':
            self.query['ownerId'] = ''
            self.query['supplierId'] = ''
            self.query['orderDate'] = ''
            self.query['estimateDate'] = ''
        elif self.case_name == 'creatreceiptOrder_billTypeId_null':
            self.query['billTypeId'] = ''
        # elif self.case_name == 'creatreceiptOrder_ownerId_null':
        #     self.query['ownerId'] = ''
        elif self.case_name == 'creatreceiptOrder_ownerId_notuuid':
            self.query['ownerId'] = '3fa85f64'
        elif self.case_name == 'creatreceiptOrder_supplierId_notuuid':
            self.query['supplierId'] = '3fa85f64'
        elif self.case_name == 'creatreceiptOrder_billTypeId_notuuid':
            self.query['billTypeId'] = '3fa85f64'
        elif self.case_name == 'creatreceiptOrder_ownerId_error':
            self.query['ownerId'] = uuid.uuid1()
        elif self.case_name == 'creatreceiptOrder_billTypeId_error':
            self.query['billTypeId'] = uuid.uuid1()

        self.query = str(self.query).encode('utf-8')

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testcreatReceiptOrder(self):
        self.checkResult()

    def tearDown(self):
        print('测试结束...')
        ms().closeDB()  # 关闭数据库连接

    def checkResult(self):
        new_url = url + ':44349' + self.path
        # data1 = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(new_url).query))
        try:
            info = RunMain().run_main(self.method, headers=self.headers, url=new_url, data=self.query)
        except Exception as e:
            print('接口调用异常：', e)
            raise Exception
        else:
            if self.case_name == 'creatreceiptOrder':
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
                    self.assertFalse(any(x for x in (self.assertEqual(self.query['ownerId'], info['ownerId'],
                                                                      '接口传参的货主id与接口返回的货主id不一致！'),
                                                     self.assertEqual(self.query['supplierId'], info['supplierId'],
                                                                      '接口传参的供应商id与接口返回的供应商id不一致！'),
                                                     self.assertEqual(self.query['billTypeId'], info['billTypeId'],
                                                                      '接口传参的单据类型id与接口返回的单据类型id不一致！'),
                                                     self.assertEqual('OPEN', info['xStatus'],
                                                                      '接口传参的单据状态与接口返回的单据状态不一致！'),
                                                     self.assertEqual('UNPUTAWAY', info['shelvesStatus'],
                                                                      '接口传参的上架状态与接口返回的上架状态不一致！'),
                                                     self.assertEqual(0.0, info['expectedPkgQuantity'],
                                                                      '接口传参的期望数量与接口返回的期望数量不一致！'),
                                                     self.assertEqual(0.0, info['receivedPkgQuantity'],
                                                                      '接口传参的收货数量与接口返回的收货数量不一致！'),
                                                     self.assertEqual(0.0, info['movedPkgQuantity'],
                                                                      '接口传参的移动数量与接口返回的移动数量不一致！'),
                                                     self.assertEqual(self.query['relatedBill1'], info['relatedBill1'],
                                                                      '接口传参的相关单据与接口返回的相关单据不一致！'),
                                                     self.assertEqual(datetime.datetime.strptime(self.query['orderDate'], '%Y-%m-%d'),
                                                                      datetime.datetime.strptime(info['orderDate'], '%Y-%m-%dT%H:%M:%S'),
                                                                      '接口传参的订单日期与接口返回的订单日期不一致！'),
                                                     self.assertEqual(datetime.datetime.strptime(self.query['estimateDate'], '%Y-%m-%d'),
                                                                      datetime.datetime.strptime(info['estimateDate'], '%Y-%m-%dT%H:%M:%S'),
                                                                      '接口传参的收货日期与接口返回的收货日期不一致！'),
                                                     self.assertEqual(self.query['fromName'], info['fromName'],
                                                                      '接口传参的发货人与接口返回的发货人不一致！'),
                                                     self.assertEqual(self.query['contactAddress'],
                                                                      info['contactAddress'],
                                                                      '接口传参的联系地址与接口返回的联系地址不一致！'),
                                                     self.assertEqual(self.query['contactPostcode'],
                                                                      info['contactPostcode'],
                                                                      '接口传参的邮编与接口返回的邮编不一致！'),
                                                     self.assertEqual(self.query['contactName'], info['contactName'],
                                                                      '接口传参的联系人与接口返回的联系人不一致！'),
                                                     self.assertEqual(self.query['contactMobile'], info['contactMobile'],
                                                                      '接口传参的联系电话与接口返回的联系电话不一致！'),
                                                     self.assertEqual(self.query['comments'], info['comments'],
                                                                      '接口传参的备注信息与接口返回的备注信息不一致！'),
                                                     self.assertEqual(self.query['str1'], info['str1'],
                                                                      '接口传参的扩展属性1与接口返回的扩展属性1不一致！'),
                                                     self.assertEqual(self.query['str2'], info['str2'],
                                                                      '接口传参的扩展属性2与接口返回的扩展属性2不一致！'),
                                                     self.assertEqual(self.query['str3'], info['str3'],
                                                                      '接口传参的扩展属性3与接口返回的扩展属性3不一致！'),
                                                     self.assertEqual(self.query['str4'], info['str4'],
                                                                      '接口传参的扩展属性4与接口返回的扩展属性4不一致！'),
                                                     self.assertEqual(self.query['ownerId'], str(ReceiptOrder[0][1]),
                                                                      '接口传参的货主ID与新建的收货单的货主ID不一致！'),
                                                     self.assertEqual(self.query['supplierId'], str(ReceiptOrder[0][2]),
                                                                      '接口传参的供应商ID与新建的收货单的供应商ID不一致！'),
                                                     self.assertEqual(self.query['billTypeId'], str(ReceiptOrder[0][0]),
                                                                      '接口传参的单据类型ID与新建的收货单的单据类型ID不一致！'),
                                                     self.assertEqual('OPEN', ReceiptOrder[0][3],
                                                                      '接口传参的单据状态与新建的收货单的单据状态不一致！'),
                                                     self.assertEqual('UNPUTAWAY', ReceiptOrder[0][4],
                                                                      '接口传参的上架状态与新建的收货单的上架状态不一致！'),
                                                     self.assertEqual(0.0, ReceiptOrder[0][5],
                                                                      '接口传参的期望数量与新建的收货单的期望数量不一致！'),
                                                     self.assertEqual(datetime.datetime.strptime(self.query['orderDate'], '%Y-%m-%d'),
                                                                      ReceiptOrder[0][13],
                                                                      '接口传参的订单日期与新建的收货单的订单日期不一致！'),
                                                     self.assertEqual(datetime.datetime.strptime(self.query['estimateDate'], '%Y-%m-%d'),
                                                                      ReceiptOrder[0][14],
                                                                      '接口传参的到货日期与新建的收货单的到货日期不一致！'),
                                                     self.assertEqual(self.query['fromName'], ReceiptOrder[0][16],
                                                                      '接口传参的发货人与新建的收货单的发货人不一致！'),
                                                     self.assertEqual(self.query['contactAddress'],
                                                                      ReceiptOrder[0][11],
                                                                      '接口传参的联系地址与新建的收货单的联系地址不一致！'),
                                                     self.assertEqual(self.query['contactPostcode'],
                                                                      ReceiptOrder[0][17],
                                                                      '接口传参的邮编与新建的收货单的邮编不一致！'),
                                                     self.assertEqual(self.query['contactName'], ReceiptOrder[0][15],
                                                                      '接口传参的联系人与新建的收货单的联系人不一致！'),
                                                     self.assertEqual(self.query['contactMobile'],
                                                                      ReceiptOrder[0][12],
                                                                      '接口传参的联系电话与新建的收货单的联系电话不一致！'),
                                                     self.assertEqual(self.query['comments'], ReceiptOrder[0][6],
                                                                      '接口传参的备注信息与新建的收货单的备注信息不一致！'),
                                                     self.assertEqual(self.query['str1'], ReceiptOrder[0][7],
                                                                      '接口传参的扩展属性1与新建的收货单的扩展属性1不一致！'),
                                                     self.assertEqual(self.query['str2'], ReceiptOrder[0][8],
                                                                      '接口传参的扩展属性2与新建的收货单的扩展属性2不一致！'),
                                                     self.assertEqual(self.query['str3'], ReceiptOrder[0][9],
                                                                      '接口传参的扩展属性3与新建的收货单的扩展属性3不一致！'),
                                                     self.assertEqual(self.query['str4'], ReceiptOrder[0][10],
                                                                      '接口传参的扩展属性4与新建的收货单的扩展属性4不一致！')
                                                     )))

            elif self.case_name == 'creatreceiptOrder_billTypeId&PkgQuantity_notnull':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                # 将请求体转换为字典格式
                self.query = eval(self.query)
                try:
                    # 判断断言接口返回的信息中的'billTypeId'值是否与接口调用时的传参一致，否则抛出断言错误
                    self.assertEqual(self.query['billTypeId'], info['billTypeId'])
                except AssertionError as e:
                    print('接口返回数据不正确：', e)
                    raise AssertionError
                else:
                    # 从数据库查询刚刚新建的收货单信息
                    ReceiptOrder = ms().get_all(
                        ms().ExecQuery("SELECT BillTypeId, OwnerId, SupplierId, XStatus, ShelvesStatus, "
                                       "ExpectedPkgQuantity, Comments, Str1, Str2, Str3, Str4, ContactAddress, "
                                       "ContactMobile, OrderDate, EstimateDate, ContactName, FromName, ContactPostcode "
                                       "FROM WMS.ReceiptOrder WHERE XCode= '%s'" % info['xCode']))
                    # 断言接口传参的数据与接口返回的数据是否一致，接口传参的数据与新建的收货单的信息时是否一致，任一一个不相等，断言失败
                    self.assertFalse(any(x for x in (self.assertEqual(None, info['ownerId'],
                                                                      '接口传参的货主id与接口返回的货主id不一致！'),
                                                     self.assertEqual(None, info['supplierId'],
                                                                      '接口传参的供应商id与接口返回的供应商id不一致！'),
                                                     self.assertEqual(self.query['billTypeId'], info['billTypeId'],
                                                                      '接口传参的单据类型id与接口返回的单据类型id不一致！'),
                                                     self.assertEqual('OPEN', info['xStatus'],
                                                                      '接口调用xStatus参数为空时，接口返回的单据状态应默认为OPEN！'),
                                                     self.assertEqual('UNPUTAWAY', info['shelvesStatus'],
                                                                      '接口调用shelvesStatus参数为空时，接口返回的上架状态应默认为UNPUTAWAY！'),
                                                     self.assertEqual(0.0, info['expectedPkgQuantity'],
                                                                      '接口传参的期望数量与接口返回的期望数量不一致！'),
                                                     self.assertEqual(0.0, info['receivedPkgQuantity'],
                                                                      '接口传参的收货数量与接口返回的收货数量不一致！'),
                                                     self.assertEqual(0.0, info['movedPkgQuantity'],
                                                                      '接口传参的移动数量与接口返回的移动数量不一致！'),
                                                     self.assertEqual(self.query['relatedBill1'], info['relatedBill1'],
                                                                      '接口传参的相关单据与接口返回的相关单据不一致！'),
                                                     self.assertEqual(None, info['orderDate'],
                                                                      '接口传参的订单日期与接口返回的订单日期不一致！'),
                                                     self.assertEqual(None, info['estimateDate'],
                                                                      '接口传参的收货日期与接口返回的收货日期不一致！'),
                                                     self.assertEqual(self.query['fromName'], info['fromName'],
                                                                      '接口传参的发货人与接口返回的发货人不一致！'),
                                                     self.assertEqual(self.query['contactAddress'],
                                                                      info['contactAddress'],
                                                                      '接口传参的联系地址与接口返回的联系地址不一致！'),
                                                     self.assertEqual(self.query['contactPostcode'],
                                                                      info['contactPostcode'],
                                                                      '接口传参的邮编与接口返回的邮编不一致！'),
                                                     self.assertEqual(self.query['contactName'], info['contactName'],
                                                                      '接口传参的联系人与接口返回的联系人不一致！'),
                                                     self.assertEqual(self.query['contactMobile'],
                                                                      info['contactMobile'],
                                                                      '接口传参的联系电话与接口返回的联系电话不一致！'),
                                                     self.assertEqual(self.query['comments'], info['comments'],
                                                                      '接口传参的备注信息与接口返回的备注信息不一致！'),
                                                     self.assertEqual(self.query['str1'], info['str1'],
                                                                      '接口传参的扩展属性1与接口返回的扩展属性1不一致！'),
                                                     self.assertEqual(self.query['str2'], info['str2'],
                                                                      '接口传参的扩展属性2与接口返回的扩展属性2不一致！'),
                                                     self.assertEqual(self.query['str3'], info['str3'],
                                                                      '接口传参的扩展属性3与接口返回的扩展属性3不一致！'),
                                                     self.assertEqual(self.query['str4'], info['str4'],
                                                                      '接口传参的扩展属性4与接口返回的扩展属性4不一致！'),
                                                     self.assertEqual(None, str(ReceiptOrder[0][1]),
                                                                      '接口传参的货主ID与新建的收货单的货主ID不一致！'),
                                                     self.assertEqual(None, str(ReceiptOrder[0][2]),
                                                                      '接口传参的供应商ID与新建的收货单的供应商ID不一致！'),
                                                     self.assertEqual(self.query['billTypeId'], str(ReceiptOrder[0][0]),
                                                                      '接口传参的单据类型ID与新建的收货单的单据类型ID不一致！'),
                                                     self.assertEqual('OPEN', ReceiptOrder[0][3],
                                                                      '接口调用xStatus参数为空时，接口返回的单据状态应默认为OPEN！'),
                                                     self.assertEqual('UNPUTAWAY', ReceiptOrder[0][4],
                                                                      '接口调用shelvesStatus参数为空时，接口返回的上架状态应默认为UNPUTAWAY！'),
                                                     self.assertEqual(0.0, ReceiptOrder[0][5],
                                                                      '接口传参的期望数量与新建的收货单的期望数量不一致！'),
                                                     self.assertEqual(None, ReceiptOrder[0][13],
                                                                      '接口传参的订单日期与新建的收货单的订单日期不一致！'),
                                                     self.assertEqual(None, ReceiptOrder[0][14],
                                                                      '接口传参的到货日期与新建的收货单的到货日期不一致！'),
                                                     self.assertEqual(self.query['fromName'], ReceiptOrder[0][16],
                                                                      '接口传参的发货人与新建的收货单的发货人不一致！'),
                                                     self.assertEqual(self.query['contactAddress'],
                                                                      ReceiptOrder[0][11],
                                                                      '接口传参的联系地址与新建的收货单的联系地址不一致！'),
                                                     self.assertEqual(self.query['contactPostcode'],
                                                                      ReceiptOrder[0][17],
                                                                      '接口传参的邮编与新建的收货单的邮编不一致！'),
                                                     self.assertEqual(self.query['contactName'], ReceiptOrder[0][15],
                                                                      '接口传参的联系人与新建的收货单的联系人不一致！'),
                                                     self.assertEqual(self.query['contactMobile'],
                                                                      ReceiptOrder[0][12],
                                                                      '接口传参的联系电话与新建的收货单的联系电话不一致！'),
                                                     self.assertEqual(self.query['comments'], ReceiptOrder[0][6],
                                                                      '接口传参的备注信息与新建的收货单的备注信息不一致！'),
                                                     self.assertEqual(self.query['str1'], ReceiptOrder[0][7],
                                                                      '接口传参的扩展属性1与新建的收货单的扩展属性1不一致！'),
                                                     self.assertEqual(self.query['str2'], ReceiptOrder[0][8],
                                                                      '接口传参的扩展属性2与新建的收货单的扩展属性2不一致！'),
                                                     self.assertEqual(self.query['str3'], ReceiptOrder[0][9],
                                                                      '接口传参的扩展属性3与新建的收货单的扩展属性3不一致！'),
                                                     self.assertEqual(self.query['str4'], ReceiptOrder[0][10],
                                                                      '接口传参的扩展属性4与新建的收货单的扩展属性4不一致！')
                                                     )))

            elif self.case_name == 'creatreceiptOrder_billTypeId_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('单据类型必填！', info['error']['message'], '缺少必填差参数billTypeId时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_expectedPkgQuantity_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('期望数量必填！', info['error']['message'], '缺少必填差参数expectedPkgQuantity时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_receivedPkgQuantity_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('收货数量必填！', info['error']['message'], '缺少必填差参数receivedPkgQuantity时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_movedPkgQuantity_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('移动数量必填！', info['error']['message'], '缺少必填差参数movedPkgQuantity时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_ownerId_notuuid':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('货主id格式错误！', info['error']['message'], 'ownerId参数类型错误时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_supplierId_notuuid':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('供应商id格式错误！', info['error']['message'], 'supplierId参数类型错误时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_billTypeId_notuuid':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('单据类型id格式错误！', info['error']['message'], 'billTypeId参数类型错误时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_expectedPkgQuantity_notdouble':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('期望数量不是数值类型！', info['error']['message'], 'expectedPkgQuantity参数不是数值类型时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_receivedPkgQuantity_notdouble':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('收货数量不是数值类型！', info['error']['message'], 'receivedPkgQuantity参数不是数值类型时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_movedPkgQuantity_notdouble':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('移动数量不是数值类型！', info['error']['message'], 'movedPkgQuantity参数不是数值类型时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_orderDate_notdata':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('订单日期不是时间类型！', info['error']['message'], 'orderDate参数类型不是data时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_estimateDate_notdata':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('预计到货日期不是时间类型！', info['error']['message'], 'estimateDate参数类型不是data时，接口没有正确的对应处理机制！')

            # elif self.case_name == 'creatreceiptOrder_contactAddress_notstring':
            #     print('测试用例中文名名：', self.case_name_ch)
            #     print('接口返回：', info)
            #     self.assertEqual('联系地址格式不正确！', info['error']['message'], 'contactAddress参数类型传参不是字符类型时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_expectedPkgQuantity_overlength':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('期望数量数值长度超长！', info['error']['message'],
                                 'expectedPkgQuantity参数长度超数据库字段长度时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_receivedPkgQuantity_overlength':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('收货数量数值长度超长！', info['error']['message'],
                                 'receivedPkgQuantity参数长度超数据库字段长度时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_relatedBill1_allowlength':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                self.assertEqual(info['relatedBill1'], self.query['relatedBill1'], '新建的收货单的‘相关单据’编号与接口调用时的传参信息不一致！')

            elif self.case_name == 'creatreceiptOrder_relatedBill1_overlength':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('相关单据字符长度过长！', info['error']['message'], 'relatedBill1参数长度超数据库字段长度时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_contactAddress_allowlength':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                self.assertEqual(self.query['contactAddress'], info['contactAddress'], '新建的收货单的‘联系地址’与接口调用时的传参信息不一致！')

            elif self.case_name == 'creatreceiptOrder_contactAddress_overlength':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('联系地址字符长度过长！', info['error']['message'], 'contactAddress参数长度超数据库字段长度时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_str1_allowlength':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                self.assertEqual(info['str1'], self.query['str1'], '新建的收货单的‘扩展属性1’编号与接口调用时的传参信息不一致！')

            elif self.case_name == 'creatreceiptOrder_str1_overlength':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('扩展属性1字符长度过长！', info['error']['message'], 'str1参数长度超数据库字段长度时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_ownerId_error':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('货主信息错误！', info['error']['message'], 'ownerId参数传值错误（ownerId没有对应的货主信息）时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_billTypeId_error':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('单据类型信息错误！', info['error']['message'],
                                 'billTypeId参数传值错误（billTypeId没有对应的单据类型信息）时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_xStatus_includespace':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                try:
                    # 断言接口返回的信息中的'xStatus'值是否是’OPEN‘，否则抛出断言错误
                    self.assertEqual("OPEN", info['xStatus'])
                except AssertionError as e:
                    print('接口调用，单据状态参数的值中前后包含空格时，接口返回的单据状态不正确！', e)
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
                    self.assertFalse(any(x for x in (self.assertEqual(self.query['ownerId'], info['ownerId'],
                                                                      '接口传参的货主id与接口返回的货主id不一致！'),
                                                     self.assertEqual(self.query['supplierId'], info['supplierId'],
                                                                      '接口传参的供应商id与接口返回的供应商id不一致！'),
                                                     self.assertEqual(self.query['billTypeId'], info['billTypeId'],
                                                                      '接口传参的单据类型id与接口返回的单据类型id不一致！'),
                                                     self.assertEqual('OPEN', info['xStatus'],
                                                                      '接口返回的单据状态值不是OPEN！'),
                                                     self.assertEqual('UNPUTAWAY', info['shelvesStatus'],
                                                                      '接口返回的上架状态值不是UNPUTAWAY！'),
                                                     self.assertEqual(0.0, info['expectedPkgQuantity'],
                                                                      '接口传参的期望数量与接口返回的期望数量不一致！'),
                                                     self.assertEqual(0.0, info['receivedPkgQuantity'],
                                                                      '接口传参的收货数量与接口返回的收货数量不一致！'),
                                                     self.assertEqual(0.0, info['movedPkgQuantity'],
                                                                      '接口传参的移动数量与接口返回的移动数量不一致！'),
                                                     self.assertEqual(self.query['relatedBill1'], info['relatedBill1'],
                                                                      '接口传参的相关单据与接口返回的相关单据不一致！'),
                                                     self.assertEqual(None, info['orderDate'],
                                                                      '接口传参的订单日期与接口返回的订单日期不一致！'),
                                                     self.assertEqual(None, info['estimateDate'],
                                                                      '接口传参的收货日期与接口返回的收货日期不一致！'),
                                                     self.assertEqual(self.query['fromName'], info['fromName'],
                                                                      '接口传参的发货人与接口返回的发货人不一致！'),
                                                     self.assertEqual(self.query['contactAddress'],
                                                                      info['contactAddress'],
                                                                      '接口传参的联系地址与接口返回的联系地址不一致！'),
                                                     self.assertEqual(self.query['contactPostcode'],
                                                                      info['contactPostcode'],
                                                                      '接口传参的邮编与接口返回的邮编不一致！'),
                                                     self.assertEqual(self.query['contactName'], info['contactName'],
                                                                      '接口传参的联系人与接口返回的联系人不一致！'),
                                                     self.assertEqual(self.query['contactMobile'], info['contactMobile'],
                                                                      '接口传参的联系电话与接口返回的联系电话不一致！'),
                                                     self.assertEqual(self.query['comments'], info['comments'],
                                                                      '接口传参的备注信息与接口返回的备注信息不一致！'),
                                                     self.assertEqual(self.query['str1'], info['str1'],
                                                                      '接口传参的扩展属性1与接口返回的扩展属性1不一致！'),
                                                     self.assertEqual(self.query['str2'], info['str2'],
                                                                      '接口传参的扩展属性2与接口返回的扩展属性2不一致！'),
                                                     self.assertEqual(self.query['str3'], info['str3'],
                                                                      '接口传参的扩展属性3与接口返回的扩展属性3不一致！'),
                                                     self.assertEqual(self.query['str4'], info['str4'],
                                                                      '接口传参的扩展属性4与接口返回的扩展属性4不一致！'),
                                                     self.assertEqual(self.query['ownerId'], str(ReceiptOrder[0][1]),
                                                                      '接口传参的货主ID与新建的收货单的货主ID不一致！'),
                                                     self.assertEqual(self.query['supplierId'], str(ReceiptOrder[0][2]),
                                                                      '接口传参的供应商ID与新建的收货单的供应商ID不一致！'),
                                                     self.assertEqual(self.query['billTypeId'], str(ReceiptOrder[0][0]),
                                                                      '接口传参的单据类型ID与新建的收货单的单据类型ID不一致！'),
                                                     self.assertEqual('OPEN', ReceiptOrder[0][3],
                                                                      '新建的收货单的单据状态不是‘OPEN’！'),
                                                     self.assertEqual('UNPUTAWAY', ReceiptOrder[0][4],
                                                                      '新建的收货单的上架状态不是‘UNPUTAWAY’！'),
                                                     self.assertEqual(0.0, ReceiptOrder[0][5],
                                                                      '接口传参的期望数量与新建的收货单的期望数量不一致！'),
                                                     self.assertEqual(None, ReceiptOrder[0][13],
                                                                      '接口传参的订单日期与新建的收货单的订单日期不一致！'),
                                                     self.assertEqual(None, ReceiptOrder[0][14],
                                                                      '接口传参的到货日期与新建的收货单的到货日期不一致！'),
                                                     self.assertEqual(self.query['fromName'], ReceiptOrder[0][16],
                                                                      '接口传参的发货人与新建的收货单的发货人不一致！'),
                                                     self.assertEqual(self.query['contactAddress'],
                                                                      ReceiptOrder[0][11],
                                                                      '接口传参的联系地址与新建的收货单的联系地址不一致！'),
                                                     self.assertEqual(self.query['contactPostcode'],
                                                                      ReceiptOrder[0][17],
                                                                      '接口传参的邮编与新建的收货单的邮编不一致！'),
                                                     self.assertEqual(self.query['contactName'], ReceiptOrder[0][15],
                                                                      '接口传参的联系人与新建的收货单的联系人不一致！'),
                                                     self.assertEqual(self.query['contactMobile'],
                                                                      ReceiptOrder[0][12],
                                                                      '接口传参的联系电话与新建的收货单的联系电话不一致！'),
                                                     self.assertEqual(self.query['comments'], ReceiptOrder[0][6],
                                                                      '接口传参的备注信息与新建的收货单的备注信息不一致！'),
                                                     self.assertEqual(self.query['str1'], ReceiptOrder[0][7],
                                                                      '接口传参的扩展属性1与新建的收货单的扩展属性1不一致！'),
                                                     self.assertEqual(self.query['str2'], ReceiptOrder[0][8],
                                                                      '接口传参的扩展属性2与新建的收货单的扩展属性2不一致！'),
                                                     self.assertEqual(self.query['str3'], ReceiptOrder[0][9],
                                                                      '接口传参的扩展属性3与新建的收货单的扩展属性3不一致！'),
                                                     self.assertEqual(self.query['str4'], ReceiptOrder[0][10],
                                                                      '接口传参的扩展属性4与新建的收货单的扩展属性4不一致！')
                                                     )))

            elif self.case_name == 'creatreceiptOrder_expectedPkgQuantity_minus':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('期望数量数值应大于0！', info['error']['message'],
                                 'expectedPkgQuantity参数数值小于0时，接口没有正确的对应处理机制！')

            elif self.case_name == 'creatreceiptOrder_contactAddress_specialcharacter':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                self.assertEqual(self.query['contactAddress'], info['contactAddress'],
                                 '接口传参的联系地址与接口返回的联系地址不一致！')

            elif self.case_name == 'creatreceiptOrder_contactName_includespace':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                self.assertEqual(self.query['contactName'].strip(), info['contactName'],
                                 '接口传参的联系人姓名前后包含空格时，接口返回的联系人姓名未去除空格！')

            elif self.case_name == 'creatreceiptOrder_comments_specialcharacter':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                self.assertEqual(self.query['comments'], info['comments'],
                                 '接口传参的备注信息与接口返回的备注信息不一致！')

            elif self.case_name == 'creatreceiptOrder_str1_specialcharacter':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                self.assertEqual(self.query['str1'], info['str1'],
                                 '接口传参的扩展属性1与接口返回的扩展属性1不一致！')

            elif self.case_name == 'creatreceiptOrder_str2_specialcharacter':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                self.assertEqual(self.query['str2'], info['str2'],
                                 '接口传参的扩展属性2与接口返回的扩展属性2不一致！')

            elif self.case_name == 'creatreceiptOrder_str3_specialcharacter':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                self.assertEqual(self.query['str3'], info['str3'],
                                 '接口传参的扩展属性3与接口返回的扩展属性3不一致！')
            elif self.case_name == 'creatreceiptOrder_str4_specialcharacter':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                self.assertEqual(self.query['str4'], info['str4'],
                                 '接口传参的扩展属性4与接口返回的扩展属性4不一致！')


if __name__ == '__main__':
    unittest.main()




