import os

def get_Path():
    path = os.path.dirname(os.path.dirname(__file__))
    return path

if __name__ == '__main__': # 执行该文件，测试下是否ok
    print('测试路径是否ok，路径为', get_Path())

