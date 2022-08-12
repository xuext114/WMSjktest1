#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
该断言有待改进点：1、如果是2伸位出库，1伸位空货载情况下，改进脚本，对其伸1位先做入库完成，再下发出库，以搭建外侧1伸位需要移库或出库的场景
               2、一个发货单中部分物料没有分配到库存时，验证当前库存是否确实没有对应物料了


****************一键下发（分配+生效分配的发货单）最新一个有发货明细，且已生效的发货单******************
判断-发货单中的所有发货明细是否能找到对应在架库存
    判断-如果所有发货明细都找不到对应库存--->【断言】接口应报‘无可用库存’
    判断-如果有至少一个发货明细找到对应库存--->
        循环所有有库存的发货明细，根据每个发货明细对应的发货单code、出库任务类型、发货明细的物料id、批次号、M_str1、M_str2..等扩展属性在mongodb查询是否有符合的任务(是否加入批次号、M_str1、M_str2...等判断条件查询mongodb，根据config.ini文件中[materialProperty]的设置确定)--->
            判断-如果没有查询到该对应任务--->直接【断言失败】
            判断-如果能找到该对应任务--->
                判断-该出库任务的出库货位是单伸货位或双伸货位的1伸位--->直接【断言成功】
                判断-该出库任务的出库货位是双伸货位的2伸位--->
                    判断-该2伸位对应的1伸位是空货位且没有锁定--->直接【断言成功】
                    判断-该2伸位对应的1伸位是空货位，但是锁定了--->【断言】该2伸位的出库任务是否是OPEN状态，不是OPEN则断言失败
                    判断-该2伸位对应的1伸位有载货--->
                        判断-该2伸位对应的1伸位有出库或入库任务--->【断言】该2伸位的出库任务是否是OPEN状态，不是OPEN则断言失败
                        判断-该2伸位对应的1伸位没有出库、入库任务--->
                            判断-该2伸位对应的1伸位没有移库任务信息--->
                                判断-该2伸位的出库任务状态为Working--->直接【断言失败】
                                判断-该2伸位的出库任务状态为OPEN--->【断言成功】2伸位的出库任务如果是OPEN状态,外侧移库任务可以暂时没有
                            判断-该2伸位对应的1伸位有移库任务信息--->
                                判断-该2伸位的出库任务状态为OPEN--->
                                    判断-对应1伸位的移库任务为OPEN状态--->直接【断言失败】
                                    判断-对应1伸位的移库任务为WORKING状态--->直接【断言成功】
                                判断-该2伸位的出库任务状态为WORKING状态--->
                                    判断-对应1伸位的移库任务为OPEN状态--->直接【断言失败】
                                    判断-对应1伸位的移库任务为WORKIND状态--->【断言】移库任务的优先级是否大于出库任务的优先级，大于则断言成功，否则失败
