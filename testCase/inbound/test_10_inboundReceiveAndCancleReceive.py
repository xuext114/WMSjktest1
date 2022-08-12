#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对更新时间最早的一条生效或收货中的收货单的收货明细进行收货
本脚本默认采用托盘不允许混托模式、默认收货后需要外形检测
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
from copy import copy


url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'receive')


@paramunittest.parametrized(*casexls)
class testreceive(unittest.TestCase):
    def setParameters(self, case_name, method, path, query):
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = str(query)
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()

        # 从数据库查询获取更新时间最早一条状态为’生效‘的收货单进行收货
        activeXstatsCur = ms().get_all(
            ms().ExecQuery("SELECT b.id ,b.ExpectedPkgQuantity ,b.CreatorId "
                           "FROM WMS.ReceiptOrderItem a INNER JOIN WMS.ReceiptOrder b "
                           "ON a.ReceiptOrderId =b.Id AND b.XStatus='ACTIVE' "
                           "AND a.ReceivedPkgQuantity=0 ORDER BY b.LastModificationTime"))
        # 从数据库查询获取更新时间最早一条状态为’部分收货‘的收货单进行收货
        receiveingXstatsCur = ms().get_all(
            ms().ExecQuery("SELECT b.id ,b.ExpectedPkgQuantity ,b.CreatorId "
                           "FROM WMS.ReceiptOrderItem a INNER JOIN WMS.ReceiptOrder b "
                           "ON a.ReceiptOrderId =b.Id AND b.XStatus='RECEIVEING' "
                           "AND a.ReceivedPkgQuantity=0 ORDER BY b.LastModificationTime"))

        if self.case_name == 'inboundReceive':
            self.query = ast.literal_eval(str(query))
            self.query['ReceiptOrderItemId'] = str(activeXstatsCur[0][0])
            self.query['ReceivedPkgQuantity'] = float(activeXstatsCur[0][1])
            self.query['LocationId'] = str(ms().transformNone(ms().getvalue('WMS.Location', 'LocationId')[0][0]))
            self.query['Pallet'] = 'TP' + str(ms().getvalue('sequencetest', 'VALUE')[0][0])
            self.query['WorkerId'] = str(activeXstatsCur[0][2])
        elif self.case_name == 'inboundReceive_ReceiptOrderItem_null':
            self.query = ast.literal_eval(str(query))
            self.query['ReceiptOrderItemId'] = ''
            self.query['ReceivedPkgQuantity'] = float(activeXstatsCur[0][1])
            self.query['LocationId'] = str(ms().transformNone(ms().getvalue('WMS.Location', 'LocationId')[0][0]))
            self.query['Pallet'] = 'TP' + str(ms().getvalue('sequencetest', 'VALUE')[0][0])
            self.query['WorkerId'] = str(activeXstatsCur[0][2])
        elif self.case_name == 'inboundReceive_ReceivedPkgQuantity_null':
            self.query = ast.literal_eval(str(query))
            self.query['ReceiptOrderItemId'] = str(activeXstatsCur[0][0])
            self.query['ReceivedPkgQuantity'] = ''
            self.query['LocationId'] = str(ms().transformNone(ms().getvalue('WMS.Location', 'LocationId')[0][0]))
            self.query['Pallet'] = 'TP' + str(ms().getvalue('sequencetest', 'VALUE')[0][0])
            self.query['WorkerId'] = str(activeXstatsCur[0][2])
        elif self.case_name == 'inboundReceive_Pallet_null':
            self.query = ast.literal_eval(str(query))
            self.query['ReceiptOrderItemId'] = str(activeXstatsCur[0][0])
            self.query['ReceivedPkgQuantity'] = float(activeXstatsCur[0][1])
            self.query['LocationId'] = str(ms().transformNone(ms().getvalue('WMS.Location', 'LocationId')[0][0]))
            self.query['Pallet'] = ''
            self.query['WorkerId'] = str(activeXstatsCur[0][2])
        elif self.case_name == 'inboundReceive_ReceivedPkgQuantity_allowlength':
            self.query = ast.literal_eval(str(query))
            self.query['ReceiptOrderItemId'] = str(activeXstatsCur[0][0])
            self.query['ReceivedPkgQuantity'] = 1000000000000000.01
            self.query['LocationId'] = str(ms().transformNone(ms().getvalue('WMS.Location', 'LocationId')[0][0]))
            self.query['Pallet'] = 'TP' + str(ms().getvalue('sequencetest', 'VALUE')[0][0])
            self.query['WorkerId'] = str(activeXstatsCur[0][2])
        elif self.case_name == 'inboundReceive_ReceivedPkgQuantity_overlength':
            self.query = ast.literal_eval(str(query))
            self.query['ReceiptOrderItemId'] = str(activeXstatsCur[0][0])
            self.query['ReceivedPkgQuantity'] = 10000000000000000.01
            self.query['LocationId'] = str(ms().transformNone(ms().getvalue('WMS.Location', 'LocationId')[0][0]))
            self.query['Pallet'] = 'TP' + str(ms().getvalue('sequencetest', 'VALUE')[0][0])
            self.query['WorkerId'] = str(activeXstatsCur[0][2])
        elif self.case_name == 'inboundReceive_ReceivedPkgQuantity_notNumber':
            self.query = ast.literal_eval(str(query))
            self.query['ReceiptOrderItemId'] = str(activeXstatsCur[0][0])
            self.query['ReceivedPkgQuantity'] = 'abc01'
            self.query['LocationId'] = str(ms().transformNone(ms().getvalue('WMS.Location', 'LocationId')[0][0]))
            self.query['Pallet'] = 'TP' + str(ms().getvalue('sequencetest', 'VALUE')[0][0])
            self.query['WorkerId'] = str(activeXstatsCur[0][2])
        elif self.case_name == 'inboundReceive_ReceivedPkgQuantity_equallZero':
            self.query = ast.literal_eval(str(query))
            self.query['ReceiptOrderItemId'] = str(activeXstatsCur[0][0])
            self.query['ReceivedPkgQuantity'] = 0
            self.query['LocationId'] = str(ms().transformNone(ms().getvalue('WMS.Location', 'LocationId')[0][0]))
            self.query['Pallet'] = 'TP' + str(ms().getvalue('sequencetest', 'VALUE')[0][0])
            self.query['WorkerId'] = str(activeXstatsCur[0][2])
        elif self.case_name == 'inboundReceive_ReceivedPkgQuantity_lessZero':
            self.query = ast.literal_eval(str(query))
            self.query['ReceiptOrderItemId'] = str(activeXstatsCur[0][0])
            self.query['ReceivedPkgQuantity'] = '-10'
            self.query['LocationId'] = str(ms().transformNone(ms().getvalue('WMS.Location', 'LocationId')[0][0]))
            self.query['Pallet'] = 'TP' + str(ms().getvalue('sequencetest', 'VALUE')[0][0])
            self.query['WorkerId'] = str(activeXstatsCur[0][2])
        elif self.case_name == 'inboundReceive_PalletInInventory':
            self.query = ast.literal_eval(str(query))
            # 数据库查询已经在库存（架上或地面）中的托盘
            PalletCur = ms().get_all(
                ms().ExecQuery("SELECT Pallet FROM WMS.InventoryDetail WHERE PackageQuantity>0"))
            self.query['ReceiptOrderItemId'] = str(activeXstatsCur[0][0])
            self.query['ReceivedPkgQuantity'] = float(activeXstatsCur[0][1])
            self.query['LocationId'] = str(ms().transformNone(ms().getvalue('WMS.Location', 'LocationId')[0][0]))
            self.query['Pallet'] = str(PalletCur[0][0])
            self.query['WorkerId'] = str(activeXstatsCur[0][2])

        self.query = str(self.query).encode('utf-8')

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testreceive(self):
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
            if self.case_name == 'inboundReceive':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                # 在数据库查询库存明细表中是否有该托盘数据
                InventoryDetail = ms().get_all(
                    ms().ExecQuery("SELECT *  FROM WMS.InventoryDetail WHERE Pallet ='%s' AND PackageQuantity =%f "
                                   % (self.query['Pallet'], float(self.query['ReceivedPkgQuantity']))))
                # 在数据库中查询该收货明细的收货数量
                ReceivedPkgQuantity = ms().get_all(
                    ms().ExecQuery("SELECT ReceivedPkgQuantity FROM WMS.ReceiptOrderItem "
                                   "WHERE Id ='%s'" % self.query['ReceiptOrderItemId']))
                # 在数据库查询是否有该条收货记录
                ReceivedRecord = ms().get_all(
                    ms().ExecQuery("SELECT * FROM WMS.ReceivedRecord "
                                   "WHERE ReceiptOrderItemId= '%s' AND LocationId ='%s' "
                                   "AND Pallet ='%s' AND ReceivedPkgQuantity =%f"
                                   % (self.query['ReceiptOrderItemId'], self.query['LocationId'],
                                      self.query['Pallet'], self.query['ReceivedPkgQuantity'])))

                # 在数据库查询收货单状态
                Xstats = ms().get_all(
                    ms().ExecQuery("SELECT XStatus FROM WMS.ReceiptOrder "
                                   "WHERE Id =(SELECT ReceiptOrderId FROM WMS.ReceiptOrderItem "
                                   "WHERE Id='%s')" % self.query['ReceiptOrderItemId']))
                # 在数据库查询获取该收货明细对应的收货单的所有收货明细的期望数量和收货数量
                ReceiptOrderItem = ms().get_all(
                    ms().ExecQuery("SELECT ExpectedPkgQuantity, ReceivedPkgQuantity FROM WMS.ReceiptOrderItem "
                                   "WHERE ReceiptOrderId =(SELECT ReceiptOrderId FROM WMS.ReceiptOrderItem "
                                   "WHERE Id ='%s')" % self.query['ReceiptOrderItemId']))

                # 循环收货明细的期望数量和收货数量，如果有收货数量小于期望数量，跳出循环，收货单状态为’部分收货‘，否则收货单状态为’收货完成‘
                reXstats = ''
                for i in range(len(ReceiptOrderItem)):  # 预计遍历所有收货明细
                    # 循环中判断收货数量是否小于期望数量，如果小于，则收货单状态定义为’部分收货‘，并跳出循环
                    if ReceiptOrderItem[i][1] < ReceiptOrderItem[i][0]:
                        reXstats = 'RECEIVING'
                        break
                else:  # 如果正常循环完成，则收货单状态应为’收货完成‘
                    reXstats = 'RECEIVED'

                self.assertFalse(any(x for x in (self.assertIs(True, info,
                                                               '测试不通过，对生效状态的收货单的收货明细进行收货时，接口没有返回true！'),
                                                 self.assertTrue(InventoryDetail,
                                                                 '收货成功后，数据库库存表中没有改托盘库存数据！'),
                                                 self.assertEqual(float(self.query['ReceivedPkgQuantity']),
                                                                  float(ReceivedPkgQuantity[0][0]),
                                                                  '收货成功后，该收货明细的收货数量与接口调用时，用户传的数量不一致！'),
                                                 self.assertEqual(reXstats, Xstats[0][0],
                                                                  '单个收货明细收货成功后，该收货明细所属收货单的状态不正确！'))))


if __name__ == '__main__':
    testreceive(unittest.TestCase)