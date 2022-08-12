#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymssql
from testFile.readConfig import ReadConfig as readconfig
from testFile.readSql import get_sql
import pymongo
from redis import StrictRedis, ConnectionPool


class MSSQL:
    """def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db """
    global host, user, pwd, db, port, server, encoding, tds_version

    host = readconfig().get_db('host')
    port = 1433
    server = readconfig().get_db('server')
    user = readconfig().get_db('username')
    pwd = readconfig().get_db('password')
    db = readconfig().get_db('database')
    encoding = 'utf-8'
    # tds_version = '7.1'

    def GetConnect(self):
        """
        连接方法
        :return:
        """
        if not db:
            raise(NameError, '没有设置数据库信息')
        self.conn = pymssql.connect(host=host, port=port, server=server, user=user, password=pwd,
                                    database=db)
        cur = self.conn.cursor()
        if not cur:
            raise(NameError, '连接数据库失败')
        else:
            return cur

    def ExecQuery(self, sql):
        """
        执行查询语句，返回是一个包含tuple的list，tuple的元素是每行记录的字段
        :param sql:
        :return:
        """
        cur = self.GetConnect()
        cur.execute(sql)
        # resList = cur.fetchall()
        # 查询完毕后，需要关闭连接
        # self.conn.close()
        return cur

    def ExecNonQuery(self, sql):
        """
        执行非查询语句
        :param sql:
        :return:
        """
        cur = self.GetConnect()
        cur.execute(sql)
        self.conn.commit()
        return cur

    def get_all(self, cur):
        value = cur.fetchall()  # 得到一个列表中包含元组的类似二维数组
        if value:
            return value
        else:
            return [('',)]

    def get_one(self, cur):
        """
        取查询结果的一条数据，将每个字段数据加载到列表中
        :param cur:
        :return:
        """
        p = []
        value = cur.fetchone()
        for i in value:
            p.append(i)
        return p


    """
    def get_one(self, cur):
        p = []
        try:
            value = cur.fetchone()
            if value:
                for i in value:
                    p.append(i)
            else:
                raise Exception(print('数据库未查询到符合条件的值！'))
        except Exception as e:
            print('出现异常：', e)
        return p
    """

    def getvalue(self, tabname, sql_id):
        value = self.get_all(self.ExecQuery(get_sql(tabname, sql_id)))
        return value

    def transformNone(self, value):
        """
        如果值是None，转换为''
        :param value:
        :return:
        """
        if value is None or value == 'None':
            return ''
        else:
            return value

    def closeDB(self):
        self.GetConnect().close()
        print('数据库连接关闭.')


class Mongo():
    global mongohost, mongoport

    mongohost = readconfig().get_mongodb('host')
    mongoport = int(readconfig().get_mongodb('port'))

    def GetMongoConnect(self):
        """
        连接mongodb
        :return:
        """
        if not mongohost or not mongoport:
            raise (ConnectionError, '没有设置数据库信息！')
        client = pymongo.MongoClient(mongohost,mongoport)
        return client

    def MongoExecquery(self, mongodb, col):
        """
        获取想要的集合
        :param mongodb:
        :param col:
        :return:
        """
        client = self.GetMongoConnect()
        Mdb = client[mongodb]
        Mcol = Mdb[col]
        return Mcol

    def ResultisNotNone(self, doc):
        """
        doc代表对集合的查询结果
        :param doc:
        :return:
        """
        doclist = list(doc)
        if len(doclist) != 0:  # 如果有结果返回
            return True
        else:
            return False

    def get_mongodata(self, doc):
        """
        获取从mongodb查询到的数据，以列表中包含字典元素形式展示
        :param doc:
        :return:
        """
        d = []
        for docelement in doc:
            d.append(docelement)
        return d

class Rds():
    def GetRedisConnect(self, db=0):  # 连接redis
        pool = ConnectionPool(host=readconfig().get_redis('host'), port=readconfig().get_redis('port'), db=db)
        r = StrictRedis(connection_pool=pool)
        return r


