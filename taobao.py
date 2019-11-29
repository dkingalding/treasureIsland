import requests,json
import re
from random import randint
from config import Agent

class duobao(object):

    def onegoods(self):
        #获取已经存储的信息
        pass

    def goodsinfo(self, paimaiid):
        #获取目前最高价格
        #https://used-api.paipai.com/auctionRecord/batchCurrentInfo?auctionId=120846715&callback=__jp5
        s = requests.session()
        headers = {
            "User-Agent": Agent[randint(0, 3)]['User-Agent'],
        }
        query_url = 'https://used-api.paipai.com/auctionRecord/batchCurrentInfo?auctionId={0}&callback=__jp5' \
            .format(paimaiid)
        try:
            r = s.get(query_url, headers=headers, timeout=1)
            # print(r.text)
            result_json = re.search(r'{.*}', r.text)
            result_dict = json.loads(result_json.group())
            return result_dict
        except:
            print("查询商品价格超过1s")

    def sendPrice(self,youcookie,auctionId,price):
        #出价
        buy_url = 'https://used-api.jd.com/auctionRecord/offerPrice'
        data = {
            # 'trackId': 'dde516c09ed6a70f14d0d9404cd963c7',
            # 'eid': 'UM3RCYTFRHBSSVPTU6IQSQSIMW77JIHEC7PWVTBCEVGSCJWMNTV3THFHD4F3N7I7SOINX3RMKXD4HJY3OX6AR5FQCQ',
        }
        HEADERS = {
            'Referer': 'https://paipai.jd.com/auction-detail',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
            'Cookie': youcookie
        }
        data['price'] = str(int(price))
        data['auctionId'] = str(auctionId)
        # print(data)
        resp = requests.post(buy_url, headers=HEADERS, data=data)
        print(resp.json())

    def offerOrNot(self):
        #判断是否出价和出多高的价格
        pass

