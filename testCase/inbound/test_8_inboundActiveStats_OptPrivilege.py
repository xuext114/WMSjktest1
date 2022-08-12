#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对生效状态的收货单进行各项功能操作验证，包括编辑、删除、收货、创建上架单、
取消收货、作废、查询收货记录、修改供应商
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
import datetime

url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'inboundActiveStats_OptPrivilege')


@paramunittest.parametrized(*casexls)
class testinboundActive(unittest.TestCase):
    def setParameters(self, case_name, case_name_ch, method, path, query):
        self.case_name = str(case_name)
        self.case_name_ch = str(case_name_ch)
        self.query = str(query)
        self.path = str(path)
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()

        # 数据库查询状态为生效的收货单
        activeStatsReceiptOrder = ms().get_all(
            ms().ExecQuery("SELECT a.Id, a.CreationTime, a.CreatorId, a.Creator, a.LastModificationTime, "
                           "a.LastModifierId, a.LastModifier, a.WhId, a.BillTypeId, a.XCode, a.OwnerId, "
                           "a.SupplierId, a.XStatus, a.ShelvesStatus, a.ExpectedPkgQuantity, a.ReceivedPkgQuantity, "
                           "a.MovedPkgQuantity, a.TolocationId, a.OperateStatus,a.ErpStatus, a.IsOffLine, a.TrusteeBy, "
                           "a.QCBy, a.Storekeeper, a.TradingCompany, a.RelationCode, a.Comments,a.Str1,a.Str2, "
                           "a.Str3, a.Str4, a.Str5, a.Str6, a.Str7, a.Str8, a.Str9, a.Str10, a.ContactAddress,"
                           "a.ContactCity,a.ContactCountry, a.ContactEmail, a.ContactFax, a.ContactMobile, "
                           "a.ContactPostcode, a.ContactProvince, a.ContactTelephone, a.EndReceivedDate, "
                           "a.EstimateDate, a.FromName, a.OrderDate, a.RelatedBill1,a.RelatedBill2, a.RelatedBill3, "
                           "a.StartReceivedDate, a.ContactName, b.Id ReceiptOrderItemId, "
                           "b.ExpectedPkgQuantity ReceiptOrderItem_ExpectedPkgQuantity "
                           "FROM WMS.ReceiptOrder a INNER JOIN WMS.ReceiptOrderItem b ON a.Id=b.ReceiptOrderId "
                           "AND a.XStatus ='ACTIVE' ORDER BY a.LastModificationTime"))

        if self.case_name == 'inboundActiveStats_update':
            self.query = eval(query)
            self.query['creator'] = str(ms().transformNone(activeStatsReceiptOrder[0][3]))
            self.query['lastModifier'] = str(ms().transformNone(activeStatsReceiptOrder[0][6]))
            self.query['id'] = str(ms().transformNone(activeStatsReceiptOrder[0][0]))
            self.query['lastModificationTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 修改更新时间
            self.query['lastModifierId'] = str(ms().transformNone(activeStatsReceiptOrder[0][5]))
            self.query['creationTime'] = activeStatsReceiptOrder[0][1].strftime("%Y-%m-%d %H:%M:%S")
            self.query['creatorId'] = str(ms().transformNone(activeStatsReceiptOrder[0][2]))
            self.query['whId'] = str(ms().transformNone(activeStatsReceiptOrder[0][7]))
            self.query['ownerId'] = str(ms().transformNone(activeStatsReceiptOrder[0][10]))
            self.query['supplierId'] = str(ms().transformNone(activeStatsReceiptOrder[0][11]))
            self.query['xCode'] = str(ms().transformNone(activeStatsReceiptOrder[0][9]))
            self.query['billTypeId'] = str(ms().transformNone(activeStatsReceiptOrder[0][8]))
            self.query['xStatus'] = ms().transformNone(activeStatsReceiptOrder[0][12])
            self.query['shelvesStatus'] = str(ms().transformNone(activeStatsReceiptOrder[0][13]))
            self.query['expectedPkgQuantity'] = float(activeStatsReceiptOrder[0][14])
            self.query['receivedPkgQuantity'] = float(activeStatsReceiptOrder[0][15])
            self.query['movedPkgQuantity'] = float(activeStatsReceiptOrder[0][16])
            self.query['tolocationId'] = str(ms().transformNone(activeStatsReceiptOrder[0][17]))
            self.query['relatedBill1'] = str(ms().transformNone(activeStatsReceiptOrder[0][50]))
            self.query['relatedBill2'] = str(ms().transformNone(activeStatsReceiptOrder[0][51]))
            self.query['relatedBill3'] = str(ms().transformNone(activeStatsReceiptOrder[0][52]))
            self.query['orderDate'] = activeStatsReceiptOrder[0][49].strftime("%Y-%m-%d")
            self.query['estimateDate'] = activeStatsReceiptOrder[0][47].strftime("%Y-%m-%d")
            self.query['startReceivedDate'] = str(ms().transformNone(activeStatsReceiptOrder[0][53]))
            self.query['endReceivedDate'] = str(ms().transformNone(activeStatsReceiptOrder[0][46]))
            self.query['fromName'] = str(ms().transformNone(activeStatsReceiptOrder[0][48]))
            self.query['contactCountry'] = str(ms().transformNone(activeStatsReceiptOrder[0][39]))
            self.query['contactProvince'] = str(ms().transformNone(activeStatsReceiptOrder[0][44]))
            self.query['contactCity'] = str(ms().transformNone(activeStatsReceiptOrder[0][38]))
            self.query['contactAddress'] = '联系地址-测试生效状态修改收货单'  # 修改联系地址
            self.query['contactPostcode'] = str(ms().transformNone(activeStatsReceiptOrder[0][43]))
            self.query['contactName'] = str(ms().transformNone(activeStatsReceiptOrder[0][54]))
            self.query['contactMobile'] = str(ms().transformNone(activeStatsReceiptOrder[0][42]))
            self.query['contactTelephone'] = str(ms().transformNone(activeStatsReceiptOrder[0][45]))
            self.query['contactFax'] = str(ms().transformNone(activeStatsReceiptOrder[0][41]))
            self.query['contactEmail'] = str(ms().transformNone(activeStatsReceiptOrder[0][40]))
            self.query['operateStatus'] = str(ms().transformNone(activeStatsReceiptOrder[0][18]))
            self.query['erpStatus'] = str(ms().transformNone(activeStatsReceiptOrder[0][19]))
            self.query['isOffLine'] = str(ms().transformNone(activeStatsReceiptOrder[0][20]))
            self.query['trusteeBy'] = str(ms().transformNone(activeStatsReceiptOrder[0][21]))
            self.query['qcBy'] = str(ms().transformNone(activeStatsReceiptOrder[0][22]))
            self.query['storekeeper'] = str(ms().transformNone(activeStatsReceiptOrder[0][23]))
            self.query['tradingCompany'] = str(ms().transformNone(activeStatsReceiptOrder[0][24]))
            self.query['relationCode'] = str(ms().transformNone(activeStatsReceiptOrder[0][25]))
            self.query['comments'] = str(ms().transformNone(activeStatsReceiptOrder[0][26]))
            self.query['str1'] = '扩展字段1-测试生效状态修改收货单'  # 修改联系地址
            self.query['str2'] = str(ms().transformNone(activeStatsReceiptOrder[0][28]))
            self.query['str3'] = str(ms().transformNone(activeStatsReceiptOrder[0][29]))
            self.query['str4'] = str(ms().transformNone(activeStatsReceiptOrder[0][30]))
            self.query['str5'] = str(ms().transformNone(activeStatsReceiptOrder[0][31]))
            self.query['str6'] = str(ms().transformNone(activeStatsReceiptOrder[0][32]))
            self.query['str7'] = str(ms().transformNone(activeStatsReceiptOrder[0][33]))
            self.query['str8'] = str(ms().transformNone(activeStatsReceiptOrder[0][34]))
            self.query['str9'] = str(ms().transformNone(activeStatsReceiptOrder[0][35]))
            self.query['str10'] = str(ms().transformNone(activeStatsReceiptOrder[0][36]))
        elif self.case_name == 'inboundActiveStats_delete':
            self.query = eval(query)
            self.query['id'] = str(ms().transformNone(activeStatsReceiptOrder[0][0]))
            self.query['billTypeId'] = str(ms().transformNone(activeStatsReceiptOrder[0][8]))
            self.query['expectedPkgQuantity'] = float(activeStatsReceiptOrder[0][14])
            self.query['receivedPkgQuantity'] = float(activeStatsReceiptOrder[0][15])
            self.query['movedPkgQuantity'] = float(activeStatsReceiptOrder[0][16])
            self.query['creationTime'] = activeStatsReceiptOrder[0][1].strftime("%Y-%m-%d %H:%M:%S")
        elif self.case_name == 'inboundActiveStats_receive':
            self.query = eval(query)
            # 数据库查询获取货位类型为‘收货’的库位,用于收货
            LocationIdcur = ms().getvalue('WMS.Location', 'LocationId')
            self.query['ReceiptOrderItemId'] = str(activeStatsReceiptOrder[0][55])
            self.query['ReceivedPkgQuantity'] = str(activeStatsReceiptOrder[0][56])
            self.query['LocationId'] = str(ms().transformNone(LocationIdcur[0][0]))
            self.query['Pallet'] = 'TP' + str(ms().getvalue('sequencetest', 'VALUE')[0][0])
            self.query['WorkerId'] = str(activeStatsReceiptOrder[0][2])
        elif self.case_name in ('inboundActiveStats_manualCreateMoveDoc', 'inboundActiveStats_cancelReceive',
                                'inboundActiveStats_cancel'):
            spilpath = os.path.split(self.path)  # 拆分路径，将最后部分拆分出来，返回元祖
            # 将拆分后的路径的前面部分和从数据库获取到的receiptOrderId重新组成一个列表,第一个值后面必须以/结尾，否则后续拼凑后的路径会不正确
            spilpathlist = [spilpath[0] + '/', str(activeStatsReceiptOrder[0][0])]
            self.path = str(os.path.join(spilpathlist[0], spilpathlist[1]))  # 用列表的两部分拼凑成新路径
            self.headers['Content-Length'] = '0'  # 将headers中的'Content-Type'值改为0，用于请求体为空的接口
        elif self.case_name == 'inboundActiveStats_queryReceiverRecords':
            self.query = eval(query)
            self.query['condition']['receiptOrderId']['='] = str(activeStatsReceiptOrder[0][0])
        elif self.case_name == 'inboundActiveStats_correctSupplier':
            supplierIdcur = ms().getvalue('WMS.Orgnization', 'supplierId')
            spilpath = os.path.split(self.path)  # 拆分路径，将最后部分拆分出来，返回元祖
            # 将拆分后的路径的前面部分和从数据库获取到的supplierId和receiptOrderCode重新组成一个列表,第一个值后面必须以/结尾，否则后续拼凑后的路径会不正确
            self.spilpathlist = [spilpath[0] + '/', str(supplierIdcur[0][0])+'?'+'receiptOrderCode=' +
                                 str(activeStatsReceiptOrder[0][9])]
            self.path = str(os.path.join(self.spilpathlist[0], self.spilpathlist[1]))  # 用列表的两部分拼凑成新路径
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
            if self.case_name == 'inboundActiveStats_update':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('生效状态的收货单不可修改!', info['error']['message'],
                                 '对‘生效’状态的收货单编辑不成功，接口没有正确的对应处理机制！')
            elif self.case_name == 'inboundActiveStats_delete':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('生效状态的收货单不可删除!', info['error']['message'],
                                 '对‘生效’状态的收货单删除不成功，接口没有正确的对应处理机制！')
            elif self.case_name == 'inboundActiveStats_receive':
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

            elif self.case_name == 'inboundActiveStats_manualCreateMoveDoc':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('请先收货，再创建上架单！', info['error']['message'],
                                 '对生效状态的收货单进行收货时，接口没有正确的对应处理机制！')
            elif self.case_name == 'inboundActiveStats_cancelReceive':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('取消收货时入库单状态:ACTIVE错误',
                                 info['error']['message'],
                                 '对生效状态的收货单进行取消收货时，接口没有正确的对应处理机制！')
            elif self.case_name == 'inboundActiveStats_cancel':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('该单据尚未收货，不能作废，请进行失效操作！',
                                 info['error']['message'],
                                 '对生效状态的收货单进行作废时，接口没有正确的对应处理机制！')
            elif self.case_name == 'inboundActiveStats_queryReceiverRecords':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual(0, info['totalCount'], '测试不通过，对生效状态的收货单进行收货记录查询，应没有记录！')
            elif self.case_name == 'inboundActiveStats_correctSupplier':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                sqltext = "SELECT SupplierId FROM WMS.ReceiptOrder WHERE XCode='%s'" % str(self.spilpathlist[1][-14:])
                SupplierIdcur = ms().get_all(ms().ExecQuery(sqltext))  # 查询数据库该收货单当前的供应商
                self.assertFalse(any(x for x in (self.assertEqual(10, info, '修改供应商不成功，接口返回不正确！'),
                                                 self.assertEqual(str(self.spilpathlist[1][0:36]),
                                                                  str(SupplierIdcur[0][0]),
                                                                  '修改供应商不成功，数据库该收货单的供应商不是用户修改的供应商！'))))


if __name__ == '__main__':
    unittest.main()

