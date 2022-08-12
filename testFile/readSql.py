import os
from xml.etree import ElementTree as ElementTree
from testFile.getpathInfo import get_Path
from testFile.readConfig import ReadConfig as readconfig


# 从xml文件中读取sql语句
database = {}
pirdor = get_Path()
def set_xml():
    if len(database) == 0:
        sql_path = os.path.join(pirdor, 'testFile', 'sql.xml')
        tree = ElementTree.parse(sql_path)
        for db in tree.findall('database'):
            db_name = db.get('name')
            table = {}
            for tb in list(db):
                table_name = tb.get('name')
                sql = {}
                for data in list(tb):
                    sql_id = data.get('id')
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table
    return database


def get_xml_dict(table_name):
    database_name = readconfig().get_db('database')  # xml文件的database_name要与confiig.ini文件中database一致
    set_xml()
    if database[database_name][table_name] is None:
        raise Exception('没有对应查询表！')
    else:
        database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(table_name, sql_id):
    db = get_xml_dict(table_name)
    if db[sql_id] is None:
        raise Exception('没有对应查询sql！')
    else:
        sql = db.get(sql_id)
    return sql


if __name__ == '__main__':
    # print(set_xml())
    print(get_sql('WMS.ReceiptOrder', 'receiptOrderId'))
    # get_xml_dict('GSWMS_TEST', 'WMS.Orgnization')


