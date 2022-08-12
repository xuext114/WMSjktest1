#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import json
import unittest
from common.configHttp import RunMain
import paramunittest
from testFile import geturlParams
# import urllib.parse
from testFile import readExcel


url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'login')
headers = {
"Connection": "keep-alive",
"Content-Length": "67",
"Content-Type": "application/json;charset=UTF-8",
"Accept": "application/json, text/plain, */*",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
"sec-ch-ua-platform": "Windows",
"Sec-Fetch-Site": "same-site",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9",
"Authorization":''
}


@paramunittest.parametrized(*casexls)
class testUserLogin(unittest.TestCase):
    def setParameters(self, case_name, method, path, query):
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = str(query)
        self.method = str(method)
        print(self.query)

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testlogin(self):
        global headers
        self.checkResult()
        Authorization = self.info['response']['token']
        headers['Authorization'] = Authorization
        print('headers:' + str(headers))

    """
    def get_headers(self):
        
        self.response1 = self.checkResult().info
        self.Authorization = self.response1['response']['token']
        headers['Authorization'] = self.Authorization
        print(headers)
        return headers """


    def tearDown(self):
        print('测试结束，输出log完结\n\n')

    def checkResult(self):
        new_url = url + ':44388' + self.path
        # data1 = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(new_url).query))
        self.info = RunMain().run_main(self.method, headers=headers, url=new_url, data=self.query)
        # ss = json.loads(info)  # 将响应转换为字典格式
        if self.case_name == 'login':
            self.assertEqual(self.info['msg'], "success")


def get_headers():
    return headers


if __name__ == '__main__':
    testUserLogin(unittest.TestCase).testlogin()
    print(get_headers())












