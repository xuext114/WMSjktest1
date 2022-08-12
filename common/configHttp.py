# -- coding: utf-8 --**

import requests
import json


class RunMain():
    def send_post(self, url, data, headers):  # 定义一个方法，传入需要的参数url和data
        #  参数必须按照url、data顺序传入
        result = requests.post(url=url, data=data, headers=headers)  # 因为这里要封装post方法，所以这里的url和data不能写死
        # res = json.dumps(result.text, ensure_ascii=False, sort_keys=True, indent=2)
        if result == 'true':  # 如果结果只返回一个’true‘
            return True
        else:  # 如果结果返回的不是一个’true‘
            res = json.loads(result.content.decode('utf-8'))  # 将response转换为字典
            return res
            # return result

    def send_get(self, url, data,  headers):
        result = requests.get(url=url, params=data, headers=headers)
        # res = json.dumps(result.text, ensure_ascii=False, sort_keys=True, indent=2)
        if result == 'true':  # 如果结果只返回一个’true‘
            return True
        else:  # 如果结果返回的不是一个’true‘
            res = json.loads(result.content.decode('utf-8'))  # 将response转换为字典
            return res
        # return result

    def run_main(self, method, headers=None, url=None, data=None):  # 定义一个run_main函数，通过传过来的method来进行不同的get或post请求
        result = None
        if method == 'post':
            result = self.send_post(url, data, headers)
        elif method == 'get':
            result = self.send_get(url, data, headers)
        else:
            print('method值错误！！！')
        return result


if __name__ == '__main__':
    info = RunMain().run_main('post', headers={
"Connection": "keep-alive",
"Content-Length": "1600",  # get请求时去掉
"Content-Type": "application/json;charset=UTF-8",
"Accept": "application/json, text/plain, */*",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
"sec-ch-ua-platform": "Windows",
"Sec-Fetch-Site": "same-site",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9",
"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NmE1ZmFlOC1iMWFlLTQ2ZTMtOTM0Ni0xNTg5OTA4Y2UzMzkiLCJuYW1lIjoiYWRtaW4iLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoiYWRtaW4iLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjU2YTVmYWU4LWIxYWUtNDZlMy05MzQ2LTE1ODk5MDhjZTMzOSIsImp0aSI6IjU2YTVmYWU4LWIxYWUtNDZlMy05MzQ2LTE1ODk5MDhjZTMzOSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvZXhwaXJhdGlvbiI6IjEyLzIxLzIwMjEgNTo1ODoyNyBQTSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IjYyNzZkZWQ5LWMyNWYtZDFiNy0yODliLTM5ZjVjZDkxN2I5MSIsIm5iZiI6MTY0MDA1MTkwNywiZXhwIjoxNjQwMDgwNzA3LCJpc3MiOiJHUyIsImF1ZCI6ImV2ZXJ5b25lIn0.5EdgNOH_9KJeCJULafWfkvsPQPn69co8mJY8WqJLJXE"
}, url='http://127.0.0.1:9877/WMSServiceForWcs/CompleteTask', data=json.dumps({'TaskCode': '20211220190552720', 'Requestld': '', 'TaskType': '入口到外形检测', 'From': '00-001-1014', 'To': '00-001-1014仅取放货', 'ContainerCodes': ['k0201'], 'Direction': '0', 'Additionallnfo': {'外形检测': '失败', 'priority': '0'}}))

    print(info)






