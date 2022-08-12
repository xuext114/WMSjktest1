#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
所有正在执行的外形检测异常回退及上架任务确认完成
"""

import ast
import unittest
from common.configHttp import RunMain
import paramunittest
from testFile import geturlParams
# import urllib.parse
from testFile import readExcel
from testFile.readyaml import readyaml
from common.configDb import MSSQL as ms, Mongo as mg
from copy import copy
import random
import json
import time


url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'completeTask')


@paramunittest.parametrized(*casexls)
class testcompleteTask(unittest.TestCase):

    def isNone(self, value):
        """
        判断某个值是否为None，如果为None，返回空字符，如果不为None，返回本身
        :param value:
        :return:
        """
        if value is None:
            return ''
        else:
            return value

    def setParameters(self, case_name, method, path, query):
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = ast.literal_eval(str(query))
        self.method = str(method)
        self.headers = readyaml().get_headerIncloudToken()

        """**************获取需要作为确认‘外形检测异常回退’任务接口的参数列表********************"""
        # 从mongodb的TaskBase集合查询正在执行的‘外形检测异常回退’任务
        doc1 = mg().MongoExecquery('GSMiddleWare', 'TaskBase').find({'TaskType': '外形检测异常回退'})
        self.TaskCodelist1 = []  # 从mongodb查询结果中获取'外形检测异常回退'任务的code列表
        self.Fromlist1 = []  # 从mongodb查询结果中获取'外形检测异常回退'任务的起始点列表
        self.Tolist1 = []  # 从mongodb查询结果中获取'外形检测异常回退'任务的目标点列表
        self.Palletslist1 = []  # 从mongodb查询结果中获取'外形检测异常回退'任务的托盘列表
        for Taskdoc in doc1:  # 根据在mongodb中查询到的正在执行的’外形检测异常回退‘的任务循环
            self.TaskCodelist1.append(str(Taskdoc["TaskCode"]))
            self.Fromlist1.append(str(Taskdoc["FromLocationCode"]))
            self.Tolist1.append(str(Taskdoc["ToLocationCode"]))
            self.Palletslist1.append(Taskdoc["Pallets"])

        """**************获取需要作为确认‘上架（MV_PUTAWAY）’任务接口的参数列表********************"""
        # 从mongodb的TaskBase集合查询正在执行的‘外形检测异常回退’任务
        doc2 = mg().MongoExecquery('GSMiddleWare', 'MiddlewareTask').find({'TaskType': 'MV_PUTAWAY'})
        self.TaskCodelist2 = []  # 从mongodb查询结果中获取'外形检测异常回退'任务的code列表
        self.Fromlist2 = []  # 从mongodb查询结果中获取'外形检测异常回退'任务的起始点列表
        self.Tolist2 = []  # 从mongodb查询结果中获取'外形检测异常回退'任务的目标点列表
        self.Palletslist2 = []  # 从mongodb查询结果中获取'外形检测异常回退'任务的托盘列表
        for Taskdoc in doc2:  # 根据在mongodb中查询到的正在执行的’外形检测异常回退‘的任务循环
            self.TaskCodelist2.append(str(Taskdoc["TaskCode"]))
            self.Fromlist2.append(str(Taskdoc["FromLocCode"]))
            self.Tolist2.append(str(Taskdoc["ToLocCode"]))
            self.Palletslist2.append(Taskdoc["Pallet"])

    def description(self):
        print(self.case_name)

    def sttUp(self):
        print(self.case_name + '测试开始前准备')

    def testcompleteTask(self):
        self.checkResult()

    def tearDown(self):
        print('测试结束，输出log完结\n\n')
        ms().closeDB()  # 关闭数据库连接

    def checkResult(self):
        new_url = url + ':9877' + self.path
        if self.case_name == 'cfm_CheckStationReturn':
            print(self.case_name)
            querylist1 = []
            for m in range(len(self.TaskCodelist1)):  # 获取由正在运行的‘外形检测异常回退’任务数据组建的请求体
                self.query['taskCode'] = str(self.TaskCodelist1[m])
                self.query['from'] = str(self.Fromlist1[m])
                self.query['to'] = str(self.Tolist1[m])
                self.query['containerCodes'] = [str(self.Palletslist1[m])]
                newquery = str(copy(self.query))  # .encode('utf-8')
                querylist1.append(newquery)
            print('异常回退任务请求体列表：', querylist1)

            for j in range(len(querylist1)):  # 根据querylist1长度决定请求几次
                print('本次’外形检测异常回退‘任务数据：', querylist1[j])
                try:
                    info = RunMain().run_main(self.method, headers=self.headers, url=new_url,
                                              data=json.dumps(eval(querylist1[j])))
                    print("外形检测异常回退任务确认完成，返回：", info)
                except Exception as e:
                    print('接口调用异常：', e)
                else:
                    # 在mongodb的ArchivedTaskBase集合中查找是否有该任务id完成的信息，如果有，表示任务完成成功
                    newdoc1 = mg().MongoExecquery('GSMiddleWare', 'ArchivedTaskBase').find({"$and": [
                        {'TaskCode': self.TaskCodelist1[j]}, {'TaskType': '外形检测异常回退'}, {'CompleteStatus': 0}]})
                    self.assertTrue(mg().ResultisNotNone(newdoc1), '调用确认‘外形检测异常回退’任务后，在mongodb已完成任务中未找到该任务数据')

                print('有确认任务较多时，确认失败的问题，每次确认后等待1秒试试.....')
                time.sleep(1)

        elif self.case_name == 'cfm_Putaway':
            print(self.case_name)
            querylist2 = []
            for n in range(len(self.TaskCodelist2)):  # 获取由正在运行的上架（MV_PUTAWAY）任务信息组件的请求体
                self.query['taskCode'] = str(self.TaskCodelist2[n])
                self.query['from'] = str(self.Fromlist2[n])
                self.query['to'] = str(self.Tolist2[n])
                self.query['containerCodes'] = [str(self.Palletslist2[n])]
                newquery = str(copy(self.query))  # .encode('utf-8')
                querylist2.append(newquery)
            print('上架任务请求体列表：', querylist2)
            for k in range(len(querylist2)):  # 根据querylist2长度决定请求几次
                print('本次上架任务数据：', querylist2[k])

                try:
                    info = RunMain().run_main(self.method, headers=self.headers, url=new_url,
                                              data=json.dumps(eval(querylist2[k])))
                    print('上架任务确认完成，返回：', info)
                except Exception as e:
                    print('接口调用异常：', e)
                else:
                    # 在mongodb的ArchivedMiddlewareTask集合中查找是否有该任务id完成的信息，如果有，表示任务完成成功
                    newdoc2 = mg().MongoExecquery('GSMiddleWare', 'ArchivedMiddlewareTask').find({"$and": [
                        {'TaskCode': self.TaskCodelist2[k]},
                        {'TaskType': 'MV_PUTAWAY'},
                        {'TaskStatus': 'FINISHED'}]})
                    self.assertTrue(mg().ResultisNotNone(newdoc2), '调用确认上架任务后，在mongodb已完成任务中未找到该任务数据')

                print('有确认任务较多时，确认失败的问题，每次确认后等待1秒试试.....')
                time.sleep(1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
