import ast
import json
from common.configDb import MSSQL as ms
from testFile.readSql import get_sql
from testFile import readExcel
import paramunittest
from testFile import readConfig
from common.configHttp import RunMain
import yaml
import ast
import os
from testFile import getpathInfo
from testFile.readyaml import readyaml
from common.configDb import MSSQL as ms, Mongo as mg
import os
import yaml
"""
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'receiptOrder')


@paramunittest.parametrized(*casexls)
def setParameters(self, case_name, method, path, query):
    self.case_name = str(case_name)
    self.path = str(path)
    self.query = ast.literal_eval(str(query))
    self.method = str(method)
    # query['ownerId'] = str(ms().get_one(ms().ExecQuery(get_sql('WMS.Orgnization', 'ownerId'))))  # 将'ownerId'参数值修改为从数据库查询到的最新ownerId
    # query['supplierId'] = str(ms().get_one(ms().ExecQuery(get_sql('WMS.Orgnization', 'supplierId'))))  # 将'supplierId'参数值修改为从数据库查询到的最新supplierId
    # query['billTypeId'] = str(ms().get_one(ms().ExecQuery(get_sql('WMS.BillType', 'billTypeId'))))  # 将'supplierId'参数值修改为从数据库查询到的最新supplierId
    print(self.query)   


if __name__ == '__main__':
    setParameters()    """



"""def main():
    query ='{"ownerId": "03db4215-0730-45ac-bde2-ffff000072fd","supplierId": "b8d6649b-6da1-4203-947c-ffff00007302","billTypeId": "84f91f9d-9213-895e-ffad-fa395b69df8a","xStatus": "OPEN","shelvesStatus": "UNPUTAWAY","expectedPkgQuantity": 0,"receivedPkgQuantity": 0,"movedPkgQuantity": 0,"receiptOrderItem": [ ]}'

    query = ast.literal_eval(str(query))
    query['ownerId'] = str(ms().get_one(ms().ExecQuery(get_sql('WMS.Orgnization', 'ownerId'))))
    print(query)


if __name__ == '__main__':
    main()   """
"""
path = getpathInfo.get_Path()

def login_token():

    headers = ast.literal_eval(readConfig.ReadConfig().get_http('headers'))
    info = RunMain().run_main(
        'post',
        headers=headers,
        url='http://localhost:44388/api/app/oauth/login',
        data='{"userName":"admin","password":"900150983cd24fb0d6963f7d28e17f72"}')
    token = 'Bearer ' + info['response']['token']
    print(info)
    print(token)
    return token

def write_token(toke_value):
    """
"""
    把获取到的token写入到yaml文件中
    :return: 
    
    ypath = os.path.join(path, 'testFile', 'token.yaml')
    t = {'token': toke_value}
    # 写入到yaml文件
    with open(ypath, 'w', encoding='utf-8') as f:
        yaml.dump(t, f, allow_unicode=True)

def checkResult():
    print(getheader())
    new_url = 'http://localhost' + ':44349' + '/api/app/createManager/receiptOrder'
    # data1 = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(new_url).query))
    info = RunMain().run_main('post', headers=getheader(), url=new_url, data='{"ownerId": "57AF8A28-36EE-428B-B108-E6F958FC4EFF", "supplierId": "57AF8A28-36EE-428B-B108-E6F958FC4EFF", "billTypeId": "84F91F9D-9213-895E-FFAD-FA395B69DF8A", "xStatus": "OPEN", "shelvesStatus": "UNPUTAWAY", "expectedPkgQuantity": 0, "receivedPkgQuantity": 0, "movedPkgQuantity": 0, "receiptOrderItem": [ ]}')
    print(info)
    return info


if __name__ == '__main__':
    token = login_token()
    write_token(token)
    checkResult()
    http://127.0.0.1:
    """