if __name__ == '__main__':
    # ms = MSSQL().GetConnect()
    # sql = MSSQL().ExecQuery("SELECT Id FROM WMS.BillType WHERE XType='RECEIVE' AND XName='生产入库1'")
    # # sql = MSSQL().ExecQuery(get_sql('WMS.Orgnization', 'supplierId'))
    # data = MSSQL().get_all(sql)
    # print(data[0][0])
    # cur = MSSQL().getvalue('WMS.ReceiptOrder', 'delreceiptOrderItemId')
    # print(cur)
    # print(cur[0][11])
    # if cur[0][11] is None:
    #     data1 = MSSQL().transformNone(cur[0][11])
    #     print('请求', data1)
    sql = "SELECT * FROM WMS.ReceiptOrder WHERE XCode='RO202202090002'"
    cur = MSSQL().get_all(MSSQL().ExecQuery(sql))
    print(cur)


    # data1 = MSSQL().getvalue('WMS.WmsTask', 'Pallet')[0][0]
    # data2 = MSSQL().getvalue('WMS.ReceiptOrder', 'receiptOrderItem')[1]
    # # print(data1)
    # print(data2)
    # MSSQL().closeDB()

    # mycol = Mongo().MongoExecquery('GSMiddleWare', 'TaskBase')
    # mydoc = mycol.find({"$and": [{'Pallets': 'TP406'}, {'TaskType': '入口到外形检测'}]})
    # re = Mongo().ResultisNone(mydoc)
    # print(re)
    # doc1 = Mongo().MongoExecquery('GSMiddleWare', 'TaskBase').find({'TaskType': '入口到外形检测'})
    # for x in doc1:
    #     print(x)
    # doc2 = Mongo().MongoExecquery('GSMiddleWare', 'ArchivedTaskBase').find({"$and": [
    #     {'TaskCode': '20211224151542816'}, {'TaskType': '外形检测异常回退'}, {'CompleteStatus': 0}]})
    # for y in doc2:
    #     print(y)
    # print(Rds().GetRedisConnect().hget('GSMiddleWare:lockStation', '00-001-1020').decode())
    # print(Rds().GetRedisConnect().hlen('GSMiddleWare:lockStation'))

    # doc1 = Mongo().MongoExecquery('GSMiddleWare', 'TaskBase').find({"$and": [{'Pallets': "TP418"}, {'TaskType': '入口到外形检测'}]})
    # re = Mongo().ResultisNone(doc1)
    # print(re)
    #
    # sqltext1 = """
    # SELECT b.id ShipOrderItemId,c.MaterialId,d.BatchNo,d.M_Str1,d.M_Str2,d.M_Str3,
    # d.M_Str4,d.M_Str5,d.M_Str6,d.M_Str7,d.M_Str8,d.M_Str9,d.M_Str10
    # FROM WMS.ShipOrder a
    # INNER JOIN WMS.ShipOrderItem b ON a.Id=b.ShipOrderId
    # INNER JOIN WMS.materialProperty c ON b.MaterialPropertyId =c.Id
    # INNER JOIN WMS.materialPropertyRule d ON c.PropertyRuleId=d.Id
    # WHERE a.Id='49E55545-1DC3-4F67-8593-FFFF00FC65AF'
    #         """
    # print(sqltext1)
    # cur1 = MSSQL().get_all(MSSQL().ExecQuery(sqltext1))  # 结果返回二维数组
    # print(cur1)
    # for i in range(len(cur1)):  # 根据cur1查询出的涉及发货明细id循环获取该发货单每条发货明细的扩展信息情况及对应是否有相应库存
    #     def isaddquery(r):  # 根据查询结果确定是否必填，如果必填，需要在后续的查询语句中假如查询条件
    #         if r == 2:  # 根据查询结果，每行第二个是BatchNo字段
    #             if cur1[i][r] == 2:  # 等于2表示必填
    #                 query1 = 'AND s.BatchNo=t.BatchNo'
    #                 query2 = ",{'WmsTask.MaterialProperty.BatchNo': self.BatchNolist[p]}"
    #                 return [query1, query2]
    #             else:
    #                 return ['', '']
    #         else:  # 根据查询结果，每行第三个到最后一个分别是M_Str1、M_Str2...字段
    #             if cur1[i][r] == 2:  # 等于2表示必填
    #                 query1 = 'AND isnull(s.M_Str%d,'')=isnull(t.M_Str%d,'')' % (r - 2, r - 2)
    #                 query2 = ",{'WmsTask.MaterialProperty.M_Str%d': self.M_Str%dlist[p]}" % (r - 2, r - 2)
    #                 return [query1, query2]
    #             else:
    #                 return ['', '']
    #
    #     print(isaddquery(2))
    #
    #     # 检查当前发货单的发货明细是否至少有一个明细有对应库存，根据materialPropertyRule中规定
    #     # 的（cur1查询结果）BatchNo、M_Str1、M_Str2等扩展属性是否必填确认这些扩展属性是否要加入查找库存的比较
    # ShipOrderCodelist = ['SO202201050003', 'SO202201050003', 'SO202201050003']
    # MaterialIdlist = ['17f3d726-98ed-4f26-94b0-299b05ea557d', '499809da-12a9-493b-9f9e-299c17cf49ab','df9e7c78-2ef2-41d9-9982-299be9c59c04']
    # BatchNolist = ['202110260009', '20211226102509', '20211226103753']
    # for p in range(len(MaterialIdlist)):
    #     mgtext1 = """{"$and": [{'OriginBillCode': ShipOrderCodelist[p]},{'TaskType': 'MV_PICKTICKET_PICKING'},{'WmsTask.MaterialProperty.MaterialId': MaterialIdlist[p]},{'WmsTask.MaterialProperty.BatchNo': BatchNolist[p]}]}"""
    #     mgtext2 = """{"$and": [{'OriginBillCode': ShipOrderCodelist[p]},{'TaskType': 'MV_PICKTICKET_PICKING'},{'WmsTask.MaterialProperty.MaterialId': MaterialIdlist[p]},{'WmsTask.MaterialProperty.BatchNo': BatchNolist[p]}]}"""
    #
    #     print(mgtext1)
    #     doc1 = Mongo().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find(eval(mgtext2))
    #     for doc in doc1:
    #         print(doc)

    # sqltext3 = """SELECT b.NearEndId FROM WMS.Location a INNER JOIN WMS.DUnit b
    # ON a.Id =b.NearEndId AND a.IsLoaded ='Y' AND FarEndId='{0}'""".format('72771813-7deb-474a-a624-e6f89e9ee271')
    # cur4 = MSSQL().get_all(MSSQL().ExecQuery(sqltext3))
    # print(cur4)

    # MaterialIdlist = ['4c5667c5-9798-4f85-9c48-299ae16c3ad3', 'df9e7c78-2ef2-41d9-9982-299be9c59c04',
    #                   'b471332f-6cf4-4328-8b25-299b735a9625', '17f3d726-98ed-4f26-94b0-299b05ea557d',
    #                   '387807c9-f8f1-49a7-a846-299a885b6ca4']
    # BatchNolist = ['20220106', '20220106', '20211226102509', '202110200010', '20211226102509']
    # ShipOrderCodelist = ['SO202201070002', 'SO202201070002', 'SO202201070002', 'SO202201070002', 'SO202201070002']
    # mgtext1 ="""{"$and": [{'OriginBillCode': 'SO202201070002'}, {'TaskType': 'MV_PICKTICKET_PICKING'},{'WmsTask.MaterialProperty.MaterialId': 'df9e7c78-2ef2-41d9-9982-299be9c59c04'},{'WmsTask.MaterialProperty.BatchNo': '20220106'}]}"""
    # doc1 = Mongo().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find(eval(mgtext1))
    # d = {}
    # for docment in doc1:  # 获取到doc1的任务数据，字典形式展示
    #     print(docment)
    # sqltext3 = """SELECT id, XDepth FROM WMS.Location WHERE Id ='9966FBAC-7342-4AC2-9556-E6F89E9EE66B'"""
    # cur3 = MSSQL().get_all(MSSQL().ExecQuery(sqltext3))
    # sqltext4 = """SELECT b.NearEndId, a.IsLoaded, a.IsLocked FROM WMS.Location a INNER JOIN WMS.DUnit b
    #                             ON a.Id =b.NearEndId AND FarEndId='9966FBAC-7342-4AC2-9556-E6F89E9EE66B'"""
    # cur4 = MSSQL().get_all(MSSQL().ExecQuery(sqltext4))
    # doc8 = Mongo().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({
    #     "$and": [{'TaskType': 'MV_PICKTICKET_PICKING'}, {'FromLocLocId': '9966fbac-7342-4ac2-9556-e6f89e9ee66b'}, {
    #         'TaskStatus': 'OPEN'}]})
    # doc9 = Mongo().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({
    #     "$and": [{'TaskType': 'MV_MOVE'}, {'FromLocLocId': str(cur4[0][0]).lower()}, {
    # #         'TaskStatus': 'OPEN'}]})
    # doc2 = Mongo().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({"$and": [
    #     {'TaskType': 'MV_PICKTICKET_PICKING'}, {'FromLocLocId': '650e1069-8f50-4453-a6d5-e6f89e9ee27a'.lower()}]})
    # for a in Mongo().get_mongodata(doc2):
    #     print(a)
    # # 如果有结果返回，表示1伸位的货位有入库任务
    # doc3 = Mongo().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({"$and": [
    #     {'TaskType': 'MV_PUTAWAY'}, {'ToLocId': str(cur4[0][0]).lower()}]})
    # doc7 = Mongo().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({
    #     "$and": [{'TaskType': 'MV_MOVE'}, {'FromLocLocId': str(cur4[0][0]).lower()}]})
    #
    # print(Mongo().ResultisNotNone(doc8))
    # print(Mongo().ResultisNotNone(doc9))
    # print(Mongo().ResultisNotNone(doc2))
    # print(Mongo().ResultisNotNone(doc3))
    # print(Mongo().ResultisNotNone(doc7))
    # doc1 = Mongo().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({
    #     "$and": [{'TaskStatus': 'WORKING'}, {
    #         'TaskType': {'$in': ['MV_PICKTICKET_PICKING', 'MV_PUTAWAY', 'MV_MOVE']}}]})
    # for a in Mongo().get_mongodata(doc1):
    #     doc2 = Mongo().MongoExecquery('GSMiddleWare', 'TaskBase').find({'TaskCode': a['TaskCode']})
    #     taskdata = Mongo().get_mongodata(doc2)
    #     print(taskdata)
    # Rds().GetRedisConnect().hdel('GSMiddleWare:lockStation', '00-001-1019')

    # taskdata = []
    # doc1 = Mongo().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({
    #     "$and": [{'TaskStatus': 'WORKING'}, {
    #         'TaskType': {'$in': ['MV_PICKTICKET_PICKING', 'MV_PUTAWAY', 'MV_MOVE']}}]})
    # # 根据从MiddlewareTask集合中查询到的TaskCode获取更详细任务信息用以给接口传参
    # for a in Mongo().get_mongodata(doc1):
    #     doc2 = Mongo().MongoExecquery('GSMiddleWare', 'TaskBase').find({'TaskCode': a['TaskCode']})
    #     taskdata.append(Mongo().get_mongodata(doc2))
    # print('重新获取当前正在在执行状态的出入库、移库任务信息：', taskdata)

    # doc2 = Mongo().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({"$and": [
    #     {'TaskType': 'MV_PICKTICKET_PICKING'}, {'FromLocLocId': '650e1069-8f50-4453-a6d5-e6f89e9ee27a'.lower()}]})
    # doc3 = Mongo().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({"$and": [
    #                                 {'TaskType': 'MV_PUTAWAY'}, {'ToLocId': '650e1069-8f50-4453-a6d5-e6f89e9ee27a'.lower()}]})
    # print(Mongo().ResultisNotNone(doc2))
    # print(Mongo().ResultisNotNone(doc3))














