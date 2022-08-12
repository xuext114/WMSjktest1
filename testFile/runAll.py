#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import common.HTMLTestRunner as HTMLTestRunner
from testFile import getpathInfo
import unittest
from testFile import readConfig
from common.configHttp import RunMain
import yaml
import ast
from common.configEmail import SendEmail
from apscheduler.schedulers.blocking import BlockingScheduler
import pythoncom


send_mail = SendEmail(
        username='xxt114@126.com',
        passwd='QLNBMSJSUBIGFGNT',
        recv=['xuexiaoting@gen-song.net'],
        title='接口自动化测试报告',
        content='测试发送邮件',
        file=r'E:\PycharmProjects\WMSjktest2\result\report.html',
        ssl=True
    )
path = getpathInfo.get_Path()
report_path = os.path.join(path, 'result')
on_off = readConfig.ReadConfig().get_email('on_off')

class AllTest:  # 定义一个类AllTest
    def __init__(self):  # 初始化一些参数和数据
        global resultPath
        resultPath = os.path.join(report_path, 'report.html')
        self.caseListFile = os.path.join(path, 'testFile', 'caselist.txt')  # 配置执行哪些测试文件的配置文件路径
        self.caseFile = os.path.join(path, 'testCase')  # 真正的测试断言文件路径
        self.caseList = []

    def login_token(self):
        """
        通过登录获取token
        :return:
        """
        headers = ast.literal_eval(readConfig.ReadConfig().get_http('headers'))
        info = RunMain().run_main(
            'post',
            headers=headers,
            url='http://localhost:44388/api/app/oauth/login',
            data='{"userName":"admin","password":"900150983cd24fb0d6963f7d28e17f72"}')
        token = 'Bearer ' + info['response']['token']
        return token

    def write_token(self, toke_value):
        """
        把获取到的token写入到yaml文件中
        :return:
        """
        ypath = os.path.join(path, 'testFile', 'token.yaml')
        t = {'token': toke_value}
        # 写入到yaml文件
        with open(ypath, 'w', encoding='utf-8') as f:
            yaml.dump(t, f, allow_unicode=True)

    def set_case_list(self):
        """
        读取caselist.txt文件中的用例名称，并添加到caseList元素组
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith('#'):  # 如果data非空且不以#开头
                self.caseList.append(data.replace('\n', ''))  # 添加符合条件的每行数据，且去掉换行符
        fb.close()

    def set_case_suite(self):
        self.set_case_list()  # 通过set_case_list()拿到caselist元素组
        print(self.caseList)
        test_suite = unittest.TestSuite()
        suite_moudle = []
        for case in self.caseList:  # 从caseList元素组中循环取出case
            case_name = case.split('/')[-1]  # 通过split函数来讲aaa/bbb分割字符串
            print(case_name+'.py')  # 打印取出来的名称
            # 批量加在用例，第一个参数为用例存放路径，第二个参数为路径文件名
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name+'.py', top_level_dir=None)
            suite_moudle.append(discover)  # 将discover存入suite_moudle元素组
            print('suite_moudle:'+str(suite_moudle))
        if len(suite_moudle) > 0:  # 判断suite_moudle元素组是否存在元素
            for suite in suite_moudle:  # 如果存在，循环取出元素组内容，命名为suite
                for test_name in suite:  # 从discover中取出test_name, 使用addTest添加到测试集
                    print(test_name)
                    test_suite.addTest(test_name)
        else:
            print('else:')
            return None
        return test_suite

    def run(self):
        try:
            suit = self.set_case_suite()  # 调用set_case_suite()获取test_suite
            print('try')
            print(str(suit))
            if suit is not None:  # 判断test_suite是否为空
                print('if-suit')
                fp = open(resultPath, 'wb')  # 打开result测试报告文件，如果不存在就创建
                # 调用HTMLTestRunner
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                runner.run(suit)
            else:
                print('Have no case to test.')
        except Exception as ex:
            print(str(ex))
            # log.info(str(ex))

        finally:
            print('***************TEST END***************')
            fp.close()
        # 判断邮件发送的开关
        if on_off == 'on':
            send_mail.send_email()
        else:
            print('邮件发送开关配置关闭，打开开关后可正常自动发送测试报告')


if __name__ == '__main__':
    token = AllTest().login_token()
    AllTest().write_token(str(token))
    AllTest().run()