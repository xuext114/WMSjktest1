import os
import yaml
import ast
from testFile import getpathInfo
from testFile.readConfig import ReadConfig as readConfig

path = getpathInfo.get_Path()

class readyaml():

    def readyaml(self, yamlfile):
        """
        读取yaml文件
        :param yamlfile:
        :return:
        """
        p = os.path.join(path, 'testFile', yamlfile)
        f = open(p, encoding='utf-8')
        a = f.read()
        t = yaml.load(a, Loader=yaml.FullLoader)
        f.close()
        return t

    def get_headerIncloudToken(self, yamlname='token.yaml'):
        """
        从token.yaml读取token值
        :param yamlName: 配置文件名称
        :return:
        """
        t = self.readyaml(yamlname)
        headers = ast.literal_eval(readConfig().get_http('headers'))
        headers['Authorization'] = t['token']
        headerIncloudToken = headers
        return headerIncloudToken

    """
    def new_header(self):
        用于将headers中的'Content-Type'值改为0，用于部分请求体为空的接口
        :return:

        headerIncloudToken1 = self.get_headerIncloudToken()
        headerIncloudToken1['Content-Length'] = '0'
        return headerIncloudToken1 """

if __name__ =='__main__':
    print(readyaml().readyaml('ShipConfig.yaml')['request']['入口到外形检测'])

