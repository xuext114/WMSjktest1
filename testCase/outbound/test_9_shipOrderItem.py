#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对当前最新的状态为打开的未新建发货明细的收货单新建发货明细，
从库存中随机取5个非托盘的、未被分配的在架物料新建，
发货数量从[5,10,15,20,25,30]中随机取"""

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

url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'shipOrderItem')


@paramunittest.parametrized(*casexls)
class testShipOrderItem(unittest.TestCase):
    def setParameters(self, case_name, method, path, query):
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = eval(query)
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()
        self.querylist = []
        cur = ms().getvalue('WMS.ShipOrder', 'ShipOrderItem')
        def isNone(value):
            """
            判断某个值是否为None，如果为None，返回空字符，如果不为None，返回本身
            :param value:
            :return:
            """
            if value is None:
                return ''
            else:
                return value

        self.shipOrderIdlist = []
        for i in range(len(cur)):  # 根据查询结果条数循环将修改后的请求体添加到querylist中
            self.query['shipOrderItem']['shipOrderId'] = str(cur[i][0])
            self.query['shipOrderItem']['materialId'] = str(cur[i][12])
            self.query['shipOrderItem']['packageUnitId'] = str(cur[i][23])
            self.query['shipOrderItem']['expectedPkgQuantity'] = random.choice([5, 10, 15, 20, 25, 30])
            self.query['shipOrderItem']['shipOrder']['ownerId'] = str(cur[i][10])
            self.query['shipOrderItem']['shipOrder']['customerId'] = str(cur[i][9])
            self.query['shipOrderItem']['shipOrder']['whId'] = str(cur[i][8])
            self.query['shipOrderItem']['shipOrder']['billTypeId'] = str(cur[i][7])
            self.query['shipOrderItem']['shipOrder']['xCode'] = str(cur[i][5])
            self.query['shipOrderItem']['shipOrder']['dockId'] = str(cur[i][11])
            self.query['shipOrderItem']['shipOrder']['receivedBy'] = str(cur[i][6])
            self.query['shipOrderItem']['shipOrder']['id'] = str(cur[i][0])
            self.query['shipOrderItem']['shipOrder']['lastModificationTime'] = str(cur[i][3])
            self.query['shipOrderItem']['shipOrder']['lastModifierId'] = str(cur[i][4])
            self.query['shipOrderItem']['shipOrder']['creationTime'] = str(cur[i][1])
            self.query['shipOrderItem']['shipOrder']['creatorId'] = str(cur[i][2])
            # self.query['shipOrderItem']['shipOrder']['isOffLine'] = False
            self.query['shipOrderItem']['material']['xCode'] = str(cur[i][17])
            self.query['shipOrderItem']['material']['xName'] = str(cur[i][18])
            self.query['shipOrderItem']['material']['spec'] = str(cur[i][19])
            self.query['shipOrderItem']['material']['smallestUnit'] = str(cur[i][20])
            self.query['shipOrderItem']['material']['materialCategoryId'] = str(cur[i][31])
            self.query['shipOrderItem']['material']['materialPropertyRuleId'] = str(cur[i][37])
            self.query['shipOrderItem']['material']['allocatRelationId'] = str(cur[i][22])
            self.query['shipOrderItem']['material']['shipmentRuleId'] = str(cur[i][21])
            self.query['shipOrderItem']['material']['id'] = str(cur[i][12])
            self.query['shipOrderItem']['material']['lastModificationTime'] = str(cur[i][15])
            self.query['shipOrderItem']['material']['lastModifierId'] = str(cur[i][16])
            self.query['shipOrderItem']['material']['creationTime'] = str(cur[i][13])
            self.query['shipOrderItem']['material']['creatorId'] = str(cur[i][14])
            self.query['shipOrderItem']['material']['materialCategory']['xCode'] = str(cur[i][32])
            self.query['shipOrderItem']['material']['materialCategory']['xName'] = str(cur[i][33])
            self.query['shipOrderItem']['material']['materialCategory']['materialPropertyRuleId'] = str(cur[i][37])
            self.query['shipOrderItem']['material']['materialCategory']['id'] = str(cur[i][31])
            self.query['shipOrderItem']['material']['materialCategory']['lastModificationTime'] = str(cur[i][34])
            self.query['shipOrderItem']['material']['materialCategory']['creationTime'] = str(cur[i][36])
            self.query['shipOrderItem']['material']['materialCategory']['creatorId'] = str(cur[i][35])
            self.query['shipOrderItem']['material']['materialPropertyRule']['xCode'] = str(cur[i][42])
            self.query['shipOrderItem']['material']['materialPropertyRule']['xName'] = str(cur[i][43])
            self.query['shipOrderItem']['material']['materialPropertyRule']['productionTime'] = str(cur[i][44])
            self.query['shipOrderItem']['material']['materialPropertyRule']['receivedTime'] = str(cur[i][45])
            self.query['shipOrderItem']['material']['materialPropertyRule']['inboundTime'] = str(cur[i][46])
            self.query['shipOrderItem']['material']['materialPropertyRule']['expiredTime'] = str(cur[i][48])
            self.query['shipOrderItem']['material']['materialPropertyRule']['aStartTime'] = str(cur[i][49])
            self.query['shipOrderItem']['material']['materialPropertyRule']['qcStartTime'] = str(cur[i][50])
            self.query['shipOrderItem']['material']['materialPropertyRule']['preservationDays'] = str(cur[i][51])
            self.query['shipOrderItem']['material']['materialPropertyRule']['sourceOrderCode'] = str(cur[i][52])
            self.query['shipOrderItem']['material']['materialPropertyRule']['batchNo'] = str(cur[i][53])
            self.query['shipOrderItem']['material']['materialPropertyRule']['supplierId'] = str(cur[i][47])
            self.query['shipOrderItem']['material']['materialPropertyRule']['m_Str1'] = str(cur[i][54])
            self.query['shipOrderItem']['material']['materialPropertyRule']['m_Str2'] = str(cur[i][55])
            self.query['shipOrderItem']['material']['materialPropertyRule']['m_Str3'] = str(cur[i][56])
            self.query['shipOrderItem']['material']['materialPropertyRule']['m_Str4'] = str(cur[i][57])
            self.query['shipOrderItem']['material']['materialPropertyRule']['m_Str5'] = str(cur[i][58])
            self.query['shipOrderItem']['material']['materialPropertyRule']['m_Str6'] = str(cur[i][59])
            self.query['shipOrderItem']['material']['materialPropertyRule']['m_Str7'] = str(cur[i][60])
            self.query['shipOrderItem']['material']['materialPropertyRule']['m_Str8'] = str(cur[i][61])
            self.query['shipOrderItem']['material']['materialPropertyRule']['m_Str9'] = str(cur[i][62])
            self.query['shipOrderItem']['material']['materialPropertyRule']['m_Str10'] = str(cur[i][63])
            self.query['shipOrderItem']['material']['materialPropertyRule']['id'] = str(cur[i][37])
            self.query['shipOrderItem']['material']['materialPropertyRule']['lastModificationTime'] = str(cur[i][40])
            self.query['shipOrderItem']['material']['materialPropertyRule']['lastModifierId'] = str(cur[i][41])
            self.query['shipOrderItem']['material']['materialPropertyRule']['creationTime'] = str(cur[i][38])
            self.query['shipOrderItem']['material']['materialPropertyRule']['creatorId'] = str(cur[i][39])
            self.query['shipOrderItem']['material']['packageUnit'][0]['materialId'] = str(cur[i][12])
            self.query['shipOrderItem']['material']['packageUnit'][0]['unit'] = str(cur[i][28])
            self.query['shipOrderItem']['material']['packageUnit'][0]['pkgLevel'] = str(cur[i][27])
            self.query['shipOrderItem']['material']['packageUnit'][0]['convertFigureSmallUnit'] = str(cur[i][29])
            self.query['shipOrderItem']['material']['packageUnit'][0]['convertFigure'] = str(cur[i][30])
            self.query['shipOrderItem']['material']['packageUnit'][0]['id'] = str(cur[i][23])
            self.query['shipOrderItem']['material']['packageUnit'][0]['lastModificationTime'] = str(cur[i][26])
            self.query['shipOrderItem']['material']['packageUnit'][0]['creationTime'] = str(cur[i][25])
            self.query['shipOrderItem']['material']['packageUnit'][0]['creatorId'] = str(cur[i][26])
            self.query['materialProperty']['propertyRuleId'] = str(cur[i][37])
            self.query['materialProperty']['materialId'] = str(cur[i][12])
            self.query['materialProperty']['productionTime'] = str(isNone(cur[i][96]))
            self.query['materialProperty']['receivedTime'] = str(isNone(cur[i][97]))
            self.query['materialProperty']['inboundTime'] = str(isNone(cur[i][98]))
            self.query['materialProperty']['expiredTime'] = str(isNone(cur[i][99]))
            self.query['materialProperty']['AStartTime'] = str(isNone(cur[i][100]))
            self.query['materialProperty']['qcStartTime'] = str(isNone(cur[i][101]))
            self.query['materialProperty']['preservationDays'] = str(isNone(cur[i][102]))
            self.query['materialProperty']['sourceOrderCode'] = str(isNone(cur[i][115]))
            self.query['materialProperty']['batchNo'] = str(isNone(cur[i][103]))
            self.query['materialProperty']['supplierId'] = str(isNone(cur[i][114]))
            self.query['materialProperty']['m_Str1'] = str(isNone(cur[i][104]))
            self.query['materialProperty']['m_Str2'] = str(isNone(cur[i][105]))
            self.query['materialProperty']['m_Str3'] = str(isNone(cur[i][106]))
            self.query['materialProperty']['m_Str4'] = str(isNone(cur[i][107]))
            self.query['materialProperty']['m_Str5'] = str(isNone(cur[i][108]))
            self.query['materialProperty']['m_Str6'] = str(isNone(cur[i][109]))
            self.query['materialProperty']['m_Str7'] = str(isNone(cur[i][110]))
            self.query['materialProperty']['m_Str8'] = str(isNone(cur[i][111]))
            self.query['materialProperty']['m_Str9'] = str(isNone(cur[i][112]))
            self.query['materialProperty']['m_Str10'] = str(isNone(cur[i][113]))

            self.shipOrderIdlist.append(str(cur[i][0]))
            # 将self.query复制出来转换为字符串加到querylist列表中，否则self.query会随着每次循环实时变动
            newquery = str(copy(self.query)).encode('utf-8')
            self.querylist.append(newquery)
        # self.querylist = [str(m).encode('utf-8') for m in self.querylist]  # 将querylist列表中的每个query转为字符类型

        # ms().closeDB()  # 关闭数据库连接
        print(self.querylist)
        print(self.shipOrderIdlist)

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testShipOrderItem(self):
        self.checkResult()

    def tearDown(self):
        print('测试结束，输出log完结\n\n')
        ms().closeDB()  # 关闭数据库连接

    def checkResult(self):
        new_url = url + ':44349' + self.path
        # data1 = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(new_url).query))
        for n in range(len(self.querylist)):  # 根据querylist长度决定请求几次
            print(self.querylist[n])
            info = RunMain().run_main(self.method, headers=self.headers, url=new_url, data=self.querylist[n])
            print('创建发货明细，接口返回：', info)
            if self.case_name == 'shipOrderItem':
                self.assertEqual(info['shipOrderId'], self.shipOrderIdlist[n])


if __name__ == '__main__':
    unittest.main()



