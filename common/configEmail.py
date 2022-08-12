import os
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SendEmail(object):
    def __init__(self, username, passwd, recv, title, content,
                 file=None, ssl=False, email_host='smtp.126.com',
                 port=25, ssl_port=465):
        self.username = username  # 用户名
        self.passwd = passwd
        self.recv = recv  # 收件人，多个要传list
        self.title = title  # 邮件主题
        self.content = content  # 邮件正文
        self.file = file  # 附件路径
        self.email_host = email_host  # smtp服务器地址
        self.port = port  # 普通端口
        self.ssl = ssl  # 是否安全链接
        self.ssl_port = ssl_port  # 安全链接端口

    def send_email(self):
        msg =MIMEMultipart()
        # 发送内容的对象
        if self.file:  # 处理附件的
            file_name = os.path.split(self.file)[-1]  # 只取文件名，不取路径
            try:
                f = open(self.file, 'rb').read()
            except Exception as e:
                raise Exception('附件打不开！！！！')
            else:
                att = MIMEText(f, 'base64', 'utf-8')
                att['Content-Type'] = 'application/octet-stream'
                att['Content-Disposition'] = 'attachment; filename="%s"' % file_name
                msg.attach(att)
        msg.attach(MIMEText(self.content))  # 邮件正文的内容
        msg['Subject'] = self.title  # 邮件主题
        msg['From'] = self.username  # 发送者账号
        msg['To'] = ','.join(self.recv)  # 接收者账号列表
        if self.ssl:
            self.smtp = smtplib.SMTP_SSL(self.email_host, port=self.ssl_port)
        else:
            self.smtp = smtplib.SMTP(self.email_host, port=self.port)
        # 发送邮件服务器对象
        self.smtp.login(self.username, self.passwd)
        try:
            self.smtp.sendmail(self.username, self.recv, msg.as_string())
            pass
        except Exception as e:
            print('出错了...', e)
        else:
            print('发送成功！')
        self.smtp.quit()


if __name__ == '__main__':
    m = SendEmail(
        username='xxt114@126.com',
        passwd='QLNBMSJSUBIGFGNT',
        recv=['xuexiaoting@gen-song.net'],
        title='接口自动化测试报告',
        content='测试发送邮件',
        file=r'E:\PycharmProjects\WMSjktest2\result\report.html',
        ssl=True
    )
    m.send_email()