"""
def main():
    query ='{"receiptOrderItem":{"receiptOrderId":"ef1b78a0-18cd-43bd-9faf-ffff00eaa2ea","materialId":"435ef367-6707-4d80-9b43-ffff00eaa1d5","packageUnitId":"c27a7157-2c82-4111-8995-ffff00eaa383","expectedPkgQuantity":"20","receivedPkgQuantity":0,"movedPkgQuantity":0,"rowNo":1,"qCStatus":"NOQUALITY","receiptOrder":{"ownerId":"57af8a28-36ee-428b-b108-e6f958fc4eff","supplierId":"57af8a28-36ee-428b-b108-e6f958fc4eff","xCode":"RO202112060003","billTypeId":"84f91f9d-9213-895e-ffad-fa395b69df8a","xStatus":"OPEN","shelvesStatus":"UNPUTAWAY","expectedPkgQuantity":0,"receivedPkgQuantity":0,"movedPkgQuantity":0,"operateStatus":"CREATED","isOffLine":"false","receiptOrderItem":[],"creator":"admin","lastModifier":"admin","id":"ef1b78a0-18cd-43bd-9faf-ffff00eaa2ea","lastModificationTime":"2021-12-06T16:49:27.427","lastModifierId":"56a5fae8-b1ae-46e3-9346-1589908ce339","creationTime":"2021-12-06T16:49:27.427","creatorId":"56a5fae8-b1ae-46e3-9346-1589908ce339","initRowIndex":0},"material":{"xCode":"A-03-03@|@A-03-03-03","xName":"测试空调","isForbidden":"N","forbiddenUserId":"00000000-0000-0000-0000-000000000000","spec":"测试型号","smallestUnit":"PCS","materialCategoryId":"5a8a4c82-8b77-0a2e-84a8-fa0e880e7341","materialPropertyRuleId":"f394e3ce-0f1a-4bc6-a8a1-ffff00eaa10c","allocatRelationId":"443fda25-eb88-0217-1244-083af9b98ce6","shipmentRuleId":"d1781cb8-3339-6554-0956-083b1b52ff3f","materialCategory":{"xCode":"default","xName":"default","materialPropertyRuleId":"e43a47ea-b186-b6cc-2af2-0ababeb0dc53","isForbidden":"Y","creator":"管理员","id":"5a8a4c82-8b77-0a2e-84a8-fa0e880e7341","lastModificationTime":"2020-05-28T17:35:45.26","creationTime":"2020-07-10T10:04:26.247","creatorId":"56a5fae8-b1ae-46e3-9346-1589908ce339"},"materialPropertyRule":{"xCode":"Test","xName":"测试属性","productionTime":2,"receivedTime":2,"inboundTime":2,"expiredTime":2,"aStartTime":2,"qcStartTime":2,"preservationDays":2,"sourceOrderCode":2,"batchNo":2,"supplierId":2,"m_Str1":2,"m_Str2":0,"m_Str3":0,"m_Str4":0,"m_Str5":0,"m_Str6":0,"m_Str7":0,"m_Str8":0,"m_Str9":0,"m_Str10":0,"m_Str11":0,"m_Str12":0,"m_Str13":0,"m_Str14":0,"m_Str15":0,"m_Str16":0,"m_Str17":0,"m_Str18":0,"m_Str19":0,"m_Str20":0,"m_Str21":0,"m_Str22":0,"m_Str23":0,"m_Str24":0,"m_Str25":0,"m_Str26":0,"m_Str27":0,"m_Str28":0,"m_Str29":0,"m_Str30":0,"m_Str31":0,"m_Str32":0,"m_Str33":0,"m_Str34":0,"m_Str35":0,"m_Str36":0,"m_Str37":0,"m_Str38":0,"m_Str39":0,"m_Str40":0,"productionTime_Display":"false","receivedTime_Display":"false","inboundTime_Display":"false","expiredTime_Display":"false","aStartTime_Display":"false","qcStartTime_Display":"false","preservationDays_Display":"false","sourceOrderCode_Display":"false","batchNo_Display":"false","m_Str1_Display":"false","m_Str2_Display":"false","m_Str3_Display":"false","m_Str4_Display":"false","m_Str5_Display":"false","m_Str6_Display":"false","m_Str7_Display":"false","m_Str8_Display":"false","m_Str9_Display":"false","m_Str10_Display":"false","m_Str11_Display":"false","m_Str12_Display":"false","m_Str13_Display":"false","m_Str14_Display":"false","m_Str15_Display":"false","m_Str16_Display":"false","m_Str17_Display":"false","m_Str18_Display":"false","m_Str19_Display":"false","m_Str20_Display":"false","m_Str21_Display":"false","m_Str22_Display":"false","m_Str23_Display":"false","m_Str24_Display":"false","m_Str25_Display":"false","m_Str26_Display":"false","m_Str27_Display":"false","m_Str28_Display":"false","m_Str29_Display":"false","m_Str30_Display":"false","m_Str31_Display":"false","m_Str32_Display":"false","m_Str33_Display":"false","m_Str34_Display":"false","m_Str35_Display":"false","m_Str36_Display":"false","m_Str37_Display":"false","m_Str38_Display":"false","m_Str39_Display":"false","m_Str40_Display":"false","productionTime_MustFill":"true","receivedTime_MustFill":"true","inboundTime_MustFill":"true","expiredTime_MustFill":"true","aStartTime_MustFill":"true","qcStartTime_MustFill":"true","preservationDays_MustFill":"true","sourceOrderCode_MustFill":"true","batchNo_MustFill":"true","m_Str1_MustFill":"true","m_Str2_MustFill":"false","m_Str3_MustFill":"false","m_Str4_MustFill":"false","m_Str5_MustFill":"false","m_Str6_MustFill":"false","m_Str7_MustFill":"false","m_Str8_MustFill":"false","m_Str9_MustFill":"false","m_Str10_MustFill":"false","m_Str11_MustFill":"false","m_Str12_MustFill":"false","m_Str13_MustFill":"false","m_Str14_MustFill":"false","m_Str15_MustFill":"false","m_Str16_MustFill":"false","m_Str17_MustFill":"false","m_Str18_MustFill":"false","m_Str19_MustFill":"false","m_Str20_MustFill":"false","m_Str21_MustFill":"false","m_Str22_MustFill":"false","m_Str23_MustFill":"false","m_Str24_MustFill":"false","m_Str25_MustFill":"false","m_Str26_MustFill":"false","m_Str27_MustFill":"false","m_Str28_MustFill":"false","m_Str29_MustFill":"false","m_Str30_MustFill":"false","m_Str31_MustFill":"false","m_Str32_MustFill":"false","m_Str33_MustFill":"false","m_Str34_MustFill":"false","m_Str35_MustFill":"false","m_Str36_MustFill":"false","m_Str37_MustFill":"false","m_Str38_MustFill":"false","m_Str39_MustFill":"false","m_Str40_MustFill":"false","creator":"admin","lastModifier":"admin","id":"f394e3ce-0f1a-4bc6-a8a1-ffff00eaa10c","lastModificationTime":"2021-12-06T16:46:24.403","lastModifierId":"56a5fae8-b1ae-46e3-9346-1589908ce339","creationTime":"2021-12-06T16:46:24.403","creatorId":"56a5fae8-b1ae-46e3-9346-1589908ce339"},"packageUnit":[{"materialId":"435ef367-6707-4d80-9b43-ffff00eaa1d5","rowNo":1,"unit":"PCS","pkgLevel":"台","convertFigureSmallUnit":1,"convertFigure":1,"creator":"admin","lastModifier":"admin","id":"c27a7157-2c82-4111-8995-ffff00eaa383","lastModificationTime":"2021-12-06T16:50:18.26","lastModifierId":"56a5fae8-b1ae-46e3-9346-1589908ce339","creationTime":"2021-12-06T16:50:18.26","creatorId":"56a5fae8-b1ae-46e3-9346-1589908ce339"}],"creator":"admin","lastModifier":"admin","id":"435ef367-6707-4d80-9b43-ffff00eaa1d5","lastModificationTime":"2021-12-06T16:48:50.91","lastModifierId":"56a5fae8-b1ae-46e3-9346-1589908ce339","creationTime":"2021-12-06T16:47:41.84","creatorId":"56a5fae8-b1ae-46e3-9346-1589908ce339"},"packageUnit":{"materialId":"435ef367-6707-4d80-9b43-ffff00eaa1d5","rowNo":1,"unit":"PCS","pkgLevel":"台","convertFigureSmallUnit":1,"convertFigure":1,"creator":"admin","lastModifier":"admin","id":"c27a7157-2c82-4111-8995-ffff00eaa383","lastModificationTime":"2021-12-06T16:50:18.26","lastModifierId":"56a5fae8-b1ae-46e3-9346-1589908ce339","creationTime":"2021-12-06T16:50:18.26","creatorId":"56a5fae8-b1ae-46e3-9346-1589908ce339"}},"materialProperty":{"propertyRuleId":"f394e3ce-0f1a-4bc6-a8a1-ffff00eaa10c","materialId":"435ef367-6707-4d80-9b43-ffff00eaa1d5","xType":"RECEIVE","productionTime":"2021-12-01","receivedTime":"2021-12-06","inboundTime":"2021-12-06","expiredTime":"2021-12-31","qcStartTime":"2021-12-06","preservationDays":"15","sourceOrderCode":"RO202112060003","batchNo":"202112061651","supplierId":"57af8a28-36ee-428b-b108-e6f958fc4eff","m_Str1":"属性1","m_Str2":"属性2","m_Str3":"属性3","m_Str4":"属性4","m_Str5":"属性5","m_Str6":"属性6","m_Str7":"属性7","m_Str8":"属性8","m_Str9":"属性9","m_Str10":"属性10",}}'
    query = eval(query)
    query['receiptOrderItem']['receiptOrderId'] = str(ms().getvalue('WMS.ReceiptOrder', 'receiptOrderItem')[0])
    print(query)

if __name__ =='__main__':
    main()
"""

