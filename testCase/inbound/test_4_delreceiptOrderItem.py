#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""删除更新时间为最新的、打开状态的收货单的某个收货明细项
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
import uuid

url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'delreceiptOrderItem')


@paramunittest.parametrized(*casexls)
class testdelreceiptOrderItem(unittest.TestCase):
    def setParameters(self, case_name, case_name_ch, method, path, query):
        self.case_name_ch = str(case_name_ch)
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = eval(query)
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()
        self.querylist = []
        cur = ms().getvalue('WMS.ReceiptOrder', 'delreceiptOrderItemId')

        if self.case_name == 'delreceiptOrderItem':
            self.query['creator'] = str(ms().transformNone(cur[0][5]))
            self.query['lastModifier'] = str(ms().transformNone(cur[0][6]))
            self.query['id'] = str(ms().transformNone(cur[0][0]))
            self.query['lastModificationTime'] = cur[0][3].strftime("%Y-%m-%d %H:%M:%S")
            self.query['lastModifierId'] = str(ms().transformNone(cur[0][4]))
            self.query['creationTime'] = cur[0][1].strftime("%Y-%m-%d %H:%M:%S")
            self.query['creatorId'] = str(ms().transformNone(cur[0][2]))
            self.query['receiptOrderId'] = str(ms().transformNone(cur[0][8]))
            self.query['materialId'] = str(ms().transformNone(cur[0][9]))
            self.query['materialPropertyId'] = str(ms().transformNone(cur[0][10]))
            self.query['manufacturer'] = str(ms().transformNone(cur[0][11]))
            self.query['productionDate'] = ms().transformNone(cur[0][12])
            self.query['expirationDate'] = ms().transformNone(cur[0][13])
            self.query['shelvesStatus'] = str(ms().transformNone(cur[0][14]))
            self.query['packageUnitId'] = str(ms().transformNone(cur[0][15]))
            self.query['supplierId'] = str(ms().transformNone(cur[0][7]))
            self.query['expectedPkgQuantity'] = float(cur[0][16])
            self.query['receivedPkgQuantity'] = float(cur[0][17])
            self.query['movedPkgQuantity'] = float(cur[0][18])
            self.query['comments'] = str(ms().transformNone(cur[0][19]))
            self.query['mergeFeatureCode'] = str(ms().transformNone(cur[0][20]))
            self.query['otherCode'] = str(ms().transformNone(cur[0][21]))
            self.query['erpCode'] = str(ms().transformNone(cur[0][22]))
            self.query['rowNo'] = ms().transformNone(cur[0][23])
            self.query['qcStatus'] = str(ms().transformNone(cur[0][24]))
            self.query['ownerUser'] = str(ms().transformNone(cur[0][25]))
            self.query['qualityGrade'] = str(ms().transformNone(cur[0][26]))
            self.query['str1'] = str(ms().transformNone(cur[0][27]))
            self.query['str2'] = str(ms().transformNone(cur[0][28]))
            self.query['str3'] = str(ms().transformNone(cur[0][29]))
            self.query['str4'] = str(ms().transformNone(cur[0][30]))
            self.query['str5'] = str(ms().transformNone(cur[0][31]))
        elif self.case_name == 'delreceiptOrderItem_parametersNotnull':
            self.query['id'] = str(ms().transformNone(cur[0][0]))
            self.query['receiptOrderId'] = str(ms().transformNone(cur[0][8]))
            self.query['materialId'] = str(ms().transformNone(cur[0][9]))
            self.query['materialPropertyId'] = str(ms().transformNone(cur[0][10]))
            self.query['packageUnitId'] = str(ms().transformNone(cur[0][15]))
            self.query['expectedPkgQuantity'] = float(cur[0][16])
            self.query['receivedPkgQuantity'] = float(cur[0][17])
            self.query['movedPkgQuantity'] = float(cur[0][18])
        elif self.case_name == 'delreceiptOrderItem_receiptOrderItemid_null':
            self.query['id'] = ''
            self.query['receiptOrderId'] = str(ms().transformNone(cur[0][8]))
            self.query['materialId'] = str(ms().transformNone(cur[0][9]))
            self.query['materialPropertyId'] = str(ms().transformNone(cur[0][10]))
            self.query['packageUnitId'] = str(ms().transformNone(cur[0][15]))
            self.query['expectedPkgQuantity'] = float(cur[0][16])
            self.query['receivedPkgQuantity'] = float(cur[0][17])
            self.query['movedPkgQuantity'] = float(cur[0][18])
        elif self.case_name == 'delreceiptOrderItem_receiptOrderId_null':
            self.query['id'] = str(ms().transformNone(cur[0][0]))
            self.query['receiptOrderId'] = ''
            self.query['materialId'] = str(ms().transformNone(cur[0][9]))
            self.query['materialPropertyId'] = str(ms().transformNone(cur[0][10]))
            self.query['packageUnitId'] = str(ms().transformNone(cur[0][15]))
            self.query['expectedPkgQuantity'] = float(cur[0][16])
            self.query['receivedPkgQuantity'] = float(cur[0][17])
            self.query['movedPkgQuantity'] = float(cur[0][18])
        elif self.case_name == 'delreceiptOrderItem_materialId_null':
            self.query['id'] = str(ms().transformNone(cur[0][0]))
            self.query['receiptOrderId'] = str(ms().transformNone(cur[0][8]))
            self.query['materialId'] = ''
            self.query['materialPropertyId'] = str(ms().transformNone(cur[0][10]))
            self.query['packageUnitId'] = str(ms().transformNone(cur[0][15]))
            self.query['expectedPkgQuantity'] = float(cur[0][16])
            self.query['receivedPkgQuantity'] = float(cur[0][17])
            self.query['movedPkgQuantity'] = float(cur[0][18])
        elif self.case_name == 'delreceiptOrderItem_materialPropertyId_null':
            self.query['id'] = str(ms().transformNone(cur[0][0]))
            self.query['receiptOrderId'] = str(ms().transformNone(cur[0][8]))
            self.query['materialId'] = str(ms().transformNone(cur[0][9]))
            self.query['materialPropertyId'] = ''
            self.query['packageUnitId'] = str(ms().transformNone(cur[0][15]))
            self.query['expectedPkgQuantity'] = float(cur[0][16])
            self.query['receivedPkgQuantity'] = float(cur[0][17])
            self.query['movedPkgQuantity'] = float(cur[0][18])
        elif self.case_name == 'delreceiptOrderItem_packageUnitId_null':
            self.query['id'] = str(ms().transformNone(cur[0][0]))
            self.query['receiptOrderId'] = str(ms().transformNone(cur[0][8]))
            self.query['materialId'] = str(ms().transformNone(cur[0][9]))
            self.query['materialPropertyId'] = str(ms().transformNone(cur[0][10]))
            self.query['packageUnitId'] = ''
            self.query['expectedPkgQuantity'] = float(cur[0][16])
            self.query['receivedPkgQuantity'] = float(cur[0][17])
            self.query['movedPkgQuantity'] = float(cur[0][18])
        elif self.case_name == 'delreceiptOrderItem_expectedPkgQuantity_null':
            self.query['id'] = str(ms().transformNone(cur[0][0]))
            self.query['receiptOrderId'] = str(ms().transformNone(cur[0][8]))
            self.query['materialId'] = str(ms().transformNone(cur[0][9]))
            self.query['materialPropertyId'] = str(ms().transformNone(cur[0][10]))
            self.query['packageUnitId'] = str(ms().transformNone(cur[0][15]))
            self.query['expectedPkgQuantity'] = ''
            self.query['receivedPkgQuantity'] = float(cur[0][17])
            self.query['movedPkgQuantity'] = float(cur[0][18])
        elif self.case_name == 'delreceiptOrderItem_receiptOrderItemid_error':
            self.query['id'] = uuid.uuid1()
            self.query['receiptOrderId'] = str(ms().transformNone(cur[0][8]))
            self.query['materialId'] = str(ms().transformNone(cur[0][9]))
            self.query['materialPropertyId'] = str(ms().transformNone(cur[0][10]))
            self.query['packageUnitId'] = str(ms().transformNone(cur[0][15]))
            self.query['expectedPkgQuantity'] = float(cur[0][16])
            self.query['receivedPkgQuantity'] = float(cur[0][17])
            self.query['movedPkgQuantity'] = float(cur[0][18])
        elif self.case_name == 'delreceiptOrderItem_receiptOrderid_error':
            self.query['id'] = str(ms().transformNone(cur[0][0]))
            self.query['receiptOrderId'] = uuid.uuid1()
            self.query['materialId'] = str(ms().transformNone(cur[0][9]))
            self.query['materialPropertyId'] = str(ms().transformNone(cur[0][10]))
            self.query['packageUnitId'] = str(ms().transformNone(cur[0][15]))
            self.query['expectedPkgQuantity'] = float(cur[0][16])
            self.query['receivedPkgQuantity'] = float(cur[0][17])
            self.query['movedPkgQuantity'] = float(cur[0][18])

        self.query = str(self.query).encode('utf-8')

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testdelreceiptOrderItem(self):
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
            if self.case_name == 'delreceiptOrderItem':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                sqltext = "select id from WMS.ReceiptOrderItem where id ='{0}' " \
                          "and ReceiptOrderId ='{1}'".format(self.query['id'], self.query['receiptOrderId'])
                newcur = ms().get_all(ms().ExecQuery(sqltext))  # 查询数据库是否有该收货明细
                self.assertFalse(any(x for x in (self.assertIs(info, True, '调用删除收货明细项的接口，返回不是True！'),
                                                 self.assertFalse(newcur[0][0],
                                                                  '收货明细项未删除成功，数据库仍然存在该数据！'))))
            elif self.case_name == 'delreceiptOrderItem_parametersNotnull':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.query = eval(self.query)
                sqltext = "select id from WMS.ReceiptOrderItem where id ='{0}' " \
                          "and ReceiptOrderId ='{1}'".format(self.query['id'], self.query['receiptOrderId'])
                newcur = ms().get_all(ms().ExecQuery(sqltext))  # 查询数据库是否有该收货明细
                self.assertFalse(any(x for x in (self.assertIs(info, True, '调用删除收货明细项的接口，返回不是True！'),
                                                 self.assertFalse(newcur[0][0],
                                                                  '收货明细项未删除成功，数据库仍然存在该数据！'))))
            elif self.case_name == 'delreceiptOrderItem_receiptOrderItemid_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('收货单明细id为空！', info['error'][
                    'message'], '删除收货单明细，收货明细id为空时，接口没有正确的对应处理机制！')
            elif self.case_name == 'delreceiptOrderItem_receiptOrderId_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('收货单id为空！', info['error'][
                    'message'], '删除收货单明细，收货单id为空时，接口没有正确的对应处理机制！')
            elif self.case_name == 'delreceiptOrderItem_materialId_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('物料id为空！', info['error'][
                    'message'], '删除收货单明细，物料id为空时，接口没有正确的对应处理机制！')
            elif self.case_name == 'delreceiptOrderItem_materialPropertyId_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('扩展属性id为空！', info['error'][
                    'message'], '删除收货单明细，扩展属性id为空时，接口没有正确的对应处理机制！')
            elif self.case_name == 'delreceiptOrderItem_packageUnitId_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('包装单位id为空！', info['error'][
                    'message'], '删除收货单明细，包装单位id为空时，接口没有正确的对应处理机制！')
            elif self.case_name == 'delreceiptOrderItem_expectedPkgQuantity_null':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('期望数量为空！', info['error'][
                    'message'], '删除收货单明细，期望数量为空时，接口没有正确的对应处理机制！')
            elif self.case_name == 'delreceiptOrderItem_receiptOrderItemid_error':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('收货明细id信息错误！', info['error'][
                    'message'], '删除收货单明细，收货明细id值错误时，接口没有正确的对应处理机制！')
            elif self.case_name == 'delreceiptOrderItem_receiptOrderid_error':
                print('测试用例中文名：', self.case_name_ch)
                print('接口返回：', info)
                self.assertEqual('收货单id信息错误！', info['error'][
                    'message'], '删除收货单明细，收货单id值错误时，接口没有正确的对应处理机制！')


if __name__ == '__main__':
    unittest.main()



