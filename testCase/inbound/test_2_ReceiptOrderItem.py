#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对当前最新的状态为打开的未新建收货明细的收货单新建收货明细，为保证测试数据充分，至少保证新建5个收货明细（基础数据除托盘外有5个以上物料即可）
从数据库物料基础表中随机取10个非托盘的物料新建，
数量从[10, 20, 30, 40, 50]中随机取
从参数必填校验、类型校验、格式校验及业务校验方面进行测试验证
"""

import ast
import unittest
from common.configHttp import RunMain
import paramunittest
from testFile import geturlParams
from testFile import readExcel
from testFile.readyaml import readyaml
from common.configDb import MSSQL as ms
import datetime
import random
from copy import copy
import uuid
from decimal import Decimal

url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'creatreceiptOrderItem')


@paramunittest.parametrized(*casexls)
class testcreatReceiptOrderItem(unittest.TestCase):
    def setParameters(self, case_name, case_name_ch, method, path, query):
        self.case_name = str(case_name)
        self.case_name_ch = str(case_name_ch)
        self.path = str(path)
        self.query = eval(query)
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()
        self.querylist = []

        cur = ms().getvalue('WMS.ReceiptOrder', 'receiptOrderItem')
        cur2 = ms().getvalue('WMS.ReceiptOrder', 'receiptOrderItem2')
        if self.case_name == 'creatreceiptOrderItem':  # 正常新增收货单明细，取一个最新的、打开状态的收货主单据，循环10个（如果有）物料创建收货明细
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
                self.querylist.append(newquery)
            # print('新建收货单明细项接口的请求体列表为：', self.querylist)

        elif self.case_name == 'creatreceiptOrderItem_parametersNotnull':  # 其他测试用例取第二新的、状态为打开的主单据，作新增明细测试用
            self.query['receiptOrderItem']['receiptOrderId'] = str(cur2[0][0])
            self.query['receiptOrderItem']['materialId'] = str(cur2[0][9])
            self.query['receiptOrderItem']['packageUnitId'] = str(cur2[0][24])
            self.query['receiptOrderItem']['packageUnit']['materialId'] = str(cur2[0][9])
            self.query['receiptOrderItem']['packageUnit']['id'] = str(cur2[0][24])
            self.query['receiptOrderItem']['expectedPkgQuantity'] = random.choice([10, 20, 30, 40, 50])
            self.query['receiptOrderItem']['receivedPkgQuantity'] = 0
            self.query['receiptOrderItem']['movedPkgQuantity'] = 0
            self.query['receiptOrderItem']['receiptOrder']['id'] = str(cur2[0][0])
            self.query['receiptOrderItem']['receiptOrder']['xCode'] = str(cur2[0][7])
            self.query['receiptOrderItem']['material']['id'] = str(cur2[0][9])
            self.query['receiptOrderItem']['material']['packageUnit'][0]['materialId'] = str(cur2[0][9])
            self.query['receiptOrderItem']['material']['packageUnit'][0]['id'] = str(cur2[0][24])
            # self.query['receiptOrderItem']['material']['materialPropertyRule']['id'] = str(cur2[0][36])
            # self.query['receiptOrderItem']['material']['materialCategory']['id'] = str(cur2[0][16])
            self.query['materialProperty']['materialId'] = str(cur2[0][9])
            self.query['materialProperty']['sourceOrderCode'] = str(cur2[0][7])
            self.query = str(self.query).encode('utf-8')

        else:  # 其他测试用例取第二新的、状态为打开的主单据作新增明细测试用
            self.query['receiptOrderItem']['receiptOrderId'] = str(cur2[0][0])
            self.query['receiptOrderItem']['materialId'] = str(cur2[0][9])
            self.query['receiptOrderItem']['packageUnitId'] = str(cur2[0][24])
            self.query['receiptOrderItem']['expectedPkgQuantity'] = random.choice([10, 20, 30, 40, 50])
            self.query['receiptOrderItem']['receiptOrder']['ownerId'] = str(cur2[0][5])
            self.query['receiptOrderItem']['receiptOrder']['supplierId'] = str(cur2[0][8])
            self.query['receiptOrderItem']['receiptOrder']['xCode'] = str(cur2[0][7])
            self.query['receiptOrderItem']['receiptOrder']['billTypeId'] = str(cur2[0][6])
            self.query['receiptOrderItem']['receiptOrder']['id'] = str(cur2[0][0])
            self.query['receiptOrderItem']['receiptOrder']['lastModificationTime'] = str(cur2[0][4])
            self.query['receiptOrderItem']['receiptOrder']['lastModifierId'] = str(cur2[0][1])
            self.query['receiptOrderItem']['receiptOrder']['creationTime'] = str(cur2[0][3])
            self.query['receiptOrderItem']['receiptOrder']['creatorId'] = str(cur2[0][2])
            self.query['receiptOrderItem']['material']['xCode'] = str(cur2[0][12])
            self.query['receiptOrderItem']['material']['xName'] = str(cur2[0][13])
            self.query['receiptOrderItem']['material']['isForbidden'] = str(cur2[0][10])
            self.query['receiptOrderItem']['material']['forbiddenUserId'] = str(cur2[0][11])
            self.query['receiptOrderItem']['material']['spec'] = str(cur2[0][14])
            self.query['receiptOrderItem']['material']['smallestUnit'] = str(cur2[0][15])
            self.query['receiptOrderItem']['material']['materialCategoryId'] = str(cur2[0][16])
            self.query['receiptOrderItem']['material']['materialPropertyRuleId'] = str(cur2[0][17])
            self.query['receiptOrderItem']['material']['allocatRelationId'] = str(cur2[0][18])
            self.query['receiptOrderItem']['material']['shipmentRuleId'] = str(cur2[0][19])
            self.query['receiptOrderItem']['material']['id'] = str(cur2[0][9])
            self.query['receiptOrderItem']['material']['lastModificationTime'] = str(cur2[0][23])
            self.query['receiptOrderItem']['material']['lastModifierId'] = str(cur2[0][21])
            self.query['receiptOrderItem']['material']['creationTime'] = str(cur2[0][22])
            self.query['receiptOrderItem']['material']['creatorId'] = str(cur2[0][20])
            self.query['receiptOrderItem']['material']['materialCategory']['xCode'] = str(cur2[0][34])
            self.query['receiptOrderItem']['material']['materialCategory']['xName'] = str(cur2[0][35])
            self.query['receiptOrderItem']['material']['materialCategory']['materialPropertyRuleId'] = str(cur2[0][36])
            self.query['receiptOrderItem']['material']['materialCategory']['isForbidden'] = str(cur2[0][37])
            self.query['receiptOrderItem']['material']['materialCategory']['id'] = str(cur2[0][16])
            self.query['receiptOrderItem']['material']['materialCategory']['lastModificationTime'] = str(cur2[0][38])
            self.query['receiptOrderItem']['material']['materialCategory']['creationTime'] = str(cur2[0][40])
            self.query['receiptOrderItem']['material']['materialCategory']['creatorId'] = str(cur2[0][39])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['xCode'] = str(cur2[0][47])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['xName'] = str(cur2[0][48])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['productionTime'] = str(cur2[0][49])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['receivedTime'] = str(cur2[0][50])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['inboundTime'] = str(cur2[0][51])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['expiredTime'] = str(cur2[0][52])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['aStartTime'] = str(cur2[0][53])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['qcStartTime'] = str(cur2[0][54])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['preservationDays'] = str(cur2[0][55])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['sourceOrderCode'] = str(cur2[0][56])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['batchNo'] = str(cur2[0][57])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['supplierId'] = str(cur2[0][58])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str1'] = str(cur2[0][59])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str2'] = str(cur2[0][60])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str3'] = str(cur2[0][61])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str4'] = str(cur2[0][62])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str5'] = str(cur2[0][63])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str6'] = str(cur2[0][64])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str7'] = str(cur2[0][65])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str8'] = str(cur2[0][66])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str9'] = str(cur2[0][67])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['m_Str10'] = str(cur2[0][68])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['id'] = str(cur2[0][36])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['lastModificationTime'] = str(
                cur2[0][44])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['lastModifierId'] = str(cur2[0][45])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['creationTime'] = str(cur2[0][41])
            self.query['receiptOrderItem']['material']['materialPropertyRule']['creatorId'] = str(cur2[0][42])
            self.query['receiptOrderItem']['material']['packageUnit'][0]['materialId'] = str(cur2[0][9])
            self.query['receiptOrderItem']['material']['packageUnit'][0]['unit'] = str(cur2[0][30])
            self.query['receiptOrderItem']['material']['packageUnit'][0]['pkgLevel'] = str(cur2[0][33])
            self.query['receiptOrderItem']['material']['packageUnit'][0]['convertFigureSmallUnit'] = str(cur2[0][31])
            self.query['receiptOrderItem']['material']['packageUnit'][0]['convertFigure'] = str(cur2[0][32])
            self.query['receiptOrderItem']['material']['packageUnit'][0]['id'] = str(cur2[0][24])
            self.query['receiptOrderItem']['material']['packageUnit'][0]['lastModificationTime'] = str(cur2[0][27])
            self.query['receiptOrderItem']['material']['packageUnit'][0]['lastModifierId'] = str(cur2[0][28])
            self.query['receiptOrderItem']['material']['packageUnit'][0]['creationTime'] = str(cur2[0][25])
            self.query['receiptOrderItem']['material']['packageUnit'][0]['creatorId'] = str(cur2[0][26])
            self.query['receiptOrderItem']['material']['packageUnit'][0]['creator'] = str(cur2[0][29])
            self.query['materialProperty']['propertyRuleId'] = str(cur2[0][17])
            self.query['materialProperty']['materialId'] = str(cur2[0][9])
            self.query['materialProperty']['productionTime'] = str(
                (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d'))  # 当前日期减30天作为生产日期
            self.query['materialProperty']['receivedTime'] = str(
                datetime.datetime.now().strftime('%Y-%m-%d'))  # 修改为当前日期
            self.query['materialProperty']['inboundTime'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))  # 修改为当前日期
            self.query['materialProperty']['expiredTime'] = str(
                (datetime.datetime.now() + datetime.timedelta(days=60)).strftime('%Y-%m-%d'))  # 当前日期加60天作为生产过期时间
            self.query['materialProperty']['qcStartTime'] = str(datetime.datetime.now().strftime('%Y-%m-%d'))  # 修改为当前日期
            self.query['materialProperty']['preservationDays'] = 90
            self.query['materialProperty']['sourceOrderCode'] = str(cur2[0][7])
            self.query['materialProperty']['batchNo'] = str(
                datetime.datetime.now().strftime('%Y%m%d'))  # str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            self.query['materialProperty']['supplierId'] = str(cur2[0][8])
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
            if self.case_name == 'creatreceiptOrderItem_receiptOrderId_null':
                self.query['receiptOrderItem']['receiptOrderId'] = ''
            elif self.case_name == 'creatreceiptOrderItem_materialId_null':
                self.query['receiptOrderItem']['materialId'] = ''
            elif self.case_name == 'creatreceiptOrderItem_packageUnitId_null':
                self.query['receiptOrderItem']['packageUnitId'] = ''
            elif self.case_name == 'creatreceiptOrderItem_expectedPkgQuantity_null':
                self.query['receiptOrderItem']['expectedPkgQuantity'] = ''
            elif self.case_name == 'creatreceiptOrderItem_receivedPkgQuantity_null':
                self.query['receiptOrderItem']['receivedPkgQuantity'] = ''
            elif self.case_name == 'creatreceiptOrderItem_movedPkgQuantity_null':
                self.query['receiptOrderItem']['movedPkgQuantity'] = ''
            elif self.case_name == 'creatreceiptOrderItem_receiptOrderId_notuuid':
                self.query['receiptOrderItem']['receiptOrderId'] = 'ef1b78a0'
            elif self.case_name == 'creatreceiptOrderItem_packageUnitId_notuuid':
                self.query['receiptOrderItem']['packageUnitId'] = 'ef1b78a0'
            elif self.case_name == 'creatreceiptOrderItem_expectedPkgQuantity_notnumber':
                self.query['receiptOrderItem']['expectedPkgQuantity'] = 'abc'
            elif self.case_name == 'creatreceiptOrderItem_receivedPkgQuantity_notnumber':
                self.query['receiptOrderItem']['receivedPkgQuantity'] = '收货数量非数值'
            elif self.case_name == 'creatreceiptOrderItem_movedPkgQuantity_notnumber':
                self.query['receiptOrderItem']['movedPkgQuantity'] = '-'
            elif self.case_name == 'creatreceiptOrderItem_productionTime_notdata':
                self.query['materialProperty']['productionTime'] = '201906'
            elif self.case_name == 'creatreceiptOrderItem_receivedTime_notdata':
                self.query['materialProperty']['receivedTime'] = 'abc'
            elif self.case_name == 'creatreceiptOrderItem_inboundTime_notdata':
                self.query['materialProperty']['inboundTime'] = '0.258'
            elif self.case_name == 'creatreceiptOrderItem_expiredTime_notdata':
                self.query['materialProperty']['expiredTime'] = '过期时间'
            elif self.case_name == 'creatreceiptOrderItem_qcStartTime_notdata':
                self.query['materialProperty']['qcStartTime'] = '2022'
            elif self.case_name == 'creatreceiptOrderItem_expectedPkgQuantity_allowlength':
                self.query['receiptOrderItem']['expectedPkgQuantity'] = '1000000000000000.99'
            elif self.case_name == 'creatreceiptOrderItem_expectedPkgQuantity_overlength':
                self.query['receiptOrderItem']['expectedPkgQuantity'] = '10000000000000000.89'
            elif self.case_name == 'creatreceiptOrderItem_expectedPkgQuantity_precisionoverlength':
                self.query['receiptOrderItem']['expectedPkgQuantity'] = '100000000000000.888'
            elif self.case_name == 'creatreceiptOrderItem_receivedPkgQuantity_overlength':
                self.query['receiptOrderItem']['receivedPkgQuantity'] = '1000000000000000000'
            elif self.case_name == 'creatreceiptOrderItem_movedPkgQuantity_overlength':
                self.query['receiptOrderItem']['movedPkgQuantity'] = '99999999999999999.01'
            elif self.case_name == 'creatreceiptOrderItem_batchNo_allowlength':
                self.query['materialProperty']['batchNo'] = '20220214150056A1-Ⅰ-01-测试批次号长度&@-20220214150056A201'
            elif self.case_name == 'creatreceiptOrderItem_batchNo_overlength':
                self.query['materialProperty']['batchNo'] = '20220214150056A1-Ⅰ-01-测试批次号长度&@-20220214150056A2001'
            elif self.case_name == 'creatreceiptOrderItem_m_Str1_overlength':
                self.query['materialProperty']['m_Str1'] = '测试扩展属性测试扩展属性测试扩展属性测试扩展属性1测试扩展属性测试扩展属性测试扩展属性测试扩展属性11'
            elif self.case_name == 'creatreceiptOrderItem_m_Str2_overlength':
                self.query['materialProperty']['m_Str2'] = '测试扩展属性测试扩展属性测试扩展属性测试扩展属性2测试扩展属性测试扩展属性测试扩展属性测试扩展属性22'
            elif self.case_name == 'creatreceiptOrderItem_receiptOrderId_error':
                self.query['materialProperty']['receiptOrderId'] = uuid.uuid1()
            elif self.case_name == 'creatreceiptOrderItem_materialId_error':
                self.query['materialProperty']['materialId'] = uuid.uuid1()
            elif self.case_name == 'creatreceiptOrderItem_expectedPkgQuantity_minus':
                self.query['receiptOrderItem']['expectedPkgQuantity'] = -99.89
            elif self.case_name == 'creatreceiptOrderItem_productionTime_ym':
                self.query['materialProperty']['productionTime'] = datetime.datetime.now().strftime('%Y-%m')
            elif self.case_name == 'creatreceiptOrderItem_batchNo_includespace':
                self.query['materialProperty']['batchNo'] = ' 202202141528A '
            elif self.case_name == 'creatreceiptOrderItem_batchNo_specialcharacter':
                self.query['materialProperty']['batchNo'] = "_202202141528A! @#$%&*(),./;'，。、？[]|+-.{0.5}①Ⅱ<>【】"
            elif self.case_name == 'creatreceiptOrderItem_m_Str1_specialcharacter':
                self.query['materialProperty']['m_Str1'] = 'NM!@_#%,;0.589 宧峟巇廱恅慯汮淗滷濪烞燖狚珱蚔蟁袾覬!ces誇譈責跊軛迵鄰鈰鋰鎯鑯祰穬'
            elif self.case_name == 'creatreceiptOrderItem_m_Str2_specialcharacter':
                self.query['materialProperty'][
                    'm_Str2'] = "歀鯾鴁鶽黇舊莃蒦薢塶0.9s(ms().ge('WS.Wm''粃絭縭陑靨"
            elif self.case_name == 'creatreceiptOrderItem_m_Str3_specialcharacter':
                self.query['materialProperty'][
                    'm_Str3'] = '顁餹騤鬴抃揨擷昖朤卾唗噐坧瓧羘胘妉媕桼楶橬@pt.(*cs)⑤⑽⒛㈢∑∏≈½‰㎏㎎¥αβàπΩㄚ零壹dʒあ'

            self.query = str(self.query).encode('utf-8')

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testcreatReceiptOrder(self):
        self.checkResult()

    def tearDown(self):
        print('测试结束....')
        ms().closeDB()  # 关闭数据库连接

    def checkResult(self):
        new_url = url + ':44349' + self.path
        # data1 = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(new_url).query))\
        if self.case_name == 'creatreceiptOrderItem':
            for n in range(len(self.querylist)):  # 根据querylist长度决定请求几次
                try:
                    info = RunMain().run_main(self.method, headers=self.headers, url=new_url, data=self.querylist[n])
                except Exception as e:
                    print('新建收货明细接口调用异常：', e)
                    raise Exception
                else:
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.query = eval(self.querylist[n])
                    try:
                        # 断言接口返回的信息中的'receiptOrderId'与接口调用中的‘receiptOrderId’参数值是否相等，若不相等，抛出断言错误
                        self.assertEqual(self.query['receiptOrderItem']['receiptOrderId'], info['receiptOrderId'])
                    except AssertionError as e:
                        print('接口未正常返回数据！', e)
                        raise AssertionError
                    else:
                        # 从数据库查询刚刚新建的收货单明细信息
                        ReceiptOrderItem = ms().get_all(
                            ms().ExecQuery("""
                            SELECT a.ReceiptOrderId, a.MaterialId MaterialId1, a.MaterialPropertyId, 
                            a.PackageUnitId, a.ExpectedPkgQuantity, a.ReceivedPkgQuantity, 
                            a.MovedPkgQuantity, a.Id ReceiptOrderItemid, b.MaterialId MaterialId2,
                            b.ProductionTime, b.ReceivedTime,b.InboundTime,b.ExpiredTime,b.SourceOrderCode,
                            b.BatchNo,b.M_Str1,b.M_Str2,b.M_Str3,b.M_Str4,b.M_Str5,
                            b.M_Str6,b.M_Str7,b.M_Str8,b.M_Str9,b.M_Str10
                            FROM WMS.ReceiptOrderItem a INNER JOIN WMS.MaterialProperty b 
                            ON a.MaterialPropertyId=b.Id WHERE a.Id='%s'
                            """ % info['id']))

                        # 断言接口传参的数据与接口返回的数据是否一致，接口传参的数据与新建的收货单明细的信息时是否一致，任意一个不相等，断言失败
                        self.assertFalse(any(x for x in (self.assertEqual(self.query['receiptOrderItem'][
                                                                              'receiptOrderId'], info['receiptOrderId'],
                                                                          '接口传参的收货主单据id与接口返回的单据id不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem'][
                                                                              'materialId'], info['materialId'],
                                                                          '接口传参的物料id与接口返回的物料id不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem'][
                                                                              'packageUnitId'], info['packageUnitId'],
                                                                          '接口传参的包装单位id与接口返回的包装单位id不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem'][
                                                                              'expectedPkgQuantity'], info[
                                                             'expectedPkgQuantity'], '接口传参的期望数量与接口返回的期望数量不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem'][
                                                                              'receivedPkgQuantity'], info[
                                                             'receivedPkgQuantity'], '接口传参的收货数量与接口返回的收货数量不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem'][
                                                                              'movedPkgQuantity'], info['movedPkgQuantity'],
                                                                          '接口传参的移动数量与接口返回的移动数量不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem'][
                                                                              'qCStatus'], info['qcStatus'],
                                                                          '接口传参的质检状态值与接口返回的质检状态值不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['receiptOrder'][
                                                                              'supplierId'], info['materialProperty'][
                                                             'supplierId'], '接口传参的供应商id与接口返回的供应商id不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['receiptOrder'][
                                                                              'xCode'], info['materialProperty'][
                                                             'sourceOrderCode'], '接口传参的收货单编号与接口返回的收货单编号不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['receiptOrder'][
                                                                              'shelvesStatus'], info[
                                                             'shelvesStatus'], '接口传参的上架状态与接口返回的上架状态不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['receiptOrder'][
                                                                              'id'], info['receiptOrderId'],
                                                                          '接口传参的收货单id与接口返回的收货单id不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['material'][
                                                                              'xCode'], info['material']['xCode'],
                                                                          '接口传参的物料编码与接口返回的物料编码不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['material'][
                                                                              'xName'], info['material']['xName'],
                                                                          '接口传参的物料名称与接口返回的物料名称不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['material'][
                                                                              'xName'], info['material']['xName'],
                                                                          '接口传参的物料名称与接口返回的物料名称不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['material'][
                                                                              'isForbidden'], info['material']['isForbidden'],
                                                                          '接口传参的物料是否禁用状态与接口返回的物料是否禁用状态不一致！'),
                                                         self.assertEqual(ms().transformNone(self.query[
                                                                                                 'receiptOrderItem'][
                                                                                                 'material']['spec']),
                                                                          ms().transformNone(info['material']['spec']),
                                                                          '接口传参的物料规格与接口返回的物料规格不一致！'),
                                                         self.assertEqual(ms().transformNone(self.query[
                                                                                                 'receiptOrderItem'][
                                                                                                 'material']['smallestUnit']),
                                                                          ms().transformNone(info['material']['smallestUnit']),
                                                                          '接口传参的包装单位与接口返回的包装单位不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['material'][
                                                                              'materialCategoryId'],
                                                                          info['material']['materialCategoryId'],
                                                                          '接口传参的物料类目id与接口返回的物料类目id不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['material'][
                                                                              'materialPropertyRuleId'],
                                                                          info['material']['materialPropertyRuleId'],
                                                                          '接口传参的属性规则id与接口返回的属性规则id不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['material'][
                                                                              'id'],
                                                                          info['material']['id'],
                                                                          '接口传参的物料id与接口返回的物料id不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['propertyRuleId'],
                                                                          info['materialProperty']['propertyRuleId'],
                                                                          '接口传参的属性规则id与接口返回的属性规则id不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['materialId'],
                                                                          info['materialProperty']['materialId'],
                                                                          '接口传参的物料id与接口返回的物料id不一致！'),
                                                         self.assertEqual(
                                                                          datetime.datetime.strptime(
                                                                              self.query['materialProperty'][
                                                                                  'productionTime'], '%Y-%m-%d'),
                                                                          datetime.datetime.strptime(
                                                                              info['materialProperty']['productionTime'],
                                                                              '%Y-%m-%dT%H:%M:%S'),
                                                                          '接口传参的物料生产日期与接口返回的物料生产日期不一致！'),
                                                         self.assertEqual(datetime.datetime.strptime(
                                                                              self.query['materialProperty'][
                                                                                  'receivedTime'], '%Y-%m-%d'),
                                                                          datetime.datetime.strptime(
                                                                              info['materialProperty']['receivedTime'],
                                                                              '%Y-%m-%dT%H:%M:%S'),
                                                                          '接口传参的物料收货日期与接口返回的物料收货日期不一致！'),
                                                         self.assertEqual(datetime.datetime.strptime(
                                                                              self.query['materialProperty'][
                                                                                  'inboundTime'], '%Y-%m-%d'),
                                                                          datetime.datetime.strptime(
                                                                              info['materialProperty']['inboundTime'],
                                                                              '%Y-%m-%dT%H:%M:%S'),
                                                                          '接口传参的物料入库时间与接口返回的物料入库时间不一致！'),
                                                         self.assertEqual(datetime.datetime.strptime(
                                                                              self.query['materialProperty'][
                                                                                  'expiredTime'], '%Y-%m-%d'),
                                                                          datetime.datetime.strptime(
                                                                              info['materialProperty']['expiredTime'],
                                                                              '%Y-%m-%dT%H:%M:%S'),
                                                                          '接口传参的物料过期时间与接口返回的物料过期时间不一致！'),
                                                         self.assertEqual(datetime.datetime.strptime(
                                                                              self.query['materialProperty'][
                                                                                  'qcStartTime'], '%Y-%m-%d'),
                                                                          datetime.datetime.strptime(
                                                                              info['materialProperty']['qcStartTime'],
                                                                              '%Y-%m-%dT%H:%M:%S'),
                                                                          '接口传参的物料质检时间与接口返回的物料质检时间不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['batchNo'],
                                                                          info['materialProperty']['batchNo'],
                                                                          '接口传参的批次号与接口返回的批次号不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str1'],
                                                                          info['materialProperty']['m_Str1'],
                                                                          '接口传参的扩展属性1与接口返回的扩展属性1不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str2'],
                                                                          info['materialProperty']['m_Str2'],
                                                                          '接口传参的扩展属性2与接口返回的扩展属性2不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str3'],
                                                                          info['materialProperty']['m_Str3'],
                                                                          '接口传参的扩展属性3与接口返回的扩展属性3不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str4'],
                                                                          info['materialProperty']['m_Str4'],
                                                                          '接口传参的扩展属性4与接口返回的扩展属性4不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str5'],
                                                                          info['materialProperty']['m_Str5'],
                                                                          '接口传参的扩展属性5与接口返回的扩展属性5不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str6'],
                                                                          info['materialProperty']['m_Str6'],
                                                                          '接口传参的扩展属性6与接口返回的扩展属性6不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str7'],
                                                                          info['materialProperty']['m_Str7'],
                                                                          '接口传参的扩展属性7与接口返回的扩展属性7不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str8'],
                                                                          info['materialProperty']['m_Str8'],
                                                                          '接口传参的扩展属性8与接口返回的扩展属性8不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str9'],
                                                                          info['materialProperty']['m_Str9'],
                                                                          '接口传参的扩展属性9与接口返回的扩展属性9不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str10'],
                                                                          info['materialProperty']['m_Str10'],
                                                                          '接口传参的扩展属性10与接口返回的扩展属性10不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['receiptOrderId'],
                                                                          str(ReceiptOrderItem[0][0]),
                                                                          '接口传参的收货主单据id与新建的收货明细中的主单据id不一致！'),
                                                         self.assertEqual(
                                                             self.query['receiptOrderItem']['materialId'],
                                                             str(ReceiptOrderItem[0][1]),
                                                             '接口传参的物料id与新建的收货明细中的物料id不一致！'),
                                                         self.assertEqual(
                                                             info['materialPropertyId'],
                                                             str(ReceiptOrderItem[0][2]),
                                                             '接口传参的扩展属性id与新建的收货明细中的扩展属性id不一致！'),
                                                         self.assertEqual(
                                                             self.query['receiptOrderItem']['packageUnitId'],
                                                             str(ReceiptOrderItem[0][3]),
                                                             '接口传参的扩展属性id与新建的收货明细中的扩展属性id不一致！'),
                                                         self.assertEqual(
                                                             self.query['receiptOrderItem']['expectedPkgQuantity'],
                                                             ReceiptOrderItem[0][4],
                                                             '接口传参的期望数量与新建的收货明细中的期望数量不一致！'),
                                                         self.assertEqual(
                                                             self.query['receiptOrderItem']['receivedPkgQuantity'],
                                                             ReceiptOrderItem[0][5],
                                                             '接口传参的收货数量与新建的收货明细中的收货数量不一致！'),
                                                         self.assertEqual(
                                                             self.query['receiptOrderItem']['movedPkgQuantity'],
                                                             ReceiptOrderItem[0][6],
                                                             '接口传参的移动数量与新建的收货明细中的移动数量不一致！'),
                                                         self.assertEqual(
                                                             info['id'],
                                                             str(ReceiptOrderItem[0][7]),
                                                             '接口传参的收货明细id与新建的收货明细的id不一致！'),
                                                         self.assertEqual(
                                                             self.query['receiptOrderItem']['materialId'],
                                                             str(ReceiptOrderItem[0][8]),
                                                             '接口传参的物料id与新建的收货明细对应的扩展属性中的物料id不一致！'),
                                                         self.assertEqual(
                                                             datetime.datetime.strptime(
                                                                 self.query['materialProperty'][
                                                                     'productionTime'], '%Y-%m-%d'),
                                                             ReceiptOrderItem[0][9],
                                                             '接口传参的物料生产日期与新建的收货明细对应的扩展属性中的生产日期不一致！'),
                                                         self.assertEqual(
                                                             datetime.datetime.strptime(self.query['materialProperty'][
                                                                                            'receivedTime'], '%Y-%m-%d'),
                                                             ReceiptOrderItem[0][10],
                                                             '接口传参的物料收货日期与新建的收货明细对应的扩展属性中的收货日期不一致！'),
                                                         self.assertEqual(
                                                         datetime.datetime.strptime(self.query['materialProperty'][
                                                                                        'inboundTime'], '%Y-%m-%d'),
                                                             ReceiptOrderItem[0][11],
                                                             '接口传参的物料入库日期与新建的收货明细对应的扩展属性中的入库日期不一致！'),
                                                         self.assertEqual(
                                                             datetime.datetime.strptime(self.query['materialProperty'][
                                                                                            'expiredTime'], '%Y-%m-%d'),
                                                             ReceiptOrderItem[0][12],
                                                             '接口传参的物料过期时间与新建的收货明细对应的扩展属性中的过期时间不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['batchNo'],
                                                             str(ReceiptOrderItem[0][14]),
                                                             '接口传参的批次号与新建的收货明细对应的扩展属性中的批次号不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str1'],
                                                             str(ReceiptOrderItem[0][15]),
                                                             '接口传参的扩展属性1的值与新建的收货明细对应的扩展属性中的扩展属性1的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str2'],
                                                             str(ReceiptOrderItem[0][16]),
                                                             '接口传参的扩展属性2的值与新建的收货明细对应的扩展属性中的扩展属性2的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str3'],
                                                             str(ReceiptOrderItem[0][17]),
                                                             '接口传参的扩展属性3的值与新建的收货明细对应的扩展属性中的扩展属性3的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str4'],
                                                             str(ReceiptOrderItem[0][18]),
                                                             '接口传参的扩展属性4的值与新建的收货明细对应的扩展属性中的扩展属性4的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str5'],
                                                             str(ReceiptOrderItem[0][19]),
                                                             '接口传参的扩展属性5的值与新建的收货明细对应的扩展属性中的扩展属性5的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str6'],
                                                             str(ReceiptOrderItem[0][20]),
                                                             '接口传参的扩展属性6的值与新建的收货明细对应的扩展属性中的扩展属性6的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str7'],
                                                             str(ReceiptOrderItem[0][20]),
                                                             '接口传参的扩展属性7的值与新建的收货明细对应的扩展属性中的扩展属性7的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str8'],
                                                             str(ReceiptOrderItem[0][20]),
                                                             '接口传参的扩展属性8的值与新建的收货明细对应的扩展属性中的扩展属性8的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str9'],
                                                             str(ReceiptOrderItem[0][20]),
                                                             '接口传参的扩展属性9的值与新建的收货明细对应的扩展属性中的扩展属性9的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str10'],
                                                             str(ReceiptOrderItem[0][20]),
                                                             '接口传参的扩展属性10的值与新建的收货明细对应的扩展属性中的扩展属性10的值不一致！')
                                                         )))
        else:
            try:
                info = RunMain().run_main(self.method, headers=self.headers, url=new_url, data=self.query)
            except Exception as e:
                print('接口调用异常：', e)
                raise Exception
            else:
                if self.case_name == 'creatreceiptOrderItem_parametersNotnull':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.query = eval(self.query)
                    try:
                        # 断言接口返回的信息中的'receiptOrderId'与接口调用中的‘receiptOrderId’参数值是否相等，若不相等，抛出断言错误
                        self.assertEqual(self.query['receiptOrderItem']['receiptOrderId'], info['receiptOrderId'])
                    except AssertionError as e:
                        print('接口未正常返回数据！', e)
                        raise AssertionError
                    else:
                        # 从数据库查询刚刚新建的收货单明细信息
                        ReceiptOrderItem = ms().get_all(
                            ms().ExecQuery("""
                            SELECT a.ReceiptOrderId, a.MaterialId MaterialId1, a.MaterialPropertyId, 
                            a.PackageUnitId, a.ExpectedPkgQuantity, a.ReceivedPkgQuantity, 
                            a.MovedPkgQuantity, a.Id ReceiptOrderItemid, b.MaterialId MaterialId2,
                            b.ProductionTime, b.ReceivedTime,b.InboundTime,b.ExpiredTime,b.SourceOrderCode,
                            b.BatchNo,b.M_Str1,b.M_Str2,b.M_Str3,b.M_Str4,b.M_Str5,
                            b.M_Str6,b.M_Str7,b.M_Str8,b.M_Str9,b.M_Str10
                            FROM WMS.ReceiptOrderItem a INNER JOIN WMS.MaterialProperty b 
                            ON a.MaterialPropertyId=b.Id WHERE a.Id='%s'
                            """ % info['id']))

                        # 根据物料id从数据库查询对应的物料编码、名称信息，用于后续断言校验
                        Material = ms().get_all(
                            ms().ExecQuery("""SELECT XCode, XName, ShortName, Spec, SmallestUnit, 
                            MaterialCategoryId, MaterialPropertyRuleId 
                            FROM  WMS.Material WHERE Id='%s'""" % info['materialId']))

                        # 断言接口传参的数据与接口返回的数据是否一致，接口传参的数据与新建的收货单明细的信息时是否一致，任意一个不相等，断言失败
                        self.assertFalse(any(x for x in (self.assertEqual(self.query['receiptOrderItem'][
                                                                              'receiptOrderId'], info['receiptOrderId'],
                                                                          '接口传参的收货主单据id与接口返回的单据id不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem'][
                                                                              'materialId'], info['materialId'],
                                                                          '接口传参的物料id与接口返回的物料id不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem'][
                                                                              'packageUnitId'], info['packageUnitId'],
                                                                          '接口传参的包装单位id与接口返回的包装单位id不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem'][
                                                                              'expectedPkgQuantity'], info[
                                                             'expectedPkgQuantity'], '接口传参的期望数量与接口返回的期望数量不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem'][
                                                                              'receivedPkgQuantity'], info[
                                                             'receivedPkgQuantity'], '接口传参的收货数量与接口返回的收货数量不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem'][
                                                                              'movedPkgQuantity'], info['movedPkgQuantity'],
                                                                          '接口传参的移动数量与接口返回的移动数量不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['receiptOrder'][
                                                                              'xCode'], info['materialProperty'][
                                                             'sourceOrderCode'], '接口传参的收货单编号与接口返回的收货单编号不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['receiptOrder'][
                                                                              'id'], info['receiptOrderId'],
                                                                          '接口传参的收货单id与接口返回的收货单id不一致！'),
                                                         self.assertEqual(Material[0][0], info['material']['xCode'],
                                                                          '接口传参的物料编码与接口返回的物料编码不一致！'),
                                                         self.assertEqual(Material[0][1], info['material']['xName'],
                                                                          '接口传参的物料名称与接口返回的物料名称不一致！'),
                                                         self.assertEqual(ms().transformNone(Material[0][3]),
                                                                          ms().transformNone(info['material']['spec']),
                                                                          '接口传参的物料规格与接口返回的物料规格不一致！'),
                                                         self.assertEqual(ms().transformNone(Material[0][4]),
                                                                          ms().transformNone(info['material']['smallestUnit']),
                                                                          '接口传参的包装单位与接口返回的包装单位不一致！'),
                                                         self.assertEqual(str(Material[0][5]),
                                                                          info['material']['materialCategoryId'],
                                                                          '接口传参的物料类目id与接口返回的物料类目id不一致！'),
                                                         self.assertEqual(str(Material[0][6]),
                                                                          info['material']['materialPropertyRuleId'],
                                                                          '接口传参的属性规则id与接口返回的属性规则id不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['material'][
                                                                              'id'],
                                                                          info['material']['id'],
                                                                          '接口传参的物料id与接口返回的物料id不一致！'),
                                                         self.assertEqual(str(Material[0][6]),
                                                                          info['materialProperty']['propertyRuleId'],
                                                                          '接口传参的属性规则id与接口返回的属性规则id不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['materialId'],
                                                                          info['materialProperty']['materialId'],
                                                                          '接口传参的物料id与接口返回的物料id不一致！'),
                                                         self.assertEqual(None, info['materialProperty']['productionTime'],
                                                                          '接口传参的物料生产日期与接口返回的物料生产日期不一致！'),
                                                         self.assertEqual(None, info['materialProperty']['receivedTime'],
                                                                          '接口传参的物料收货日期与接口返回的物料收货日期不一致！'),
                                                         self.assertEqual(None, info['materialProperty']['inboundTime'],
                                                                          '接口传参的物料入库时间与接口返回的物料入库时间不一致！'),
                                                         self.assertEqual(None, info['materialProperty']['expiredTime'],
                                                                          '接口传参的物料过期时间与接口返回的物料过期时间不一致！'),
                                                         self.assertEqual(None, info['materialProperty']['qcStartTime'],
                                                                          '接口传参的物料质检时间与接口返回的物料质检时间不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['batchNo'],
                                                                          info['materialProperty']['batchNo'],
                                                                          '接口传参的批次号与接口返回的批次号不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str1'],
                                                                          info['materialProperty']['m_Str1'],
                                                                          '接口传参的扩展属性1与接口返回的扩展属性1不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str2'],
                                                                          info['materialProperty']['m_Str2'],
                                                                          '接口传参的扩展属性2与接口返回的扩展属性2不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str3'],
                                                                          info['materialProperty']['m_Str3'],
                                                                          '接口传参的扩展属性3与接口返回的扩展属性3不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str4'],
                                                                          info['materialProperty']['m_Str4'],
                                                                          '接口传参的扩展属性4与接口返回的扩展属性4不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str5'],
                                                                          info['materialProperty']['m_Str5'],
                                                                          '接口传参的扩展属性5与接口返回的扩展属性5不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str6'],
                                                                          info['materialProperty']['m_Str6'],
                                                                          '接口传参的扩展属性6与接口返回的扩展属性6不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str7'],
                                                                          info['materialProperty']['m_Str7'],
                                                                          '接口传参的扩展属性7与接口返回的扩展属性7不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str8'],
                                                                          info['materialProperty']['m_Str8'],
                                                                          '接口传参的扩展属性8与接口返回的扩展属性8不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str9'],
                                                                          info['materialProperty']['m_Str9'],
                                                                          '接口传参的扩展属性9与接口返回的扩展属性9不一致！'),
                                                         self.assertEqual(self.query['materialProperty']['m_Str10'],
                                                                          info['materialProperty']['m_Str10'],
                                                                          '接口传参的扩展属性10与接口返回的扩展属性10不一致！'),
                                                         self.assertEqual(self.query['receiptOrderItem']['receiptOrderId'],
                                                                          str(ReceiptOrderItem[0][0]),
                                                                          '接口传参的收货主单据id与新建的收货明细中的主单据id不一致！'),
                                                         self.assertEqual(
                                                             self.query['receiptOrderItem']['materialId'],
                                                             str(ReceiptOrderItem[0][1]),
                                                             '接口传参的物料id与新建的收货明细中的物料id不一致！'),
                                                         self.assertEqual(
                                                             info['materialPropertyId'],
                                                             str(ReceiptOrderItem[0][2]),
                                                             '接口传参的扩展属性id与新建的收货明细中的扩展属性id不一致！'),
                                                         self.assertEqual(
                                                             self.query['receiptOrderItem']['packageUnitId'],
                                                             str(ReceiptOrderItem[0][3]),
                                                             '接口传参的扩展属性id与新建的收货明细中的扩展属性id不一致！'),
                                                         self.assertEqual(
                                                             self.query['receiptOrderItem']['expectedPkgQuantity'],
                                                             ReceiptOrderItem[0][4],
                                                             '接口传参的期望数量与新建的收货明细中的期望数量不一致！'),
                                                         self.assertEqual(
                                                             self.query['receiptOrderItem']['receivedPkgQuantity'],
                                                             ReceiptOrderItem[0][5],
                                                             '接口传参的收货数量与新建的收货明细中的收货数量不一致！'),
                                                         self.assertEqual(
                                                             self.query['receiptOrderItem']['movedPkgQuantity'],
                                                             ReceiptOrderItem[0][6],
                                                             '接口传参的移动数量与新建的收货明细中的移动数量不一致！'),
                                                         self.assertEqual(
                                                             info['id'],
                                                             str(ReceiptOrderItem[0][7]),
                                                             '接口传参的收货明细id与新建的收货明细的id不一致！'),
                                                         self.assertEqual(
                                                             self.query['receiptOrderItem']['materialId'],
                                                             str(ReceiptOrderItem[0][8]),
                                                             '接口传参的物料id与新建的收货明细对应的扩展属性中的物料id不一致！'),
                                                         self.assertEqual(None, ReceiptOrderItem[0][9],
                                                                          '接口传参的物料生产日期与新建的收货明细对应的扩展属性中的生产日期不一致！'),
                                                         self.assertEqual(None, ReceiptOrderItem[0][10],
                                                                          '接口传参的物料收货日期与新建的收货明细对应的扩展属性中的收货日期不一致！'),
                                                         self.assertEqual(None, ReceiptOrderItem[0][11],
                                                                          '接口传参的物料入库日期与新建的收货明细对应的扩展属性中的入库日期不一致！'),
                                                         self.assertEqual(None, ReceiptOrderItem[0][12],
                                                                          '接口传参的物料过期时间与新建的收货明细对应的扩展属性中的过期时间不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['batchNo'],
                                                             str(ReceiptOrderItem[0][14]),
                                                             '接口传参的批次号与新建的收货明细对应的扩展属性中的批次号不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str1'],
                                                             str(ReceiptOrderItem[0][15]),
                                                             '接口传参的扩展属性1的值与新建的收货明细对应的扩展属性中的扩展属性1的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str2'],
                                                             str(ReceiptOrderItem[0][16]),
                                                             '接口传参的扩展属性2的值与新建的收货明细对应的扩展属性中的扩展属性2的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str3'],
                                                             str(ReceiptOrderItem[0][17]),
                                                             '接口传参的扩展属性3的值与新建的收货明细对应的扩展属性中的扩展属性3的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str4'],
                                                             str(ReceiptOrderItem[0][18]),
                                                             '接口传参的扩展属性4的值与新建的收货明细对应的扩展属性中的扩展属性4的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str5'],
                                                             str(ReceiptOrderItem[0][19]),
                                                             '接口传参的扩展属性5的值与新建的收货明细对应的扩展属性中的扩展属性5的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str6'],
                                                             str(ReceiptOrderItem[0][20]),
                                                             '接口传参的扩展属性6的值与新建的收货明细对应的扩展属性中的扩展属性6的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str7'],
                                                             str(ReceiptOrderItem[0][20]),
                                                             '接口传参的扩展属性7的值与新建的收货明细对应的扩展属性中的扩展属性7的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str8'],
                                                             str(ReceiptOrderItem[0][20]),
                                                             '接口传参的扩展属性8的值与新建的收货明细对应的扩展属性中的扩展属性8的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str9'],
                                                             str(ReceiptOrderItem[0][20]),
                                                             '接口传参的扩展属性9的值与新建的收货明细对应的扩展属性中的扩展属性9的值不一致！'),
                                                         self.assertEqual(
                                                             self.query['materialProperty']['m_Str10'],
                                                             str(ReceiptOrderItem[0][20]),
                                                             '接口传参的扩展属性10的值与新建的收货明细对应的扩展属性中的扩展属性10的值不一致！')
                                                         )))

                elif self.case_name == 'creatreceiptOrderItem_receiptOrderId_null':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('收货单id必填！', info['error']['message'], '缺少必填参数receiptOrderId时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_materialId_null':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('物料id必填！', info['error']['message'], '缺少必填参数materialId时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_packageUnitId_null':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('物料包装单位id必填！', info['error']['message'], '缺少必填参数packageUnitId时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_expectedPkgQuantity_null':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('期望数量必填！', info['error']['message'], '必填参数expectedPkgQuantity值为空时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_receivedPkgQuantity_null':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('收货数量必填！', info['error']['message'], '必填参数receivedPkgQuantity值为空时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_movedPkgQuantity_null':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('移动数量必填！', info['error']['message'], '必填参数movedPkgQuantity值为空时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_receiptOrderId_notuuid':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('收货单id格式错误！', info['error']['message'], 'receiptOrderId参数类型错误时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_packageUnitId_notuuid':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('包装单位id格式错误！', info['error']['message'], 'packageUnitId参数类型错误时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_expectedPkgQuantity_notnumber':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('期望数量不是数值类型！', info['error']['message'], 'expectedPkgQuantity参数不是数值类型时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_receivedPkgQuantity_notnumber':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('收货数量不是数值类型！', info['error']['message'], 'receivedPkgQuantity参数不是数值类型时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_movedPkgQuantity_notnumber':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('移动数量不是数值类型！', info['error']['message'], 'movedPkgQuantity参数不是数值类型时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_productionTime_notdata':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('生产时间不是日期类型！', info['error']['message'], 'productionTime参数不是日期类型时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_receivedTime_notdata':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('收货日期不是日期类型！', info['error']['message'], 'receivedTime参数不是日期类型时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_inboundTime_notdata':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('入库日期不是日期类型！', info['error']['message'], 'inboundTime参数不是日期类型时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_expiredTime_notdata':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('过期时间不是日期类型！', info['error']['message'], 'expiredTime参数不是日期类型时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_qcStartTime_notdata':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('质检时间不是日期类型！', info['error']['message'], 'qcStartTime参数不是日期类型时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_expectedPkgQuantity_allowlength':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    print('接口请求体：', self.query)
                    self.query = eval(self.query)
                    self.assertEqual(self.query['receiptOrderItem']['expectedPkgQuantity'], info[
                        'expectedPkgQuantity'], '接口返回的expectedPkgQuantity值与调用时的值不相等！')
                elif self.case_name == 'creatreceiptOrderItem_expectedPkgQuantity_overlength':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    print('接口请求体：', self.query)
                    self.assertEqual('期望数量数值长度过长！', info['error'][
                        'message'], 'expectedPkgQuantity参数长度超数据库字段长度时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_expectedPkgQuantity_precisionoverlength':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    print('接口请求体：', self.query)
                    self.query = eval(self.query)
                    self.assertEqual(float(
                        Decimal(self.query['receiptOrderItem']['expectedPkgQuantity']).quantize(
                            Decimal('0.00'))), info['expectedPkgQuantity'],
                        '接口返回的expectedPkgQuantity值与调用时的值不相等！')
                elif self.case_name == 'creatreceiptOrderItem_receivedPkgQuantity_overlength':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('收货数量数值长度过长！', info['error'][
                        'message'], 'receivedPkgQuantity参数长度超数据库字段长度时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_movedPkgQuantity_overlength':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('移动数量数值长度过长！', info['error'][
                        'message'], 'movedPkgQuantity参数长度超数据库字段长度时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_batchNo_allowlength':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    print('接口请求体：', self.query)
                    self.query = eval(self.query)
                    self.assertEqual(self.query['materialProperty']['batchNo'], info[
                        'materialProperty']['batchNo'], '接口返回的batchNo值与调用时传的值不相等！')
                elif self.case_name == 'creatreceiptOrderItem_batchNo_overlength':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('批次号长度过长！', info['error'][
                        'message'], 'batchNo参数长度超数据库字段长度时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_m_Str1_overlength':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    print('接口请求体：', self.query)
                    self.assertEqual('扩展属性1长度过长！', info['error'][
                        'message'], 'm_Str1参数长度超数据库字段长度时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_m_Str2_overlength':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('扩展属性2长度过长！', info['error'][
                        'message'], 'm_Str2参数长度超数据库字段长度时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_receiptOrderId_error':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('收货id信息错误！', info['error'][
                        'message'], 'receiptOrderId参数传值错误（传的receiptOrderId没有对应的收货单信息）时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_materialId_error':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('物料id信息错误！', info['error'][
                        'message'], 'receiptOrderId参数传值错误（传的materialId没有对应的物料信息）时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_expectedPkgQuantity_minus':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.assertEqual('期望数量数值应大于0！', info['error'][
                        'message'], 'expectedPkgQuantity参数数值小于0时，接口没有正确的对应处理机制！')
                elif self.case_name == 'creatreceiptOrderItem_productionTime_ym':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.query = eval(self.query)
                    self.assertEqual(datetime.datetime.strptime(self.query['materialProperty'][
                                                                    'productionTime'], '%Y-%m').date(),
                                     datetime.datetime.strptime(str(info['materialProperty'][
                                                                    'productionTime'])[:7], '%Y-%m').date(),
                                     '接口返回的productionTime值与调用时传的值不相等！')
                elif self.case_name == 'creatreceiptOrderItem_batchNo_includespace':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.query = eval(self.query)
                    self.assertEqual(self.query['materialProperty']['batchNo'].strip(),
                                     info['materialProperty']['batchNo'], '接口返回的batchNo值没有去除前后空格！')
                elif self.case_name == 'creatreceiptOrderItem_batchNo_specialcharacter':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.query = eval(self.query)
                    self.assertEqual(self.query['materialProperty']['batchNo'],
                                     info['materialProperty']['batchNo'], '接口传参的batchNo与接口返回的batchNo不一致！')
                elif self.case_name == 'creatreceiptOrderItem_m_Str1_specialcharacter':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.query = eval(self.query)
                    self.assertEqual(self.query['materialProperty']['m_Str1'],
                                     info['materialProperty']['m_Str1'], '接口传参的m_Str1与接口返回的m_Str1不一致！')
                elif self.case_name == 'creatreceiptOrderItem_m_Str2_specialcharacter':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.query = eval(self.query)
                    self.assertEqual(self.query['materialProperty']['m_Str2'],
                                     info['materialProperty']['m_Str2'], '接口传参的m_Str2与接口返回的m_Str2不一致！')
                elif self.case_name == 'creatreceiptOrderItem_m_Str3_specialcharacter':
                    print('测试用例中文名：', self.case_name_ch)
                    print('接口返回：', info)
                    self.query = eval(self.query)
                    self.assertEqual(self.query['materialProperty']['m_Str3'],
                                     info['materialProperty']['m_Str3'], '接口传参的m_Str3与接口返回的m_Str3不一致！')


if __name__ == '__main__':
    unittest.main()