def main():
    """
    yamlfile = os.path.join('E:\PycharmProjects\WMSjktest1\\testFile', 'ShipConfig.yaml')
    f = open(yamlfile, 'r', encoding='utf-8')
    a = f.read()
    content = yaml.load(a, Loader=yaml.FullLoader)
    print(content) """

    """
    a = [1,2,3,4,5,6,7]
    b = [20,21,22]
    i = 0
    while len(b)<len(a):
        b.append(b[i])
        i = i+1

    print(b) """

sqltext1 = """
    SELECT b.id ShipOrderItemId,c.MaterialId,d.BatchNo,d.M_Str1,d.M_Str2,d.M_Str3,
    d.M_Str4,d.M_Str5,d.M_Str6,d.M_Str7,d.M_Str8,d.M_Str9,d.M_Str10
    FROM WMS.ShipOrder a 
    INNER JOIN WMS.ShipOrderItem b ON a.Id=b.ShipOrderId
    INNER JOIN WMS.materialProperty c ON b.MaterialPropertyId =c.Id
    INNER JOIN WMS.materialPropertyRule d ON c.PropertyRuleId=d.Id
    WHERE a.Id='49E55545-1DC3-4F67-8593-FFFF00FC65AF'
            """
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
addBatchNoquerylist = []
addM_Str1querylist = []
addM_Str2querylist = []
addM_Str3querylist = []
addM_Str4querylist = []
addM_Str5querylist = []
addM_Str6querylist = []
addM_Str7querylist = []
addM_Str8querylist = []
addM_Str9querylist = []
addM_Str10querylist = []
addquerydict = {}
for i in range(len(cur1)):  # 根据cur1查询出的涉及发货明细id循环获取该发货单每条发货明细的扩展信息情况及对应是否有相应库存
    def isaddquery(r):  # 根据查询结果确定是否必填，如果必填，需要在后续的查询语句中加入查询条件
        if r == 2:  # 根据查询结果，每行第二个是BatchNo字段
            if cur1[i][r] == 2:  # 等于2表示必填
                query1 = 'AND s.BatchNo=t.BatchNo'
                query2 = ",{'WmsTask.MaterialProperty.BatchNo': self.BatchNolist[p]}"
                addquerydict[str(cur1[i][0])] = {'BatchNo': [query1, query2]}
            else:
                addquerydict[str(cur1[i][0])] = {'BatchNo': ['', '']}
        else:  # 根据查询结果，每行第三个到最后一个分别是M_Str1、M_Str2...字段
            if cur1[i][r] == 2:  # 等于2表示必填
                query1 = 'AND isnull(s.M_Str%d,'')=isnull(t.M_Str%d,'')' % (r-2, r-2)
                query2 = ",{'WmsTask.MaterialProperty.M_Str%d': self.M_Str%dlist[p]}" % (r-2, r-2)
                addquerydict[str(cur1[i][0])] = {'M_Str%d' % (r-2): [query1, query2]}
            else:
                addquerydict[str(cur1[i][0])] = {'M_Str%d' % (r-2): ['', '']}

        return addquerydict  # 获取到以ShipOrderItemId为key，各扩展属性为value的类似二维数组
        print(addquerydict)

        # # 用于判断扩展属性是否必填确定是否将查询条件假如对应sql或mobgodb查询语句
        # if cur1[i][2] == 2:  # 如果BatchNo字段等于2（2表示必填）
        #     query1 = 'AND s.BatchNo=t.BatchNo'
        #     query2 = ",{'WmsTask.MaterialProperty.BatchNo': self.BatchNolist[p]}"
        #     self.addquerydict[cur1[i][0]]['BatchNo'] = [query1,query2]
        # elif cur1[i][3] == 2:  # 如果M_Str1字段等于2（2表示必填）
        #     query1 = 'AND isnull(s.M_Str1,'')=isnull(t.M_Str1,'')'
        #     query2 = ",{'WmsTask.MaterialProperty.M_Str1': self.M_Str1list[p]}"
        #     self.addquerydict[cur1[i][0]]['M_Str1'] = [query1, query2]
        # elif cur1[i][4] == 2:  # 如果M_Str2字段等于2（2表示必填）
        #     query1 = 'AND isnull(s.M_Str2,'')=isnull(t.M_Str2,'')'
        #     query2 = ",{'WmsTask.MaterialProperty.M_Str2': self.M_Str2list[p]}"
        #     self.addquerydict[cur1[i][0]]['M_Str2'] = [query1, query2]
        # elif cur1[i][5] == 2:  # 如果M_Str3字段等于2（2表示必填）
        #     query1 = 'AND isnull(s.M_Str3,'')=isnull(t.M_Str3,'')'
        #     query2 = ",{'WmsTask.MaterialProperty.M_Str3': self.M_Str3list[p]}"
        #     self.addquerydict[cur1[i][0]]['M_Str3'] = [query1, query2]
        # elif cur1[i][6] == 2:  # 如果M_Str4字段等于2（2表示必填）
        #     query1 = 'AND isnull(s.M_Str4,'')=isnull(t.M_Str4,'')'
        #     query2 = ",{'WmsTask.MaterialProperty.M_Str4': self.M_Str4list[p]}"
        #     self.addquerydict[cur1[i][0]]['M_Str4'] = [query1, query2]
        # elif cur1[i][7] == 2:
        #     query1 = 'AND isnull(s.M_Str5,'')=isnull(t.M_Str5,'')'
        #     query2 = ",{'WmsTask.MaterialProperty.M_Str5': self.M_Str5list[p]}"
        #     self.addquerydict[cur1[i][0]]['M_Str5'] = [query1, query2]
        # elif cur1[i][8] == 2:
        #     query1 = 'AND isnull(s.M_Str6,'')=isnull(t.M_Str6,'')'
        #     query2 = ",{'WmsTask.MaterialProperty.M_Str6': self.M_Str6list[p]}"
        #     self.addquerydict[cur1[i][0]]['M_Str6'] = [query1, query2]
        # elif cur1[i][9] == 2:
        #     query1 = 'AND isnull(s.M_Str7,'')=isnull(t.M_Str7,'')'
        #     query2 = ",{'WmsTask.MaterialProperty.M_Str7': self.M_Str7list[p]}"
        #     self.addquerydict[cur1[i][0]]['M_Str7'] = [query1, query2]
        # elif cur1[i][10] == 2:
        #     query1 = 'AND isnull(s.M_Str8,'')=isnull(t.M_Str8,'')'
        #     query2 = ",{'WmsTask.MaterialProperty.M_Str8': self.M_Str8list[p]}"
        #     self.addquerydict[cur1[i][0]]['M_Str8'] = [query1, query2]
        # elif cur1[i][11] == 2:
        #     query1 = 'AND isnull(s.M_Str9,'')=isnull(t.M_Str9,'')'
        #     query2 = ",{'WmsTask.MaterialProperty.M_Str9': self.M_Str9list[p]}"
        #     self.addquerydict[cur1[i][0]]['M_Str9'] = [query1, query2]
        # elif cur1[i][12] == 2:
        #     query1 = 'AND isnull(s.M_Str10,'')=isnull(t.M_Str10,'')'
        #     query2 = ",{'WmsTask.MaterialProperty.M_Str10': self.M_Str10list[p]}"
        #     self.addquerydict[cur1[i][0]]['M_Str10'] = [query1, query2]
        # else:
        #     query1 = ''
        #     query2 = ''
        #     self.addquerydict[cur1[i][0]] = [query1, query2]


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
        (SELECT a.id ShipOrderId, c.MaterialId,c.BatchNo,c.M_Str1,c.M_Str2,c.M_Str3,c.M_Str4,c.M_Str5,c.M_Str6,
        c.M_Str7,c.M_Str8,c.M_Str9,c.M_Str10,a.XCode ShipOrderCode,d.Xcode
        FROM WMS.ShipOrder a 
        INNER JOIN WMS.ShipOrderItem b ON a.Id=b.ShipOrderId
        INNER JOIN WMS.materialProperty c ON b.MaterialPropertyId =c.Id
        INNER JOIN WMS.Dock d ON a.DockId =d.Id
        WHERE b.id='{0}'
        )t --查询出某个发货单的某个发货明细的物料编码及扩展属性
        ON --根据 WMS.materialPropertyRule表中规定的扩展属性是否必填确定是否需要加入BatchNo、M_Str1等其他对比条件
        s.MaterialId =t.MaterialId 
                """.format(str(cur1[i][0])) + isaddquery(2)[str(cur1[i][0])]['BatchNo'][0] + isaddquery(3)[str(cur1[i][0])]['M_Str1'][0] + isaddquery(4)[str(cur1[i][0])]['M_Str2'][0] + isaddquery(5)[str(cur1[i][0])]['M_Str3'][0] + isaddquery(6)[str(cur1[i][0])]['M_Str4'][0] + isaddquery(7)[str(cur1[i][0])]['M_Str5'][0] + isaddquery(8)[str(cur1[i][0])]['M_Str6'][0] + isaddquery(9)[str(cur1[i][0])]['M_Str7'][0] + isaddquery(10)[str(cur1[i][0])]['M_Str8'][0] + isaddquery(11)[str(cur1[i][0])]['M_Str9'][0] + isaddquery(12)[str(cur1[i][0])]['M_Str10'][0]

    print(sqltext2)
    cur2 = ms().get_all(ms().ExecQuery(sqltext2))
    if cur2 == [(None,)]:
        cur2 = []
    a = len(cur2) + a  # 若循环完，len(cur2)都为0，则代表所有物料都没有查到对应库存
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
    Docklist.append(cur2[0][13])
    if len(cur2) > 0:  # 如果查询有结果返回，将判断扩展属性是否必填得到的mongodb查询条件字符串加到列表中，以备后续mongodb查询使用
        addBatchNoquerylist.append(addquerydict[str(cur1[i][0])]['BatchNo'][1])
        addM_Str1querylist.append(addquerydict[str(cur1[i][0])]['M_Str1'][1])
        addM_Str2querylist.append(addquerydict[str(cur1[i][0])]['M_Str2'][1])
        addM_Str3querylist.append(addquerydict[str(cur1[i][0])]['M_Str3'][1])
        addM_Str4querylist.append(addquerydict[str(cur1[i][0])]['M_Str4'][1])
        addM_Str5querylist.append(addquerydict[str(cur1[i][0])]['M_Str5'][1])
        addM_Str6querylist.append(addquerydict[str(cur1[i][0])]['M_Str6'][1])
        addM_Str7querylist.append(addquerydict[str(cur1[i][0])]['M_Str7'][1])
        addM_Str8querylist.append(addquerydict[str(cur1[i][0])]['M_Str8'][1])
        addM_Str9querylist.append(addquerydict[str(cur1[i][0])]['M_Str9'][1])
        addM_Str10querylist.append(addquerydict[str(cur1[i][0])]['M_Str10'][1])
print(MaterialIdlist)
print(BatchNolist)
print(M_Str1list)
print(addBatchNoquerylist)
print(addM_Str1querylist)
info = RunMain().run_main(post, headers=self.headers, url=new_url)

if __name__ =='__main__':
    main()