"""

import ast
import os
import unittest
from common.configHttp import RunMain
import paramunittest
from testFile import geturlParams
from testFile import readExcel, readConfig
from testFile.readyaml import readyaml
from common.configDb import MSSQL as ms, Mongo as mg
import random
from testFile.readConfig import ReadConfig as rcon
import time


url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'autoAllocateAndActive')


@paramunittest.parametrized(*casexls)
class testautoAllocateAndActive(unittest.TestCase):
    def setParameters(self, case_name, method, path, query):
        self.case_name = str(case_name)
        spilpath = os.path.split(path)  # 拆分路径，将最后部分拆分出来，返回元祖
        # 将拆分后的路径的前面部分和从数据库获取到的receiptOrderId重新组成一个列表,第一个值后面必须以/结尾，否则后续拼凑后的路径会不正确
        self.spilpathlist = [spilpath[0]+'/', str(ms().getvalue('WMS.ShipOrder', 'Active_ShipOrderId')[0][0])]
        self.path = str(os.path.join(self.spilpathlist[0], self.spilpathlist[1]))  # 用列表的两部分拼凑成新路径
        self.query = str(query)
        self.method = str(method)
        headers1 = readyaml().get_headerIncloudToken()
        headers1['Content-Length'] = '0'  # 将headers中的'Content-Type'值改为0，用于请求体为空的接口
        self.headers = headers1

        # ms().closeDB()  # 关闭数据库连接
        self.query = str(self.query).encode('utf-8')

    #     # 查询发货单中发货明细物料规定的批次号等扩展属性是否需要必填,字段值如果为2代表必填
    #     sqltext1 = """
    # SELECT b.id ShipOrderItemId,c.MaterialId,d.BatchNo,d.M_Str1,d.M_Str2,d.M_Str3,
    # d.M_Str4,d.M_Str5,d.M_Str6,d.M_Str7,d.M_Str8,d.M_Str9,d.M_Str10 --查询字段顺序不能调整
    # FROM WMS.ShipOrder a
    # INNER JOIN WMS.ShipOrderItem b ON a.Id=b.ShipOrderId
    # INNER JOIN WMS.materialProperty c ON b.MaterialPropertyId =c.Id
    # INNER JOIN WMS.materialPropertyRule d ON c.PropertyRuleId=d.Id
    # WHERE a.Id='BAEC83D2-5A00-417A-AA7A-FFFF0100F354'
    #         """#.format(self.spilpathlist[1])
    #     print(sqltext1)
    #     cur1 = ms().get_all(ms().ExecQuery(sqltext1))  # 结果返回二维数组
    #
    #     print(cur1)
    #     global a
    #
    #     a = 0  # 定义一个作为每次循环是否查询出数据的长度初始值
    #     self.ShipOrderCodelist = []
    #     self.MaterialIdlist = []
    #     self.BatchNolist = []
    #     self.M_Str1list = []
    #     self.M_Str2list = []
    #     self.M_Str3list = []
    #     self.M_Str4list = []
    #     self.M_Str5list = []
    #     self.M_Str6list = []
    #     self.M_Str7list = []
    #     self.M_Str8list = []
    #     self.M_Str9list = []
    #     self.M_Str10list = []
    #     self.Docklist = []
    #     # self.addBatchNoquerylist = []
    #     # self.addM_Str1querylist = []
    #     # self.addM_Str2querylist = []
    #     # self.addM_Str3querylist = []
    #     # self.addM_Str4querylist = []
    #     # self.addM_Str5querylist = []
    #     # self.addM_Str6querylist = []
    #     # self.addM_Str7querylist = []
    #     # self.addM_Str8querylist = []
    #     # self.addM_Str9querylist = []
    #     # self.addM_Str10querylist = []
    #     # addquerydict = {}
    #
    #     def isaddquery(name):  # 根据从confiig.ini中获取的扩展属性是否加入物料唯一性判断设置，确定是否加入查询文本
    #         if name == 'BatchNo':
    #             if rcon().get_Property(name) == 1:
    #                 query1 = 'AND s.BatchNo=t.BatchNo'
    #                 query2 = ",{'WmsTask.MaterialProperty.BatchNo': self.BatchNolist[p]}"
    #                 return [query1, query2]
    #             else:
    #                 return ['', '']
    #         else:
    #             if rcon().get_Property(name) == 1:
    #                 query1 = 'AND s.{0}=t.{0}'.format(name)
    #                 query2 = ",{'WmsTask.MaterialProperty.{0}': self.{0}list[p]}".format(name)
    #                 return [query1, query2]
    #             else:
    #                 return ['', '']
    #
    #     for i in range(len(cur1)):  # 根据cur1查询出的涉及发货明细id循环获取该发货单每条发货明细的扩展信息情况及对应是否有相应库存
    #         # def isaddquery():  # 根据查询结果确定是否必填，如果必填，需要在后续的查询语句中加入查询条件
    #         #     if cur1[i][2] == 2:  # 根据查询结果，每行第二个是BatchNo字段, 等于2表示必填
    #         #         query1 = 'AND s.BatchNo=t.BatchNo'
    #         #         query2 = ",{'WmsTask.MaterialProperty.BatchNo': self.BatchNolist[p]}"
    #         #         addquerydict[str(cur1[i][0])] = {'BatchNo': [query1, query2]}
    #         #     elif cur1[i][2] != 2:
    #         #         addquerydict[str(cur1[i][0])] = {'BatchNo': ['', '']}
    #         #     for r in (range(3, 13)):  # 根据查询结果，每行第三个到最后一个分别是M_Str1、M_Str2...字段
    #         #         if cur1[i][r] == 2:  # 等于2表示必填
    #         #             query1 = 'AND isnull(s.M_Str%d,'')=isnull(t.M_Str%d,'')' % (r - 2, r - 2)
    #         #             query2 = ",{'WmsTask.MaterialProperty.M_Str%d': self.M_Str%dlist[p]}" % (r - 2, r - 2)
    #         #             addquerydict[str(cur1[i][0])]['M_Str%d' % (r - 2)] = [query1, query2]
    #         #         elif cur1[i][r] != 2:
    #         #             addquerydict[str(cur1[i][0])]['M_Str%d' % (r - 2)] = ['', '']
    #         #     return addquerydict  # 获取到以ShipOrderItemId为key，各扩展属性为value的类似二维数组
    #         # print(isaddquery())
    #
    #         # 检查当前发货单的发货明细是否至少有一个明细有对应库存，根据materialPropertyRule中规定
    #         # 的（cur1查询结果）BatchNo、M_Str1、M_Str2等扩展属性是否必填确认这些扩展属性是否要加入查找库存的比较
    #         sqltext2 = """
    #                     SELECT DISTINCT t.* FROM
    #             (SELECT n.Id MaterialId,k.BatchNo,k.M_Str1,k.M_Str2,k.M_Str3,k.M_Str4,k.M_Str5,k.M_Str6,k.M_Str7,k.M_Str8,k.M_Str9,k.M_Str10
    #             FROM WMS.InventoryDetail m
    #             INNER JOIN WMS.Material n ON n.Id=m.MaterialId AND m.AllocatedPackageQuantity =0
    #             INNER JOIN WMS.Location j ON m.LocationId=j.Id AND j.LocType = 'STORAGE'
    #             INNER JOIN WMS.MaterialProperty k ON m.MaterialPropertyId = k.Id
    #             ) s --查出在架库存的物料编码及扩展属性
    #             INNER JOIN
    #             (SELECT a.id ShipOrderId,c.MaterialId,c.BatchNo,c.M_Str1,c.M_Str2,c.M_Str3,c.M_Str4,c.M_Str5,c.M_Str6,
    #             c.M_Str7,c.M_Str8,c.M_Str9,c.M_Str10,a.XCode ShipOrderCode,d.Xcode
    #             FROM WMS.ShipOrder a
    #             INNER JOIN WMS.ShipOrderItem b ON a.Id=b.ShipOrderId
    #             INNER JOIN WMS.materialProperty c ON b.MaterialPropertyId =c.Id
    #             INNER JOIN WMS.Dock d ON a.DockId =d.Id
    #             WHERE b.id='{0}'
    #             )t --查询出某个发货单的某个发货明细的物料编码及扩展属性
    #             ON --根据 WMS.materialPropertyRule表中规定的扩展属性是否必填确定是否需要加入BatchNo、M_Str1等其他对比条件
    #             s.MaterialId =t.MaterialId
    #                     """.format(str(cur1[i][0])) + isaddquery('BatchNo')[0] + isaddquery('M_Str1')[0] + \
    #                    isaddquery('M_Str2')[0] + isaddquery('M_Str3')[0] + isaddquery('M_Str4')[0] + \
    #                    isaddquery('M_Str5')[0] + isaddquery('M_Str6')[0] + isaddquery('M_Str7')[0] + \
    #                    isaddquery('M_Str8')[0] + isaddquery('M_Str9')[0] + isaddquery('M_Str10')[0]
    #
    #         print(sqltext2)
    #         cur2 = ms().get_all(ms().ExecQuery(sqltext2))
    #         if cur2 == [(None,)]:
    #             cur2 = []
    #         a = len(cur2) + a  # 若循环完，len(cur2)都为0，则代表所有物料都没有查到对应库存
    #         if len(cur2) > 0:
    #             self.MaterialIdlist.append(cur2[0][1])  # 将每次循环查询出的物料依次添加到列表中
    #             self.BatchNolist.append(cur2[0][2])
    #             self.M_Str1list.append(cur2[0][3])
    #             self.M_Str2list.append(cur2[0][4])
    #             self.M_Str3list.append(cur2[0][5])
    #             self.M_Str4list.append(cur2[0][6])
    #             self.M_Str5list.append(cur2[0][7])
    #             self.M_Str6list.append(cur2[0][8])
    #             self.M_Str7list.append(cur2[0][9])
    #             self.M_Str8list.append(cur2[0][10])
    #             self.M_Str9list.append(cur2[0][11])
    #             self.M_Str10list.append(cur2[0][12])
    #             self.Docklist.append(cur2[0][14])
    #             self.ShipOrderCodelist.append(cur2[0][13])
    #             # # 如果查询有结果返回，将判断扩展属性是否必填得到的mongodb查询条件字符串加到列表中，以备后续mongodb查询使用
    #             # self.addBatchNoquerylist.append(addquerydict[str(cur1[i][0])]['BatchNo'][1])
    #             # self.addM_Str1querylist.append(addquerydict[str(cur1[i][0])]['M_Str1'][1])
    #             # self.addM_Str2querylist.append(addquerydict[str(cur1[i][0])]['M_Str2'][1])
    #             # self.addM_Str3querylist.append(addquerydict[str(cur1[i][0])]['M_Str3'][1])
    #             # self.addM_Str4querylist.append(addquerydict[str(cur1[i][0])]['M_Str4'][1])
    #             # self.addM_Str5querylist.append(addquerydict[str(cur1[i][0])]['M_Str5'][1])
    #             # self.addM_Str6querylist.append(addquerydict[str(cur1[i][0])]['M_Str6'][1])
    #             # self.addM_Str7querylist.append(addquerydict[str(cur1[i][0])]['M_Str7'][1])
    #             # self.addM_Str8querylist.append(addquerydict[str(cur1[i][0])]['M_Str8'][1])
    #             # self.addM_Str9querylist.append(addquerydict[str(cur1[i][0])]['M_Str9'][1])
    #             # self.addM_Str10querylist.append(addquerydict[str(cur1[i][0])]['M_Str10'][1])
    #     print(self.MaterialIdlist)
    #     print(self.BatchNolist)
    #     print(self.M_Str1list)
    #     # print(self.addBatchNoquerylist)
    #     print(a)

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testautoAllocateAndActive(self):
        self.checkResult()

    def tearDown(self):
        print('测试结束，输出log完结\n\n')
        ms().closeDB()  # 关闭数据库连接

    def checkResult(self):
        # 查询发货单中发货明细物料规定的批次号等扩展属性是否需要必填,字段值如果为2代表必填
        sqltext1 = """
        SELECT b.id ShipOrderItemId,c.MaterialId,d.BatchNo,d.M_Str1,d.M_Str2,d.M_Str3,
        d.M_Str4,d.M_Str5,d.M_Str6,d.M_Str7,d.M_Str8,d.M_Str9,d.M_Str10 --查询字段顺序不能调整
        FROM WMS.ShipOrder a 
        INNER JOIN WMS.ShipOrderItem b ON a.Id=b.ShipOrderId
        INNER JOIN WMS.materialProperty c ON b.MaterialPropertyId =c.Id
        INNER JOIN WMS.materialPropertyRule d ON c.PropertyRuleId=d.Id
        WHERE a.Id='{0}'
                """ .format(self.spilpathlist[1])
        print(sqltext1)
        cur1 = ms().get_all(ms().ExecQuery(sqltext1))  # 结果返回二维数组

        print(cur1)
        global a

        a = 0  # 定义一个作为每次循环是否查询出数据的长度初始值
        ShipOrderCodelist = []
        MaterialIdlist = []
        BatchNolist = []
        M_Str1list = []
        M_Str2list = []
        M_Str3list = []
        M_Str4list = []
        M_Str5list = []
        M_Str6list = []
        M_Str7list = []
        M_Str8list = []
        M_Str9list = []
        M_Str10list = []
        Docklist = []

        # self.addBatchNoquerylist = []
        # self.addM_Str1querylist = []
        # self.addM_Str2querylist = []
        # self.addM_Str3querylist = []
        # self.addM_Str4querylist = []
        # self.addM_Str5querylist = []
        # self.addM_Str6querylist = []
        # self.addM_Str7querylist = []
        # self.addM_Str8querylist = []
        # self.addM_Str9querylist = []
        # self.addM_Str10querylist = []
        # addquerydict = {}

        def isaddquery(name):  # 根据从confiig.ini中获取的扩展属性是否加入物料唯一性判断设置，确定是否加入查询文本
            if name == 'BatchNo':
                if rcon().get_Property(name) == '1':
                    query1 = 'AND s.BatchNo=t.BatchNo'
                    query2 = ",{'WmsTask.MaterialProperty.BatchNo': BatchNolist[p]}"
                    return [query1, query2]
                else:
                    return ['', '']
            else:
                if rcon().get_Property(name) == '1':
                    query1 = 'AND s.{0}=t.{0}'.format(name)
                    query2 = ",{'WmsTask.MaterialProperty.%s': %slist[p]}" % (name, name)
                    return [query1, query2]
                else:
                    return ['', '']

        for i in range(len(cur1)):  # 根据cur1查询出的涉及发货明细id循环获取该发货单每条发货明细的扩展信息情况及对应是否有相应库存
            # def isaddquery():  # 根据查询结果确定是否必填，如果必填，需要在后续的查询语句中加入查询条件
            #     if cur1[i][2] == 2:  # 根据查询结果，每行第二个是BatchNo字段, 等于2表示必填
            #         query1 = 'AND s.BatchNo=t.BatchNo'
            #         query2 = ",{'WmsTask.MaterialProperty.BatchNo': self.BatchNolist[p]}"
            #         addquerydict[str(cur1[i][0])] = {'BatchNo': [query1, query2]}
            #     elif cur1[i][2] != 2:
            #         addquerydict[str(cur1[i][0])] = {'BatchNo': ['', '']}
            #     for r in (range(3, 13)):  # 根据查询结果，每行第三个到最后一个分别是M_Str1、M_Str2...字段
            #         if cur1[i][r] == 2:  # 等于2表示必填
            #             query1 = 'AND isnull(s.M_Str%d,'')=isnull(t.M_Str%d,'')' % (r - 2, r - 2)
            #             query2 = ",{'WmsTask.MaterialProperty.M_Str%d': self.M_Str%dlist[p]}" % (r - 2, r - 2)
            #             addquerydict[str(cur1[i][0])]['M_Str%d' % (r - 2)] = [query1, query2]
            #         elif cur1[i][r] != 2:
            #             addquerydict[str(cur1[i][0])]['M_Str%d' % (r - 2)] = ['', '']
            #     return addquerydict  # 获取到以ShipOrderItemId为key，各扩展属性为value的类似二维数组
            # print(isaddquery())

            # 检查当前发货单的发货明细是否至少有一个明细有对应库存，根据materialPropertyRule中规定
            # 的（cur1查询结果）BatchNo、M_Str1、M_Str2等扩展属性是否必填确认这些扩展属性是否要加入查找库存的比较
            sqltext2 = """
                            SELECT DISTINCT t.* FROM 
                    (SELECT n.Id MaterialId,k.BatchNo,k.M_Str1,k.M_Str2,k.M_Str3,k.M_Str4,k.M_Str5,k.M_Str6,k.M_Str7,k.M_Str8,k.M_Str9,k.M_Str10
                    FROM WMS.InventoryDetail m
                    INNER JOIN WMS.Material n ON n.Id=m.MaterialId AND m.AllocatedPackageQuantity =0 
                    INNER JOIN WMS.Location j ON m.LocationId=j.Id AND j.LocType = 'STORAGE' 
                    INNER JOIN WMS.MaterialProperty k ON m.MaterialPropertyId = k.Id
                    ) s --查出在架库存的物料编码及扩展属性
                    INNER JOIN 
                    (SELECT a.id ShipOrderId,c.MaterialId,c.BatchNo,c.M_Str1,c.M_Str2,c.M_Str3,c.M_Str4,c.M_Str5,c.M_Str6,
                    c.M_Str7,c.M_Str8,c.M_Str9,c.M_Str10,a.XCode ShipOrderCode,d.Xcode 
                    FROM WMS.ShipOrder a 
                    INNER JOIN WMS.ShipOrderItem b ON a.Id=b.ShipOrderId
                    INNER JOIN WMS.materialProperty c ON b.MaterialPropertyId =c.Id
                    INNER JOIN WMS.Dock d ON a.DockId =d.Id
                    WHERE b.id='{0}'
                    )t --查询出某个发货单的某个发货明细的物料编码及扩展属性
                    ON --根据 WMS.materialPropertyRule表中规定的扩展属性是否必填确定是否需要加入BatchNo、M_Str1等其他对比条件
                    s.MaterialId =t.MaterialId 
                            """.format(str(cur1[i][0])) + isaddquery('BatchNo')[0] + isaddquery('M_Str1')[0] + \
                       isaddquery('M_Str2')[0] + isaddquery('M_Str3')[0] + isaddquery('M_Str4')[0] + \
                       isaddquery('M_Str5')[0] + isaddquery('M_Str6')[0] + isaddquery('M_Str7')[0] + \
                       isaddquery('M_Str8')[0] + isaddquery('M_Str9')[0] + isaddquery('M_Str10')[0]

            print(sqltext2)
            cur2 = ms().get_all(ms().ExecQuery(sqltext2))
            if cur2 == [(None,)]:
                cur2 = []
            a = len(cur2) + a  # 若循环完，len(cur2)都为0，则代表所有物料都没有查到对应库存
            if len(cur2) > 0:
                MaterialIdlist.append(cur2[0][1])  # 将每次循环查询出的物料依次添加到列表中
                BatchNolist.append(cur2[0][2])
                M_Str1list.append(cur2[0][3])
                M_Str2list.append(cur2[0][4])
                M_Str3list.append(cur2[0][5])
                M_Str4list.append(cur2[0][6])
                M_Str5list.append(cur2[0][7])
                M_Str6list.append(cur2[0][8])
                M_Str7list.append(cur2[0][9])
                M_Str8list.append(cur2[0][10])
                M_Str9list.append(cur2[0][11])
                M_Str10list.append(cur2[0][12])
                Docklist.append(cur2[0][14])
                ShipOrderCodelist.append(cur2[0][13])
                # # 如果查询有结果返回，将判断扩展属性是否必填得到的mongodb查询条件字符串加到列表中，以备后续mongodb查询使用
                # self.addBatchNoquerylist.append(addquerydict[str(cur1[i][0])]['BatchNo'][1])
                # self.addM_Str1querylist.append(addquerydict[str(cur1[i][0])]['M_Str1'][1])
                # self.addM_Str2querylist.append(addquerydict[str(cur1[i][0])]['M_Str2'][1])
                # self.addM_Str3querylist.append(addquerydict[str(cur1[i][0])]['M_Str3'][1])
                # self.addM_Str4querylist.append(addquerydict[str(cur1[i][0])]['M_Str4'][1])
                # self.addM_Str5querylist.append(addquerydict[str(cur1[i][0])]['M_Str5'][1])
                # self.addM_Str6querylist.append(addquerydict[str(cur1[i][0])]['M_Str6'][1])
                # self.addM_Str7querylist.append(addquerydict[str(cur1[i][0])]['M_Str7'][1])
                # self.addM_Str8querylist.append(addquerydict[str(cur1[i][0])]['M_Str8'][1])
                # self.addM_Str9querylist.append(addquerydict[str(cur1[i][0])]['M_Str9'][1])
                # self.addM_Str10querylist.append(addquerydict[str(cur1[i][0])]['M_Str10'][1])
        print(MaterialIdlist)
        print(BatchNolist)
        print(M_Str1list)
        print(ShipOrderCodelist)
        # print(self.addBatchNoquerylist)
        print(a)
        if self.case_name == 'autoAllocateAndActive':
            new_url = url + ':44349' + self.path
            print('接口url为：', new_url)
            info = RunMain().run_main(self.method, headers=self.headers, url=new_url)
            print('一键发货发货单，结果返回：', info)
            print('等待8秒钟，确定任务数据已插入mongodb')
            time.sleep(8)  # 等待6秒钟，确定数据已插入mongodb

            if a == 0:  # 发货单中的发货明细都没有找到对应库存
                self.assertEqual(info['error']['message'], '无可用库存！')
            else:  # 发货单中有物料找到了对应库存
                for p in range(len(MaterialIdlist)):
                    # mgtext1 = """{"$and": [{'OriginBillCode': self.ShipOrderCodelist[p]}, {'TaskType': 'MV_PICKTICKET_PICKING'},
                    #      {'WmsTask.MaterialProperty.MaterialId': self.MaterialIdlist[p]}""" + \
                    #           self.addBatchNoquerylist[p] + self.addM_Str1querylist[p] + self.addM_Str2querylist[p] +\
                    #           self.addM_Str3querylist[p] + self.addM_Str4querylist[p] + self.addM_Str5querylist[p] + \
                    #           self.addM_Str6querylist[p] + self.addM_Str7querylist[p] + self.addM_Str8querylist[p] +\
                    #           self.addM_Str9querylist[p] + self.addM_Str10querylist[p] + ']}'

                    #  拼接到mongodb找正在执行或已经打开状态的下架任务的查询条件
                    mgtext1 = """{"$and": [{'OriginBillCode': ShipOrderCodelist[p]}, {'TaskType': 'MV_PICKTICKET_PICKING'},{'WmsTask.MaterialProperty.MaterialId': str(MaterialIdlist[p])}""" + \
                              isaddquery('BatchNo')[1] + isaddquery('M_Str1')[1] + isaddquery('M_Str2')[1] + \
                              isaddquery('M_Str3')[1] + isaddquery('M_Str4')[1] + isaddquery('M_Str5')[1] + \
                              isaddquery('M_Str6')[1] + isaddquery('M_Str7')[1] + isaddquery('M_Str8')[1] + \
                              isaddquery('M_Str9')[1] + isaddquery('M_Str10')[1] + ']}'
                    # mgtext2 = """{"$and": [{'OriginBillCode': ShipOrderCodelist[p]},{'TaskType': 'MV_PICKTICKET_PICKING'},{'WmsTask.MaterialProperty.MaterialId': MaterialIdlist[p]},{'WmsTask.MaterialProperty.BatchNo': BatchNolist[p]}]}"""
                    print(mgtext1)
                    # 在mongodb的MiddlewareTask集合中查询是否有对应的任务数据
                    doc1 = mg().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find(eval(mgtext1))
                    d = {}
                    for docment in doc1:  # 获取到doc1的任务数据，字典形式展示
                        d = docment
                    if len(d) == 0:  # 如果查询mongodb没有结果返回，直接断言失败
                        self.assertLess(0, len(d), 'mongodb没有查询到%s的出库任务数据' % str(MaterialIdlist[p]))
                    else:
                        FromLocLocId = d['FromLocLocId']  # 根据查询到的mongodb数据获取下架货位id
                        print('FromLocLocId的值为：', FromLocLocId)
                        sqltext3 = "SELECT id, XDepth FROM WMS.Location WHERE Id ='%s'" % FromLocLocId
                        print('sqltext3查询语句为：', sqltext3)
                        # 根据下架货位id在数据库中查询是否为双伸货位
                        cur3 = ms().get_all(ms().ExecQuery(sqltext3))
                        if cur3[0][1] == 1 or cur3 == [(None,)]:  # 如果是双伸货位的伸1位或单伸货位
                            self.assertLess(0, len(d))  # 有该出库任务，直接断言成功
                        else:  # cur3[0][1]等于2，则表示是双伸位的伸2位
                            # 查询该2伸位对应的1伸位是否载货
                            sqltext4 = """SELECT b.NearEndId, a.IsLoaded, a.IsLocked FROM WMS.Location a INNER JOIN WMS.DUnit b
                            ON a.Id =b.NearEndId AND FarEndId='{0}'""".format(cur3[0][0])
                            print('sqltext4查询语句为：', sqltext4)
                            cur4 = ms().get_all(ms().ExecQuery(sqltext4))
                            # 查询mongodb中该伸2位的出库任务信息是否为open状态
                            doc5 = mg().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({
                                "$and": [{'TaskType': 'MV_PICKTICKET_PICKING'}, {
                                    'FromLocLocId': str(cur3[0][0]).lower()}, {'TaskStatus': 'OPEN'}]})
                            d2 = {}
                            for doc5ment in doc5:  # 获取到doc5的任务数据，以字典形式展示
                                d2 = doc5ment

                            if cur4[0][1] == 'N' and cur4[0][2] == 'N':  # 如果IsLoaded=N，IsLocked=N,则表示1伸位是空货位,没有锁定
                                self.assertLess(0, len(d))  # 有该出库任务，直接断言成功
                            elif cur4[0][1] == 'N' and cur4[0][2] == 'Y':  # 1伸位为空货位且是锁定状态时
                                self.assertLess(0, len(d2), '1伸位为空货位锁定状态时，2伸位的出库任务不是open状态')
                            else:  # 如果IsLoaded=Y，表示1伸位有货
                                print('2伸位出库时，1伸位货位有货载')
                                # 如果有结果返回，表示1伸位的货位有出库任务
                                doc2 = mg().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({"$and": [
                                    {'TaskType': 'MV_PICKTICKET_PICKING'}, {'FromLocLocId': str(cur4[0][0]).lower()}]})
                                # 如果有结果返回，表示1伸位的货位有入库任务
                                doc3 = mg().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({"$and": [
                                    {'TaskType': 'MV_PUTAWAY'}, {'ToLocId': str(cur4[0][0]).lower()}]})
                                # 如果有结果返回，表示1伸位的货位有移库任务
                                doc4 = mg().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({"$and": [
                                    {'TaskType': 'MV_MOVE'}, {'FromLocLocId': str(cur4[0][0]).lower()}, {
                                        'TaskStatus': 'WORKING'}]})
                                d3 = {}
                                for doc4ment in doc4:  # 获取doc4的任务数据，以字典形式展示
                                    d3 = doc4ment

                                if mg().ResultisNotNone(doc2) or mg().ResultisNotNone(doc3):  # 如果外侧1伸位有出库或入库任务
                                    print('2伸位出库时，1伸位有出库或入库任务')
                                    # 如果1伸位有入库或出库任务，则查询该2伸位的出库任务状态试是否为‘OPEN’
                                    self.assertLess(0, len(d2), '1伸位有出库或入库任务时，2伸位出库任务状态不是open')
                                else:  # 如果1伸位没有入库、出库任务
                                    print('2伸位出库时，1伸位没有出库或入库任务')
                                    print('等待4秒，等待移库任务信息添加进mongodb（若有）')
                                    time.sleep(4)  # 等待四秒，等待移库任务信息添加进mongodb（若有）

                                    # 查询2伸位的working状态的出库任务信息
                                    doc6 = mg().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({
                                        "$and": [{'TaskType': 'MV_PICKTICKET_PICKING'}, {
                                            'FromLocLocId': str(cur3[0][0]).lower()}, {'TaskStatus': 'WORKING'}]})
                                    # 查询1伸位的移库任务信息
                                    doc7 = mg().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({
                                        "$and": [{'TaskType': 'MV_MOVE'}, {'FromLocLocId': str(cur4[0][0]).lower()}]})
                                    d4 = {}
                                    for doc6ment in doc6:
                                        d4 = doc6ment
                                        print('2伸位Working状态的出库任务：', d4)

                                    d5 = {}
                                    for doc5ment in doc7:
                                        d5 = doc5ment
                                        print('1伸位移库任务：', d5)

                                    if len(d5) == 0:  # 在1伸位没有出库、入库、也没有移库任务的情况下
                                        print('2伸位出库时，1伸位没有出库、入库任务，也没有移库任务')
                                        if len(d4) > 0:  # 2伸位的出库任务如果是working状态，断言失败
                                            self.assertEqual(1, 2, '在1伸位没有出库、入库、也没有移库任务的情况下，2伸位的出库任务不可能是working状态，断言失败')
                                        else:  # 2伸位的出库任务如果是OPEN状态,移库任务可以没有
                                            self.assertEqual(1, 1)
                                    else:  # 在1伸位没有出库、入库,有移库任务的情况下
                                        print('2伸位出库时，1伸位没有出库、入库任务，有移库任务')
                                        doc8 = mg().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({
                                            "$and": [{'TaskType': 'MV_PICKTICKET_PICKING'}, {'FromLocLocId': str(cur3[0][0]).lower()}, {
                                                'TaskStatus': 'OPEN'}]})
                                        doc9 = mg().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({
                                            "$and": [{'TaskType': 'MV_MOVE'}, {'FromLocLocId': str(cur4[0][0]).lower()}, {
                                                'TaskStatus': 'OPEN'}]})

                                        if mg().ResultisNotNone(doc8) is True:  # 如果2伸位的出库任务是打开状态
                                            print('2伸位的出库任务是打开状态时，1伸位有移库任务')
                                            if mg().ResultisNotNone(doc9) is True:  # 如果1伸位的移库任务也是打开状态
                                                print('2伸位的出库任务是打开状态时，1伸位有移库任务也是打开状态')
                                                self.assertEqual(1, 2, '2伸位的出库任务是open状态时，1伸位的移库任务不可能是OPEN状态，断言失败')
                                            else:  # 如果1伸位的移库任务是WORKING状态
                                                print('2伸位的出库任务是打开状态时，1伸位有移库任务是WORKING状态')
                                                self.assertEqual(1, 1)  # 2伸位的出库任务是OPEN状态时，1伸位的移库任务应该是WORKING状态
                                        elif len(d4) > 0:  # 如果2伸位的出库任务是WORKING状态
                                            if mg().ResultisNotNone(doc9) is True:  # 如果1伸位的移库任务是OPEN状态
                                                self.assertEqual(1, 2, '如果2伸位出库任务是WORKING状态，1伸位移库任务不可能是OPEN状态，断言失败')
                                            else:  # 如果1伸位的移库任务是WORKING状态
                                                self.assertLess(int(d4['Proirity']), int(d3['Proirity']), '出库任务的优先级比移库任务的优先级高')


if __name__ == '__main__':
    # testinboundActive(unittest.TestCase)
    unittest.main()

