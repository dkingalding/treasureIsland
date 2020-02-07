import smtplib
from email.mime.text import MIMEText
from email.header import Header

class dingmail(object):
    def __init__(self):
        self.from_addr='2502309334@qq.com'   #邮件发送账号
        self.to_addrs='1247975688@qq.com'   #接收邮件账号
        self.qqCode='fmfrjdqrgmsnecbf'   #授权码（这个要填自己获取到的）
        self.smtp_server='smtp.qq.com'#固定写死
        self.smtp_port=465#固定端口


    def sendmail(self, titl , content):
        #配置服务器
        stmp=smtplib.SMTP_SSL(self.smtp_server,self.smtp_port)
        stmp.login(self.from_addr,self.qqCode)

        #组装发送内容
        dindanurl = content
        message = MIMEText(dindanurl, 'plain', 'utf-8')   #发送的内容
        message['From'] = Header("alading夺宝岛", 'utf-8')   #发件人
        message['To'] = Header("", 'utf-8')   #收件人
        subject = titl
        message['Subject'] = Header(subject, 'utf-8')  #邮件标题

        try:
            stmp.sendmail(self.from_addr, self.to_addrs, message.as_string())
        except Exception as e:
            print ('邮件发送失败--' + str(e))
        print ('邮件发送成功')