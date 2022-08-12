import os
import configparser
from testFile import getpathInfo

path = getpathInfo.get_Path() # 调用实例化
config_path = os.path.join(path, 'testFile', 'config.ini')
config = configparser.ConfigParser()  # 调用外部的读取配置文件的办法
config.read(config_path, encoding='utf-8')


class ReadConfig():
    def get_http(self, name):
        value = config.get('HTTP', name)
        return value

    def get_email(self, name):
        value = config.get('EMAIL', name)
        return value

    def get_db(self, name):
        value = config.get('DATABASE', name)
        return value

    def get_mongodb(self, name):
        value = config.get('MONGODB', name)
        return value

    def get_redis(self, name):
        value = config.get('Redis', name)
        return value

    def get_Property(self, name):
        value = config.get('materialProperty', name)
        return value

    def isaddquery(self, name):  # 根据从confiig.ini中获取的扩展属性是否加入物料唯一性判断设置，确定是否加入查询文本
        if name == 'BatchNo':
            if ReadConfig().get_Property(name) == '1':
                query1 = 'AND s.BatchNo=t.BatchNo'
                query2 = ",{'WmsTask.MaterialProperty.BatchNo': self.BatchNolist[p]}"
                return [query1, query2]
            else:
                return ['', '']
        else:
            if ReadConfig().get_Property(name) == '1':
                query1 = 'AND s.{0}=t.{0}'.format(name)
                query2 = ",{'WmsTask.MaterialProperty.%s': self.%slist[p]}" % (name, name)
                return [query1, query2]
            else:
                return ['', '']


if __name__ == '__main__':
    print('HTTP中的baseurl值为：', ReadConfig().get_http('baseurl'))
    print(ReadConfig().get_Property('BatchNo'))
    print(ReadConfig().isaddquery('M_Str1'))

