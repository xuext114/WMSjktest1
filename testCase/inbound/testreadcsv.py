import requests
import json
from common.configHttp import RunMain, headers1
import paramunittest
from testFile import geturlParams
from testFile import readExcel

url = geturlParams.geturlParams().get_Url()
casexls = readExcel.readExcel().get_xls('userCase.xlsx', 'login')
token = ''

headers1 = {
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
"token":''
}


class RunMain():
    def send_post(self, url, data):  # 定义一个方法，传入需要的参数url和data
        #  参数必须按照url、data顺序传入
        result = requests.post(url=url, data=data, headers=headers1)  # 因为这里要封装post方法，所以这里的url和data不能写死
        # res = json.dumps(result.text, ensure_ascii=False, sort_keys=True, indent=2)
        res = json.loads(result.content.decode('utf-8'))
        return res
        # return result

    def run_main(self, method, url=None, data=None):  # 定义一个run_main函数，通过传过来的method来进行不同的get或post请求
        result = None
        if method == 'post':
            result = self.send_post(url, data)
        elif method == 'get':
            result = self.send_get(url, data)
        else:
            print('method值错误！！！')
        return result


def checkResult(method, query):
    global token
    new_url = url + ':44388' + '/api/app/oauth/login'
    # data1 = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(new_url).query))
    info = RunMain().run_main(method, url=new_url, data=query)
    # ss = json.loads(info)  # 将响应转换为字典格式
    # token = info['response']
    #if self.case_name == 'login':
     #   self.assertEqual(info['code'], 200)
    return info


if __name__ == '__main__':
    new_url = url + ':44388' + '/api/app/oauth/login'
    print(RunMain().run_main('post', new_url, casexls[0][3]))
    # print(RunMain().send_post(new_url, '{“userName”: "108847", “password”: "96e79218965eb72c92a549dd5a330112"}'.encode('utf-8')))
    # result = requests.post(url='http://127.0.0.1:44388/api/app/oauth/login',data='{"userName":"108847", "password":"96e79218965eb72c92a549dd5a330112"}', headers=headers1)
    # print(json.loads(result.content.decode('utf-8')))

    #print(checkResult('post', casexls[0][3].encode('utf-8')))
    #print(casexls[0][3])

