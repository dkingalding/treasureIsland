import requests,json,time
import re
import pymysql
import redis
from config import mymysql
from config import myredis
from config import Agent
from random import randint
# import logging

#http://www.jdwl.com/order/search?waybillCodes=JD0010032744940

class kuaidi(object):
    def getkuaidi(self):
        #出价
        youcookie = self.loginClass.getCookies()

        buy_url = 'http://www.jdwl.com/waybill/trackWithPin?waybillCodes=JD0010110652524'
        data = {
            # 'trackId': 'dde516c09ed6a70f14d0d9404cd963c7',
            # 'eid': 'UM3RCYTFRHBSSVPTU6IQSQSIMW77JIHEC7PWVTBCEVGSCJWMNTV3THFHD4F3N7I7SOINX3RMKXD4HJY3OX6AR5FQCQ',
        }
        HEADERS = {
            'Referer': 'https://paipai.jd.com/auction-detail',
            'User-Agent':Agent[randint(0, 3)]['User-Agent'],
            'Cookie': youcookie
        }
        # data['price'] = str(int(price))
        # data['auctionId'] = str(auctionId)
        # print(data)
        resp = requests.post(buy_url, headers=HEADERS, data=data)

        resultdata = resp.json()
        print(resultdata)
        # if resultdata['code'] == 501 and resultdata['message'] == "用户未登录":
        #     self.loginClass.longduomingdao()
        #     titl = '拍卖时登录失败'
        #     content = 'http://120.27.22.37/index.php赶紧登录'
        #     mailclass = dingmail()
        #     mailclass.sendmail(titl, content)
        #     self.sendPrice(auctionId, price)
        # return resultdata