#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建测试数据用！
本脚本非测试脚本，脚本主要功能为新建收货单、收货明细，生效收货单、
收货、对部分已收货明细进行外形检测及部分进行上架，用于其他测试脚本在进行业务校验时，作为测试数据使用
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
import random
from copy import copy
import os


url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'constructTestData')

@paramunittest.parametrized(*casexls)
class testcreatReceiptOrder(unittest.TestCase):
    def setParameters(self, case_name, case_name_ch, method, path, query):
        self.case_name = str(case_name)
        self.case_name_ch = str(case_name_ch)
        self.path = str(path)
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()
        if self.case_name == 'ActiveReceiptOrder':
            self.query = str(query)
        else:
            self.query = ast.literal_eval(query)

        if self.case_name == 'creatreceiptOrder':
            self.query['ownerId'] = str(ms().getvalue('WMS.Orgnization', 'ownerId')[0][0])
            self.query['supplierId'] = str(ms().getvalue('WMS.Orgnization', 'supplierId')[0][0])
            self.query['billTypeId'] = str(ms().getvalue('WMS.BillType', 'billTypeId')[0][0])

        elif self.case_name == 'creatreceiptOrderItem':
            # 新增收货单明细，取一个最新的、打开状态的收货主单据(即creatreceiptOrder用例创建的收货单)，循环10个（如果有）物料创建收货明细
            cur = ms().getvalue('WMS.ReceiptOrder', 'receiptOrderItem')
            self.querylist1 = []
            for i in range(len(cur)):  # 将查询结果添加到querylist中
                self.query['receiptOrderItem']['receiptOrderId'] = str(cur[i][0])
                self.query['receiptOrderItem']['materialId'] = str(cur[i][9])
                self.query['receiptOrderItem']['packageUnitId'] = str(cur[i][24])
                self.query['receiptOrderItem']['expectedPkgQuantity'] = random.choice([10, 20, 30, 40, 50])
                self.query['receiptOrderItem']['receiptOrder']['ownerId'] = str(cur[i][5])
                self.query['receiptOrderItem']['receiptOrder']['supplierId'] = str(cur[i][8])
                self.query['receiptOrderItem']['receiptOrder']['xCode'] = str(cur[i][7])
                self.query['receiptOrderItem']['receiptOrder']['billTypeId'] = str(cur[i][6])
                self.query['receiptOrderItem']['receiptOrder']['id'] = str(cur[i][0])
                self.query['receiptOrderItem']['receiptOrder']['lastModificationTime'] = str(cur[i][4])
                self.query['receiptOrderItem']['receiptOrder']['lastModifierId'] = str(cur[i][1])
                self.query['receiptOrderItem']['receiptOrder']['creationTime'] = str(cur[i][3])
                self.query['receiptOrderItem']['receiptOrder']['creatorId'] = str(cur[i][2])
                self.query['receiptOrderItem']['material']['xCode'] = str(cur[i][12])
                self.query['receiptOrderItem']['material']['xName'] = str(cur[i][13])
                self.query['receiptOrderItem']['material']['isForbidden'] = str(cur[i][10])
                self.query['receiptOrderItem']['material']['forbiddenUserId'] = str(cur[i][11])
                self.query['receiptOrderItem']['material']['spec'] = str(cur[i][14])
                self.query['receiptOrderItem']['material']['smallestUnit'] = str(cur[i][15])
                self.query['receiptOrderItem']['material']['materialCategoryId'] = str(cur[i][16])
                self.query['receiptOrderItem']['material']['materialPropertyRuleId'] = str(cur[i][17])
                self.query['receiptOrderItem']['material']['allocatRelationId'] = str(cur[i][18])
                self.query['receiptOrderItem']['material']['shipmentRuleId'] = str(cur[i][19])
                self.query['receiptOrderItem']['material']['id'] = str(cur[i][9])
                self.query['receiptOrderItem']['material']['lastModificationTime'] = str(cur[i][23])
                self.query['receiptOrderItem']['material']['lastModifierId'] = str(cur[i][21])
                self.query['receiptOrderItem']['material']['creationTime'] = str(cur[i][22])
                self.query['receiptOrderItem']['material']['creatorId'] = str(cur[i][20])
                self.query['receiptOrderItem']['material']['materialCategory']['xCode'] = str(cur[i][34])
                self.query['receiptOrderItem']['material']['materialCategory']['xName'] = str(cur[i][35])
                self.query['receiptOrderItem']['material']['materialCategory']['materialPropertyRuleId'] = str(cur[i][36])
                self.query['receiptOrderItem']['material']['materialCategory']['isForbidden'] = str(cur[i][37])
                self.query['receiptOrderItem']['material']['materialCategory']['id'] = str(cur[i][16])
                self.query['receiptOrderItem']['material']['materialCategory']['lastModificationTime'] = str(cur[i][38])
                self.query['receiptOrderItem']['material']['materialCategory']['creationTime'] = str(cur[i][40])
                self.query['receiptOrderItem']['material']['materialCategory']['creatorId'] = str(cur[i][39])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['xCode'] = str(cur[i][47])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['xName'] = str(cur[i][48])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['productionTime'] = str(cur[i][49])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['receivedTime'] = str(cur[i][50])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['inboundTime'] = str(cur[i][51])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['expiredTime'] = str(cur[i][52])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['aStartTime'] = str(cur[i][53])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['qcStartTime'] = str(cur[i][54])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['preservationDays'] = str(cur[i][55])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['sourceOrderCode'] = str(cur[i][56])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['batchNo'] = str(cur[i][57])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['supplierId'] = str(cur[i][58])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str1'] = str(cur[i][59])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str2'] = str(cur[i][60])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str3'] = str(cur[i][61])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str4'] = str(cur[i][62])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str5'] = str(cur[i][63])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str6'] = str(cur[i][64])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str7'] = str(cur[i][65])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str8'] = str(cur[i][66])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str9'] = str(cur[i][67])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str10'] = str(cur[i][68])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['id'] = str(cur[i][36])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['lastModificationTime'] = str(cur[i][44])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['lastModifierId'] = str(cur[i][45])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['creationTime'] = str(cur[i][41])
                self.query['receiptOrderItem']['material']['materialPropertyRule']['creatorId'] = str(cur[i][42])
                self.query['receiptOrderItem']['material']['packageUnit'][0]['materialId'] = str(cur[i][9])
                self.query['receiptOrderItem']['material']['packageUnit'][0]['unit'] = str(cur[i][30])
                self.query['receiptOrderItem']['material']['packageUnit'][0]['pkgLevel'] = str(cur[i][33])
                self.query['receiptOrderItem']['material']['packageUnit'][0]['convertFigureSmallUnit'] = str(cur[i][31])
                self.query['receiptOrderItem']['material']['packageUnit'][0]['convertFigure'] = str(cur[i][32])
                self.query['receiptOrderItem']['material']['packageUnit'][0]['id'] = str(cur[i][24])
                self.query['receiptOrderItem']['material']['packageUnit'][0]['lastModificationTime'] = str(cur[i][27])
                self.query['receiptOrderItem']['material']['packageUnit'][0]['lastModifierId'] = str(cur[i][28])
                self.query['receiptOrderItem']['material']['packageUnit'][0]['creationTime'] = str(cur[i][25])
                self.query['receiptOrderItem']['material']['packageUnit'][0]['creatorId'] = str(cur[i][26])
                self.query['receiptOrderItem']['material']['packageUnit'][0]['creator'] = str(cur[i][29])
                self.query['materialProperty']['propertyRuleId'] = str(cur[i][17])
                self.query['materialProperty']['materialId'] = str(cur[i][9])
                self.query['materialProperty']['productionTime'] = str((datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d'))  # 当前日期减30天作为生产日期
                self.query['materialProperty']['receivedTime'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))  # 修改为当前日期
                self.query['materialProperty']['inboundTime'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))  # 修改为当前日期
                self.query['materialProperty']['expiredTime'] = str((datetime.datetime.now() + datetime.timedelta(days=60)).strftime('%Y-%m-%d'))  # 当前日期加60天作为生产过期时间
                self.query['materialProperty']['qcStartTime'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))  # 修改为当前日期
                self.query['materialProperty']['preservationDays'] = 90
                self.query['materialProperty']['sourceOrderCode'] = str(cur[i][7])
                self.query['materialProperty']['batchNo'] = str(datetime.datetime.now().strftime('%Y%m%d'))  # str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
                self.query['materialProperty']['supplierId'] = str(cur[i][8])
                self.query['materialProperty']['m_Str1'] = str(ms().getvalue('WMS.WmsEnumerable', 'M_Str1')[0][0])
                self.query['materialProperty']['m_Str2'] = str(ms().getvalue('WMS.WmsEnumerable', 'M_Str2')[0][0])
                self.query['materialProperty']['m_Str3'] = str(ms().getvalue('WMS.WmsEnumerable', 'M_Str3')[0][0])
                self.query['materialProperty']['m_Str4'] = str(ms().getvalue('WMS.WmsEnumerable', 'M_Str4')[0][0])
                self.query['materialProperty']['m_Str5'] = str(ms().getvalue('WMS.WmsEnumerable', 'M_Str5')[0][0])
                self.query['materialProperty']['m_Str6'] = str(ms().getvalue('WMS.WmsEnumerable', 'M_Str6')[0][0])
                self.query['materialProperty']['m_Str7'] = str(ms().getvalue('WMS.WmsEnumerable', 'M_Str7')[0][0])
                self.query['materialProperty']['m_Str8'] = str(ms().getvalue('WMS.WmsEnumerable', 'M_Str8')[0][0])
                self.query['materialProperty']['m_Str9'] = str(ms().getvalue('WMS.WmsEnumerable', 'M_Str9')[0][0])
                self.query['materialProperty']['m_Str10'] = str(ms().getvalue('WMS.WmsEnumerable', 'M_Str10')[0][0])
                # 将self.query复制出来转换为字符串加到querylist列表中，否则self.query会随着每次循环实时变动
                newquery = str(copy(self.query)).encode('utf-8')
                self.querylist1.append(newquery)

        elif self.case_name == 'ActiveReceiptOrder':
            # 从数据库查询最新创建的收货单，同于生效
            openStatsReceiptOrderId = ms().get_all(
                ms().ExecQuery("SELECT Id FROM WMS.ReceiptOrder a WHERE XStatus ='OPEN'"
                               "AND EXISTS(SELECT ReceiptOrderId FROM WMS.ReceiptOrderItem b "
                               "WHERE a.Id=b.ReceiptOrderId)ORDER BY a.CreationTime DESC "))
            self.headers['Content-Length'] = '0'  # 将headers中的'Content-Type'值改为0，用于请求体为空的接口
            spilpath = os.path.split(self.path)  # 拆分路径，将最后部分拆分出来，返回元祖
            # 将拆分后的路径的前面部分和从数据库获取到的receiptOrderId重新组成一个列表,第一个值后面必须以/结尾，否则后续拼凑后的路径会不正确
            self.spilpathlist1 = [spilpath[0] + '/', str(openStatsReceiptOrderId[0][0])]
            self.path = str(os.path.join(self.spilpathlist1[0], self.spilpathlist1[1]))  # 用列表的两部分拼凑成新路径

        elif self.case_name == 'inboundReceive':
            self.querylist2 = []
            # 从数据库查询获取最新创建的状态为生效或收货中的，还未进行收货的收货单明细
            toReceiveCur = ms().getvalue('WMS.ReceiptOrder', 'receiptOrderItemId')
            for i in range(len(toReceiveCur-1)):  # 留一个不收货，让该收货单状态为’部分收货‘
                self.query['ReceiptOrderItemId'] = str(toReceiveCur[i][0])
                self.query['ReceivedPkgQuantity'] = float(toReceiveCur[i][1])
                self.query['LocationId'] = str(ms().transformNone(ms().getvalue('WMS.Location', 'LocationId')[0][0]))
                self.query['Pallet'] = 'TP' + str(ms().getvalue('sequencetest', 'VALUE')[0][0])
                self.query['WorkerId'] = str(toReceiveCur[i][2])
                # 将self.query复制出来转换为字符串加到querylist列表中，否则self.query会随着每次循环实时变动
                newquery = str(copy(self.query)).encode('utf-8')
                self.querylist2.append(newquery)

        elif self.case_name == 'to_profileCheckStation':
            self.querylist3 = []
            # 数据库查询最新创建的状态为收货完成或部分收货的收货单中的已收货的收货明细的托盘号，且托盘不是在上下架、盘点等任务中
            palletCur = ms().get_all(
                ms().ExecQuery("SELECT c.Pallet FROM(SELECT TOP 1 id "
                               "FROM WMS.ReceiptOrder WHERE XStatus IN('RECEIVED','RECEIVEING') "
                               "AND ShelvesStatus='UNPUTAWAY' ORDER BY CreationTime DESC ) a"
                               "INNER JOIN WMS.ReceiptOrderItem b ON a.Id=b.ReceiptOrderId"
                               "INNER JOIN WMS.ReceivedRecord c ON b.Id = c.ReceiptOrderItemId"
                               "INNER JOIN WMS.InventoryDetail d ON c.Pallet = d.Pallet"
                               "INNER JOIN  WMS.Location e ON d.LocationCode = e.Xcode AND e.Loctype='RECEIVE'"
                               "WHERE c.Pallet NOT IN"
                               "(SELECT Pallet FROM WMS.WmsTask WHERE Status NOT IN ('FINISHED','CANCEL'))"))
            Palletlist = []
            # 将查询到的托盘依次添加到Palletlist列表中
            for i in range(len(palletCur)):
                Pallet = palletCur[i][0]
                Palletlist.append(Pallet)
            # 获取入口到外形检测的检测点、异常口配置信息列表
            profileCheckShipConfig = readyaml().readyaml('ShipConfig.yaml')['request']['入口到外形检测']
            shiplist = []
            profileChecklist = []
            for m in range(len(profileCheckShipConfig)):
                ship = profileCheckShipConfig[m]['ship']
                profileCheckStation = profileCheckShipConfig[m]['profileCheckStation']
                shiplist.append(ship)
                profileChecklist.append(profileCheckStation)
            # while循环实现：如果外形检测入库口的数量小于待上架托盘数，则填充入库口列表的值与托盘数一致
            num = 0
            while len(shiplist) < len(Palletlist):
                shiplist.append(shiplist[num])
                profileChecklist.append(profileChecklist[num])
                num = num + 1
            # 循环托盘列表，获取请求体列表
            for n in range(len(Palletlist)):
                self.query['pallet'] = Palletlist[n]
                self.query['fromLocCode'] = shiplist[n]
                newquery = str(copy(self.query)).encode('utf-8')
                self.querylist3.append(newquery)

        elif self.case_name == 'cfmyes_profileCheck':  # 确认部分外形检测任务，部分不确认





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




