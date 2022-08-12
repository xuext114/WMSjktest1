#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查询收货单管理页面列表，包含’只看自己‘查询、普通查询、高级搜索及其组合查询
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
from testCase.inbound.test_1_CreatReceiptOrder import testcreatReceiptOrder

url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'queryReceiptOrder')


@paramunittest.parametrized(*casexls)
class testqueryReceiptOrder(unittest.TestCase):
    def setParameters(self, case_name, method, path, query):
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = eval(query)
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()
        self.querylist = []

        # 查询存在于收货单的物料信息
        self.Material = ms().get_all(ms().ExecQuery("SELECT * FROM (SELECT DISTINCT a.MaterialId,b.XCode,"
                                                    "b.XName, b.Barcode, b.MnemonicCode FROM "
                                                    "WMS.ReceiptOrderItem a INNER JOIN WMS.Material b "
                                                    "ON a.MaterialId = b.Id AND b.XCode<>'0000') a "
                                                    "ORDER BY newid() "))

        # 从数据库查询可用于赋值单据类型参数的单据类型id
        self.billType = ms().get_all(ms().ExecQuery("SELECT id FROM WMS.BillType WHERE XType= 'RECEIVE' "
                                                    "AND XName IN ('成品入库','生产入库','采购入库') "
                                                    "ORDER BY XName;"))

        # 从数据库查询收货单涉及供应商
        self.SupplierId = ms().get_all(ms().ExecQuery("SELECT SupplierId FROM(SELECT DISTINCT SupplierId "
                                                      "FROM WMS.ReceiptOrder)a ORDER BY newid()"))

        # 从数据库查询收货单包含的发货人
        self.FromName = ms().get_all(ms().ExecQuery("SELECT FromName FROM (SELECT DISTINCT FromName "
                                                    "FROM WMS.ReceiptOrder WHERE FromName IS NOT NULL) a "
                                                    "ORDER BY  newid()"))

        # 查询收货单单据编号
        self.XCode = ms().get_all(ms().ExecQuery("SELECT XCode FROM(SELECT DISTINCT XCode FROM "
                                                 "WMS.ReceiptOrder) a ORDER BY newid()"))

        # 查询当前收货单的最大与最小期望数量
        self.ExpectedPkgQuantity1 = ms().get_all(ms().ExecQuery("SELECT max(ExpectedPkgQuantity) maxExpectedPkgQuantity,"
                                                                "min(ExpectedPkgQuantity) minExpectedPkgQuantity "
                                                                "FROM WMS.ReceiptOrder"))

        self.ExpectedPkgQuantity2 = ms().get_all(ms().ExecQuery("SELECT ExpectedPkgQuantity FROM (SELECT DISTINCT "
                                                                "ExpectedPkgQuantity FROM WMS.ReceiptOrder) a "
                                                                "ORDER BY newid()"))

        # 查询当前收货单的最大与最小收货数量
        self.ReceivedPkgQuantity = ms().get_all(ms().ExecQuery("SELECT max(ReceivedPkgQuantity) maxReceivedPkgQuantity,"
                                                               "min(ReceivedPkgQuantity) minReceivedPkgQuantity "
                                                               "FROM WMS.ReceiptOrder"))

        # 查询当前收货单的最大与最小上架数量
        self.MovedPkgQuantity = ms().get_all(ms().ExecQuery("SELECT max(MovedPkgQuantity) maxMovedPkgQuantity,"
                                                            "min(MovedPkgQuantity) minMovedPkgQuantity "
                                                            "FROM WMS.ReceiptOrder"))

        # 查询当前收货单中涉及的相关单据编号
        self.RelatedBill1 = ms().get_all(ms().ExecQuery("SELECT RelatedBill1 FROM (SELECT DISTINCT RelatedBill1 "
                                                        "FROM WMS.ReceiptOrder WHERE RelatedBill1 IS NOT NULL "
                                                        "AND RelatedBill1<>'') a ORDER BY newid()"))

        # 从数据库中查询收货单中扩展属性1的值
        self.str1 = ms().get_all(ms().ExecQuery("SELECT str1 FROM (SELECT DISTINCT str1 FROM WMS.ReceiptOrder "
                                                "WHERE str1 IS NOT NULL) a ORDER BY newid()"))

        # 从数据库中查询收货单中涉及扩展属性2的值
        self.str2 = ms().get_all(ms().ExecQuery("SELECT str2 FROM (SELECT DISTINCT str2 FROM "
                                                "WMS.ReceiptOrder WHERE str2 IS NOT NULL) a ORDER BY newid()"))

        # 从数据库中查询收货单中扩展属性3的值
        self.str3 = ms().get_all(ms().ExecQuery("SELECT str3 FROM (SELECT DISTINCT str3 FROM "
                                                "WMS.ReceiptOrder WHERE str3 IS NOT NULL) a ORDER BY newid()"))

        # 从数据库中查询收货单中扩展属性4的值
        self.str4 = ms().get_all(ms().ExecQuery("SELECT str4 FROM (SELECT DISTINCT str4 FROM "
                                                "WMS.ReceiptOrder WHERE str4 IS NOT NULL) a ORDER BY newid()"))

        # 从数据库中查询收货单中扩展属性5的值
        self.str5 = ms().get_all(ms().ExecQuery("SELECT str5 FROM (SELECT DISTINCT str5 FROM "
                                                "WMS.ReceiptOrder WHERE str5 IS NOT NULL) a ORDER BY newid()"))

        # 从数据库中查询收货单中扩展属性6的值
        self.str6 = ms().get_all(ms().ExecQuery("SELECT str6 FROM (SELECT DISTINCT str6 FROM "
                                                "WMS.ReceiptOrder WHERE str6 IS NOT NULL) a ORDER BY newid()"))

        # 从数据库中查询收货单中扩展属性7的值
        self.str7 = ms().get_all(ms().ExecQuery("SELECT str7 FROM (SELECT DISTINCT str7 FROM "
                                                "WMS.ReceiptOrder WHERE str7 IS NOT NULL) a ORDER BY newid()"))

        # 从数据库中查询收货单中扩展属性8的值
        self.str8 = ms().get_all(ms().ExecQuery("SELECT str8 FROM (SELECT DISTINCT str8 FROM "
                                                "WMS.ReceiptOrder WHERE str8 IS NOT NULL) a ORDER BY newid()"))

        # 从数据库中查询收货单中扩展属性9的值
        self.str9 = ms().get_all(ms().ExecQuery("SELECT str9 FROM (SELECT DISTINCT str9 FROM "
                                                "WMS.ReceiptOrder WHERE str9 IS NOT NULL) a ORDER BY newid()"))

        # 从数据库中查询收货单中扩展属性9的值
        self.str10 = ms().get_all(ms().ExecQuery("SELECT str10 FROM (SELECT DISTINCT str10 FROM "
                                                 "WMS.ReceiptOrder WHERE str10 IS NOT NULL) a ORDER BY newid()"))

        self.creator = ms().get_all(ms().ExecQuery("SELECT Creator FROM(SELECT DISTINCT Creator FROM "
                                                   "WMS.ReceiptOrder WHERE Creator IS NOT NULL)a ORDER BY newid()"))

        self.lastModifier = ms().get_all(ms().ExecQuery("SELECT LastModifier FROM(SELECT DISTINCT LastModifier FROM "
                                                        "WMS.ReceiptOrder WHERE LastModifier IS NOT NULL)a "
                                                        "ORDER BY newid()"))

        self.CreationTime = ms().get_all(ms().ExecQuery("SELECT max(CreationTime) maxCreationTime,"
                                                        "min(CreationTime) minCreationTime "
                                                        "FROM WMS.ReceiptOrder"))

        self.LastModificationTime = ms().get_all(ms().ExecQuery("SELECT max(LastModificationTime) maxLastModificationTime, "
                                                                "min(LastModificationTime) minLastModificationTime "
                                                                "FROM WMS.ReceiptOrder"))

        # '************************************修改测试用例中的参数信息************************************'
        #  若需要人工修改，不需要程序修改，则注销下面代码
        if self.case_name == 'queryMaterial_code':
            self.query['condition']['xCode']['like'] = '%'+str(ms().transformNone(self.Material[0][1]))[0:4]+'%'  # 截取4位用于模糊查询
            self.query['condition']['xName']['like'] = '%'+str(ms().transformNone(self.Material[0][1]))[0:4]+'%'
            self.query['condition']['barcode']['like'] = str(ms().transformNone(self.Material[0][1]))[0:4]+'%'
            self.query['condition']['mnemonicCode']['like'] = str(ms().transformNone(self.Material[0][1]))[0:4]+'%'
        elif self.case_name == 'queryMaterial_name':
            self.query['condition']['xCode']['like'] = '%'+str(ms().transformNone(self.Material[0][2]))[0:2]+'%'  # 截取2位用于模糊查询
            self.query['condition']['xName']['like'] = '%'+str(ms().transformNone(self.Material[0][2]))[0:2]+'%'
            self.query['condition']['barcode']['like'] = str(ms().transformNone(self.Material[0][2]))[0:2]+'%'
            self.query['condition']['mnemonicCode']['like'] = str(ms().transformNone(self.Material[0][2]))[0:2]+'%'
        elif self.case_name == 'queryreceiptOrder_Material':
            self.query['condition']['receiptOrderItem.materialId']['='] = str(ms().transformNone(self.Material[0][0]))
        elif self.case_name == 'queryreceiptOrder_Xcode':
            self.query['condition']['xCode']['like'] = '%'+str(ms().transformNone(self.XCode[0][0]))[0:9]+'%'  # 截取前9位模糊查询
        elif self.case_name == 'queryreceiptOrder_BillType_CG':
            self.query['condition']['billTypeId']['='] = str(ms().transformNone(self.billType[0][0]))
        elif self.case_name == 'queryreceiptOrder_BillType_CP':
            self.query['condition']['billTypeId']['='] = str(ms().transformNone(self.billType[1][0]))
        elif self.case_name == 'queryreceiptOrder_BillType_SC':
            self.query['condition']['billTypeId']['='] = str(ms().transformNone(self.billType[2][0]))
        elif self.case_name == 'queryreceiptOrder_Supplier':
            self.query['condition']['supplierId']['='] = str(ms().transformNone(self.SupplierId[0][0]))
        elif self.case_name == 'queryreceiptOrder_expectedPkgQuantity':
            self.query['condition']['expectedPkgQuantity']['>='] = float(
                ms().transformNone(self.ExpectedPkgQuantity1[0][0]))+10
            self.query['condition']['expectedPkgQuantity']['<='] = float(
                ms().transformNone(self.ExpectedPkgQuantity1[0][1])) - 10
        elif self.case_name == 'queryreceiptOrder_expectedPkgQuantity_Float':
            self.query['condition']['expectedPkgQuantity']['>='] = float(
                ms().transformNone(self.ExpectedPkgQuantity1[0][0]))+9.99
            self.query['condition']['expectedPkgQuantity']['<='] = float(
                ms().transformNone(self.ExpectedPkgQuantity1[0][1]))-9.99
        elif self.case_name == 'queryreceiptOrder_expectedPkgQuantity_lessnull':
            self.query['condition']['expectedPkgQuantity']['>='] = float(
                ms().transformNone(self.ExpectedPkgQuantity2[0][0]))
        elif self.case_name == 'queryreceiptOrder_expectedPkgQuantity_morenull':
            self.query['condition']['expectedPkgQuantity']['<='] = float(
                ms().transformNone(self.ExpectedPkgQuantity2[0][0]))
        elif self.case_name == 'queryreceiptOrder_expectedPkgQuantity_resultnull':
            self.query['condition']['expectedPkgQuantity']['>='] = float(
                ms().transformNone(self.ExpectedPkgQuantity1[0][1]))
            self.query['condition']['expectedPkgQuantity']['<='] = float(
                ms().transformNone(self.ExpectedPkgQuantity1[0][0]))
        elif self.case_name == 'queryreceiptOrder_expectedPkgQuantity_valueequal':
            self.query['condition']['expectedPkgQuantity']['>='] = float(
                ms().transformNone(self.ExpectedPkgQuantity1[0][0]))
            self.query['condition']['expectedPkgQuantity']['<='] = float(
                ms().transformNone(self.ExpectedPkgQuantity1[0][0]))
        elif self.case_name == 'queryreceiptOrder_receivedPkgQuantity':
            self.query['condition']['receivedPkgQuantity']['>='] = float(
                ms().transformNone(self.ReceivedPkgQuantity[0][0]))+10
            self.query['condition']['receivedPkgQuantity']['<='] = float(
                ms().transformNone(self.ReceivedPkgQuantity[0][1]))-10
        elif self.case_name == 'queryreceiptOrder_movedPkgQuantity':
            self.query['condition']['movedPkgQuantity']['>='] = float(
                ms().transformNone(self.MovedPkgQuantity[0][0]))+10
            self.query['condition']['movedPkgQuantity']['<='] = float(
                ms().transformNone(self.MovedPkgQuantity[0][1]))-10
        elif self.case_name == 'queryreceiptOrder_relatedBill1':
            self.query['condition']['relatedBill1']['like'] = '%' + str(ms().transformNone(self.RelatedBill1[0][0]))[0:5]+'%'
        elif self.case_name == 'queryreceiptOrder_str1':
            self.query['condition']['str1']['like'] = '%' + str(ms().transformNone(self.str1[0][0]))[0:4] + '%'
        elif self.case_name == 'queryreceiptOrder_str2':
            self.query['condition']['str2']['like'] = '%' + str(ms().transformNone(self.str2[0][0]))[0:4] + '%'
        elif self.case_name == 'queryreceiptOrder_str3':
            self.query['condition']['str3']['like'] = '%' + str(ms().transformNone(self.str3[0][0]))[0:4] + '%'
        elif self.case_name == 'queryreceiptOrder_str4':
            self.query['condition']['str4']['like'] = '%' + str(ms().transformNone(self.str4[0][0]))[0:4] + '%'
        elif self.case_name == 'queryreceiptOrder_fromName':
            self.query['condition']['fromName']['like'] = '%' + str(ms().transformNone(self.FromName[0][0]))[0:2] + '%'
        elif self.case_name == 'queryreceiptOrder_creator':
            self.query['condition']['creator']['like'] = '%' + str(ms().transformNone(self.creator[0][0]))[0:2] + '%'
        elif self.case_name == 'queryreceiptOrder_lastModifier':
            self.query['condition']['lastmodifier']['like'] = '%' + str(ms().transformNone(self.lastModifier[0][0]))[0:2] + '%'
        elif self.case_name == 'queryreceiptOrder_CreationTime':
            self.query['condition']['creationTime']['>='] = self.CreationTime[0][0].strftime('%Y/%m/%d %H:%M:%S') # +datetime.timedelta(days=1)
            self.query['condition']['creationTime']['<='] = self.CreationTime[0][0].strftime('%Y/%m/%d %H:%M:%S') # -datetime.timedelta(days=1)
        elif self.case_name == 'queryreceiptOrder_LastModificationTime':
            self.query['condition']['lastModificationTime']['>='] = self.LastModificationTime[0][0].strftime(
                '%Y/%m/%d %H:%M:%S') #+datetime.timedelta(days=1)  # 小于等于最小更新时间加1天
            self.query['condition']['lastModificationTime']['<='] = self.LastModificationTime[0][0].strftime(
                '%Y/%m/%d %H:%M:%S') #-datetime.timedelta(days=1)  # 大于等于最大更新时间减1天
        elif self.case_name == 'queryreceiptOrder_combination1':
            self.query['condition']['xCode']['like'] = '%' + str(ms().transformNone(self.XCode[0][0]))[0:9] + '%'
            self.query['condition']['billTypeId']['='] = str(ms().transformNone(self.billType[2][0]))
        elif self.case_name == 'queryreceiptOrder_combination2':
            self.query['condition']['expectedPkgQuantity']['>='] = float(
                ms().transformNone(self.ExpectedPkgQuantity1[0][0]))
            self.query['condition']['expectedPkgQuantity']['<='] = float(
                ms().transformNone(self.ExpectedPkgQuantity1[0][0]))
            self.query['condition']['supplierId']['='] = str(ms().transformNone(self.SupplierId[0][0]))
        elif self.case_name == 'authorizeQuery_Material':
            self.query['condition']['receiptOrderItem.materialId']['='] = str(ms().transformNone(self.Material[0][0]))
        elif self.case_name == 'authorizeQuery_Xcode':
            self.query['condition']['xCode']['like'] = '%'+str(ms().transformNone(self.XCode[0][0]))[0:9]+'%'
        elif self.case_name == 'authorizeQuery_BillType_SC':
            self.query['condition']['billTypeId']['='] = str(ms().transformNone(self.billType[2][0]))
        elif self.case_name == 'authorizeQuery_expectedPkgQuantity':
            self.query['condition']['expectedPkgQuantity']['>='] = float(
                ms().transformNone(self.ExpectedPkgQuantity1[0][0]))+10
            self.query['condition']['expectedPkgQuantity']['<='] = float(
                ms().transformNone(self.ExpectedPkgQuantity1[0][0])) - 10

        self.query = str(self.query).encode('utf-8')

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name)
        # temp = testcreatReceiptOrder()
        # temp.sttUp()
        # temp.checkResult()
        # temp.tearDown()

    def testqueryReceiptOrder(self):
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
            if self.case_name == 'queryMaterial_code':
                print('测试用例名：', self.case_name)
                print('查询关键字是：', self.Material[0][1][0:4])
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询物料
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT xcode FROM WMS.Material "
                                                            "WHERE XCode LIKE '%%%s%%'" % self.Material[0][1][0:4]))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的物料Xcode中不包含查询关键字的数据生成到jkresult列表中
                jkresult = [info['data'][i]['xCode'] for i in range(len(info['data']))
                            if self.Material[0][1][0:4] not in info['data'][i]['xCode']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按物料Xcode关键字查询，接口返回的物料有不包含查询关键字的数据！'),
                                                self.assertEqual(len(dbqueryresult), len(info['data']),
                                                                 '按物料Xcode关键字查询，接口返回的物料数量与在数据库查询数量不一致'))))
            elif self.case_name == 'queryMaterial_name':
                print('测试用例名：', self.case_name)
                print('查询关键字是：', self.Material[0][2][0:2])
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询物料
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT xname FROM WMS.Material "
                                                            "WHERE Xname LIKE '%%%s%%'" % self.Material[0][2][0:2]))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的物料Xname中不包含查询关键字的数据生成到jkresult列表中
                jkresult = [info['data'][i]['xName'] for i in range(len(info['data']))
                            if self.Material[0][2][0:2] not in info['data'][i]['xName']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按物料xName关键字查询，接口返回的物料有不包含查询关键字的数据！'),
                                                self.assertEqual(len(dbqueryresult), len(info['data']),
                                                                 '按物料xName关键字查询，接口返回物料数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryMaterial_specialcharacter_':
                print('测试用例名：', self.case_name)
                print('查询关键字是：', '_')
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询物料
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.Material WHERE xCode "
                                                            "LIKE '%[_]%' OR xName LIKE '%[_]%' "
                                                            "OR barcode = '%[_]%' OR mnemonicCode "
                                                            "= '%[_]%'"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的物料中不包含查询关键字的数据生成到jkresult列表中
                jkresult = [info['data'][i]['xName'] for i in range(len(info['data']))
                            if '_' not in info['data'][i]['xName'] or '_' not in info['data'][i]['xCode']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按关键字’_‘查询，接口返回的物料有不包含查询关键字的数据！'),
                                                self.assertEqual(len(dbqueryresult), len(info['data']),
                                                                 '按关键字’_‘查询，接口返回物料数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryMaterial_specialcharacter%':
                print('测试用例名：', self.case_name)
                print('查询关键字是：', '%')
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询物料
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.Material WHERE xCode "
                                                            "LIKE '%[%]%' OR xName LIKE '%[%]%' "
                                                            "OR barcode = '%[%]%' OR mnemonicCode "
                                                            "= '%[%]%'"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的物料中不包含查询关键字的数据生成到jkresult列表中
                jkresult = [info['data'][i]['xName'] for i in range(len(info['data']))
                            if '%' not in info['data'][i]['xName'] or '%' not in info['data'][i]['xCode']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按关键字’%‘查询，接口返回的物料有不包含查询关键字的数据！'),
                                                self.assertEqual(len(dbqueryresult), len(info['data']),
                                                                 '按关键字’%‘查询，接口返回的物料数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryMaterial_specialcharacter%':
                print('测试用例名：', self.case_name)
                print('查询关键字是：', '%')
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询物料
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.Material WHERE xCode "
                                                            "LIKE '%*%' OR xName LIKE '%*%' "
                                                            "OR barcode = '%*%' OR mnemonicCode "
                                                            "= '%*%'"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的物料中不包含查询关键字的数据生成到jkresult列表中
                jkresult = [info['data'][i]['xName'] for i in range(len(info['data']))
                            if '*' not in info['data'][i]['xName'] or '*' not in info['data'][i]['xCode']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按关键字’*‘查询，接口返回的物料有不包含查询关键字的数据！'),
                                                self.assertEqual(len(dbqueryresult), len(info['data']),
                                                                 '按关键字’*‘查询，接口返回的物料数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_all':
                print('测试用例名：', self.case_name)
                print('查询关键字是：', '无查询关键字，全查')
                print('查询接口返回：', info)

                # 在数据库查询物料
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT XCode FROM WMS.ReceiptOrder"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []


                # 断言数据库查询结果数据量与接口返回数据量是否一致
                self.assertEqual(len(dbqueryresult), info['totalCount'], '全查时，接口返回的物料数量与在数据库查询数量不一致')

            elif self.case_name == 'queryreceiptOrder_Material':
                print('测试用例名：', self.case_name)
                print('查询对应物料的ID：', self.Material[0][0])
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT MaterialId FROM WMS.ReceiptOrderItem "
                                                            "WHERE materialId ='%s'" % self.Material[0][0]))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的物料id数据生成到jkresult列表中
                jkresult1 = [info['data'][m]['receiptOrderItem'][n]['materialId'] for m in range(
                    len(info['data'])) for n in range(len(info['data'][m]['receiptOrderItem']))]
                # 将接口返回物料id数据与查询id进行比对，比对不上则加入列表jkresult2
                jkresult2 = [i for i in jkresult1 if i == self.Material[0][0]]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult2,
                                                                 '按物料id查询，接口返回的物料有不是该物料ID的数据！'),
                                                self.assertEqual(len(dbqueryresult), len(jkresult1),
                                                                 '按物料id查询，接口返回物料数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_Xcode':
                print('测试用例名：', self.case_name)
                print('查询关键字是：', self.XCode[0][0][0:9])
                print('查询接口返回：', info)
                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder "
                                                            "WHERE XCode LIKE '%%%s%%'" % self.XCode[0][0][0:9]))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单XCode中不包含查询关键字的数据生成到jkresult列表中
                jkresult = [info['data'][i]['xCode'] for i in range(len(info['data']))
                            if self.XCode[0][0][0:9] not in info['data'][i]['xCode']]
                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in (self.assertFalse(jkresult,
                                                                  '按收货单XCode关键字查询，接口返回的收货单Code有不包含查询关键字的数据！'),
                                                 self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                  '按收货单XCode关键字查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_Xcode_specialcharacter_':
                print('测试用例名：', self.case_name)
                print('查询关键字是：', '_')
                print('查询接口返回：', info)
                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder "
                                                            "WHERE XCode LIKE '%[_]%'"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单XCode中不包含查询关键字的数据生成到jkresult列表中
                jkresult = [info['data'][i]['xCode'] for i in range(len(info['data']))
                            if '_' not in info['data'][i]['xCode']]
                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in (self.assertFalse(jkresult,
                                                                  '按_查询，接口返回的收货单Code有不包含查询关键字的数据！'),
                                                 self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                  '按_查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_Xcode_specialcharacter%':
                print('测试用例名：', self.case_name)
                print('查询关键字是：', '%')
                print('查询接口返回：', info)
                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder "
                                                            "WHERE XCode LIKE '%[%]%'"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单XCode中不包含查询关键字的数据生成到jkresult列表中
                jkresult = [info['data'][i]['xCode'] for i in range(len(info['data']))
                            if '%' not in info['data'][i]['xCode']]
                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in (self.assertFalse(jkresult,
                                                                  '按%查询，接口返回的收货单Code有不包含查询关键字的数据！'),
                                                 self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                  '按%查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_Xcode_specialcharacter*':
                print('测试用例名：', self.case_name)
                print('查询关键字是：', '*')
                print('查询接口返回：', info)
                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder "
                                                            "WHERE XCode LIKE '%[*]%'"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单XCode中不包含查询关键字的数据生成到jkresult列表中
                jkresult = [info['data'][i]['xCode'] for i in range(len(info['data']))
                            if '*' not in info['data'][i]['xCode']]
                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in (self.assertFalse(jkresult,
                                                                  '按*查询，接口返回的收货单Code有不包含查询关键字的数据！'),
                                                 self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                  '按*查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_Xcode_resultnull':
                print('测试用例名：', self.case_name)
                print('查询关键字是：', 'RO9999')
                print('查询接口返回：', info)

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(info['data'], '接口应无查询结果返回，但实际有结果返回！')

            elif self.case_name == 'queryreceiptOrder_BillType_CG':
                print('测试用例名：', self.case_name)
                print('查询采购入库单据类型id：', self.billType[0][0])
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder "
                                                            "WHERE BillTypeId ='%s'" % str(self.billType[0][0])))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单数据中不是查询单据的数据添加到jkresult列表中
                jkresult = [info['data'][i]['billTypeId'] for i in range(len(info['data']))
                            if str(self.billType[0][0]) not in info['data'][i]['billTypeId']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按‘采购入库’单据类型查询，接口返回的收货单有不是该单据类型的数据！'),
                                                self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                 '按‘采购入库’入库单据类型查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_BillType_CP':
                print('测试用例名：', self.case_name)
                print('查询成品入库单据类型id：', self.billType[1][0])
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder "
                                                            "WHERE BillTypeId ='%s'" % str(self.billType[1][0])))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单数据中不是查询单据的数据添加到jkresult列表中
                jkresult = [info['data'][i]['billTypeId'] for i in range(len(info['data']))
                            if str(self.billType[1][0]) not in info['data'][i]['billTypeId']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按‘成品入库’单据类型查询，接口返回的收货单有不是该单据类型的数据！'),
                                                self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                 '按‘成品入库’入库单据类型查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_BillType_SC':
                print('测试用例名：', self.case_name)
                print('查询生产入库单据类型id：', self.billType[2][0])
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder "
                                                            "WHERE BillTypeId ='%s'" % str(self.billType[2][0])))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单数据中不是查询单据的数据添加到jkresult列表中
                jkresult = [info['data'][i]['billTypeId'] for i in range(len(info['data']))
                            if str(self.billType[2][0]) not in info['data'][i]['billTypeId']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按‘生产入库’单据类型查询，接口返回的收货单有不是该单据类型的数据！'),
                                                self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                 '按‘生产入库’入库单据类型查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_Supplier':
                print('测试用例名：', self.case_name)
                print('查询供应商id：', self.SupplierId[0][0])
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder "
                                                            "WHERE SupplierId ='%s'" % str(self.SupplierId[0][0])))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单数据中不是查询单据的数据添加到jkresult列表中
                jkresult = [info['data'][i]['supplierId'] for i in range(len(info['data']))
                            if str(self.SupplierId[0][0]) not in info['data'][i]['supplierId']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按供应商查询，接口返回的收货单有不是该供应商的数据！'),
                                                self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                 '按供应商查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_xStatus_OPEN':
                print('测试用例名：', self.case_name)
                print('查询收货单状态：', 'OPEN')
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder WHERE XStatus='OPEN'"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单数据中不是查询单据的数据添加到jkresult列表中
                jkresult = [info['data'][i]['xStatus'] for i in range(len(info['data']))
                            if 'OPEN' not in info['data'][i]['xStatus']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按收货单’OPEN‘状态查询，接口返回的收货单有不是该状态的数据！'),
                                                self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                 '按收货单’OPEN‘状态查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_xStatus_ACTIVE':
                print('测试用例名：', self.case_name)
                print('查询收货单状态：', 'ACTIVE')
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder WHERE XStatus='ACTIVE'"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单数据中不是查询单据的数据添加到jkresult列表中
                jkresult = [info['data'][i]['xStatus'] for i in range(len(info['data']))
                            if 'ACTIVE' not in info['data'][i]['xStatus']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按收货单’ACTIVE‘状态查询，接口返回的收货单有不是该状态的数据！'),
                                                self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                 '按收货单’ACTIVE‘状态查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_xStatus_RECEIVING':
                print('测试用例名：', self.case_name)
                print('查询收货单状态：', 'RECEIVING')
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder WHERE XStatus='RECEIVING'"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单数据中不是查询单据的数据添加到jkresult列表中
                jkresult = [info['data'][i]['xStatus'] for i in range(len(info['data']))
                            if 'RECEIVING' not in info['data'][i]['xStatus']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按收货单’RECEIVING‘状态查询，接口返回的收货单有不是该状态的数据！'),
                                                self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                 '按收货单’RECEIVING‘状态查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_xStatus_RECEIVED':
                print('测试用例名：', self.case_name)
                print('查询收货单状态：', 'RECEIVED')
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder WHERE XStatus='RECEIVED'"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单数据中不是查询单据的数据添加到jkresult列表中
                jkresult = [info['data'][i]['xStatus'] for i in range(len(info['data']))
                            if 'RECEIVED' not in info['data'][i]['xStatus']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按收货单’RECEIVED‘状态查询，接口返回的收货单有不是该状态的数据！'),
                                                self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                 '按收货单’RECEIVED‘状态查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_xStatus_CANCELED':
                print('测试用例名：', self.case_name)
                print('查询收货单状态：', 'CANCELED')
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder WHERE XStatus='CANCELED'"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单数据中不是查询单据的数据添加到jkresult列表中
                jkresult = [info['data'][i]['xStatus'] for i in range(len(info['data']))
                            if 'CANCELED' not in info['data'][i]['xStatus']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按收货单’CANCELED‘状态查询，接口返回的收货单有不是该状态的数据！'),
                                                self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                 '按收货单’CANCELED‘状态查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_shelvesStatus_UNPUTAWAY':
                print('测试用例名：', self.case_name)
                print('查询上架状态：', 'UNPUTAWAY')
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder "
                                                            "WHERE shelvesStatus='UNPUTAWAY'"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单数据中不是查询单据的数据添加到jkresult列表中
                jkresult = [info['data'][i]['shelvesStatus'] for i in range(len(info['data']))
                            if 'UNPUTAWAY' not in info['data'][i]['shelvesStatus']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按收货单上架状态’UNPUTAWAY‘查询，接口返回的收货单有不是该状态的数据！'),
                                                self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                 '按收货单上架状态’UNPUTAWAY‘查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_shelvesStatus_PUTAWAY':
                print('测试用例名：', self.case_name)
                print('查询上架状态：', 'PUTAWAY')
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder "
                                                            "WHERE shelvesStatus='PUTAWAY'"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单数据中不是查询单据的数据添加到jkresult列表中
                jkresult = [info['data'][i]['shelvesStatus'] for i in range(len(info['data']))
                            if 'PUTAWAY' not in info['data'][i]['shelvesStatus']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按收货单上架状态’PUTAWAY‘查询，接口返回的收货单有不是该状态的数据！'),
                                                self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                 '按收货单上架状态’PUTAWAY‘查询，接口返回收货单数量与在数据库查询数量不一致'))))

            elif self.case_name == 'queryreceiptOrder_shelvesStatus_FINISHED':
                print('测试用例名：', self.case_name)
                print('查询上架状态：', 'FINISHED')
                print('查询接口返回：', info)

                # 根据本次查询关键字在数据库查询收货单
                dbqueryresult = ms().get_all(ms().ExecQuery("SELECT * FROM WMS.ReceiptOrder "
                                                            "WHERE shelvesStatus='FINISHED'"))
                if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
                    dbqueryresult = []

                # 将接口返回的收货单数据中不是查询单据的数据添加到jkresult列表中
                jkresult = [info['data'][i]['shelvesStatus'] for i in range(len(info['data']))
                            if 'FINISHED' not in info['data'][i]['shelvesStatus']]

                # 断言查询结果数据量和查询字段信息是否与查询关键字一致
                self.assertFalse(any(x for x in(self.assertFalse(jkresult,
                                                                 '按收货单上架状态’FINISHED‘查询，接口返回的收货单有不是该状态的数据！'),
                                                self.assertEqual(len(dbqueryresult), info['totalCount'],
                                                                 '按收货单上架状态’FINISHED‘查询，接口返回收货单数量与在数据库查询数量不一致'))))

            # elif self.case_name == 'queryreceiptOrder_expectedPkgQuantity':
            #     print('测试用例名：', self.case_name)
            #     print('查询期望数量范围：', '>={0:.2f},<={1:.2f}'.format(float(self.ExpectedPkgQuantity1[0][0])+10,
            #                                                     float(self.ExpectedPkgQuantity1[0][0])-10))
            #     print('查询接口返回：', info)
            #
            #     # 根据本次查询关键字在数据库查询收货单
            #     dbqueryresult = ms().get_all(ms().ExecQuery("SELECT ExpectedPkgQuantity FROM WMS.ReceiptOrder "
            #                                                 "WHERE ExpectedPkgQuantity>={0:.2f} "
            #                                                 "AND ExpectedPkgQuantity<={1:.2f}".
            #                                                 format(float(self.ExpectedPkgQuantity1[0][0])+10,
            #                                                        float(self.ExpectedPkgQuantity1[0][0])-10)))
            #     if len(dbqueryresult) == 1 and dbqueryresult[0][0] == '':
            #         dbqueryresult = []
            #
            #     # 将接口返回的收货单数据中不是查询单据的数据添加到jkresult列表中
            #     jkresult1 = [info['data'][i]['expectedPkgQuantity'] for i in range(len(info['data']))
            #                 if float(self.ExpectedPkgQuantity1[0][0])+10 > info['data'][i]['expectedPkgQuantity']]
            #     jkresult2 = [info['data'][i]['expectedPkgQuantity'] for i in range(len(info['data']))
            #                 if float(self.ExpectedPkgQuantity1[0][1])-10 < info['data'][i]['expectedPkgQuantity']]
            #     # 断言查询结果数据量和查询字段信息是否与查询关键字一致
            #     self.assertFalse(any(x for x in(self.assertFalse(jkresult,
            #                                                      '按收货单上架状态’FINISHED‘查询，接口返回的收货单有不是该状态的数据！'),
            #                                     self.assertEqual(len(dbqueryresult), info['totalCount'],
            #                                                      '按收货单上架状态’FINISHED‘查询，接口返回收货单数量与在数据库查询数量不一致'))))


if __name__ == '__main__':
    unittest.main()



