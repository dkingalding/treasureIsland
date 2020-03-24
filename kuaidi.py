import requests
import re
import pymysql

from config import mymysql

from config import Agent
from random import randint
from login import loginCook
from mailtongzhi import dingmail
import chardet#检测网页编码形式的模块
# import logging

#http://www.jdwl.com/order/search?waybillCodes=JD0010032744940

class kuaidi(object):
    def getkuaidi(self,kuaidi):
        #出价
        loginClass = loginCook()
        youcookie = loginClass.getCookies()

        buy_url = 'http://www.jdwl.com/waybill/trackWithPin?waybillCodes=%s'%kuaidi
        data = {

        }
        HEADERS = {
            'Referer': 'https://paipai.jd.com/auction-detail',
            'User-Agent':Agent[randint(0, 3)]['User-Agent'],
            'Cookie': youcookie
        }
        resp = requests.post(buy_url, headers=HEADERS, data=data)

        temp = resp.text.encode('utf-8').decode('utf8')
        find1 = u"(签收+)"

        find2 = u"(送往+)"
        find3 = u"(该运单暂无物流跟踪信息+)"
        find4 = u"(欢迎再次光临+)"
        pattern = re.compile(find4)
        results = pattern.findall(temp)
        if results:
            # 已经签收
            return 2
        pattern = re.compile(find1)
        results = pattern.findall(temp)
        if results:
            #已经签收
            return 2
        pattern = re.compile(find2)
        results = pattern.findall(temp)
        if results:
            # 已经发货
            return 1
        pattern = re.compile(find3)
        results = pattern.findall(temp)
        if results:
            # 没有发货
            return 0
        return 0

    def genxin(self, id, kuaidistatus):
        myqllink = pymysql.connect(host=mymysql['host'], user=mymysql['user'], passwd=mymysql['passwd'],
                                   db=mymysql['db'])
        cursor = myqllink.cursor()
        sql = "UPDATE  offorlog SET kuaidistatus = '{0}' WHERE id ='{1}'".format(kuaidistatus, id)
        cursor.execute(sql)
        # 执行sql语句
        myqllink.commit()

    def sendemail(self, emailcontent):

        if emailcontent:
            dingto = dingmail()
            thecontent = ""
            titl = '昨日已签收快递,提醒他们收货'
            for content in emailcontent:
                if content[2] ==1:
                    pingtai = "转转"
                else:
                    pingtai = "咸鱼"
                onecontent = "{0}----{1}----http://120.27.22.37/admin/offerlogs/{2}/edit".format(pingtai, content[3], content[0])
                thecontent = thecontent + onecontent + "\r\n"
        # print(thecontent)
            dingto.sendmail(titl, thecontent)

if __name__ == '__main__':
    myqllink = pymysql.connect(host=mymysql['host'], user=mymysql['user'], passwd=mymysql['passwd'],
                                    db=mymysql['db'])
    cursor = myqllink.cursor()
    kuai = kuaidi()
    sql = "SELECT id, kuaidi, pingtai, nicheng FROM offorlog  WHERE kuaidistatus <> 2 AND status = 1"
    cursor.execute(sql)
    # 执行sql语句
    myqllink.commit()
    results = cursor.fetchall()
    emailcontent = ''
    for offer in results:
        print(offer)
        if offer[1]:
            bb = kuai.getkuaidi(offer[1])
            kuai.genxin(offer[0], bb)
            if bb == 2:
                emailcontent = emailcontent+offer
                #将信息填入表格,发邮件用


    kuai.sendemail(emailcontent)
    # print(emailcontent)