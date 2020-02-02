import time
import re
import pymysql
from config import mymysql
from config import Agent
from random import randint
import logging
import traceback

class seachgoods(object):

    def __init__(self):
        self.headers = {
            # "Host": "used-api.jd.com",
            # "Host" : "used - api.paipai.com",
            # "Connection": "keep-alive",
            # "Referer": "https: // paipai.jd.com / auction - list",
            # "Connection": "close",
            "User-Agent":Agent[randint(0, 3)]['User-Agent'],
        }
        self.errordata = {'geterror':[],'setsqlerror':[]}
        # self.redislink = redis.Redis(host=myredis['host'], port=myredis['port'], decode_responses=True)
        self.myqllink = pymysql.connect(host=mymysql['host'], user=mymysql['user'], passwd=mymysql['passwd'], db=mymysql['db'])
        self.cursor = self.myqllink.cursor()
        logging.basicConfig(filename='log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


    def getGoodsid(self, usedNo):
        #根据提供的usedNo获取拍卖品id
        #在获取历史成交价格和拍卖时选着使用
        auconttime = (int(time.time()))*1000
        sql = "SELECT id, startTime, endTime FROM goods WHERE usedNo LIKE '{0}%' AND endTime >= {1} ORDER BY endTime".format(usedNo,auconttime)
        try:
            self.cursor.execute(sql)
            # 执行sql语句
            self.myqllink.commit()
            results = self.cursor.fetchall()

        except:
            #将错误信息计入，并输出错误信息
            logging.error(traceback.format_exc())
            print("查询商品拍卖id {0} 出错".format(usedNo))
            results = ()
        finally:
            return results

    def getGoodInfo(self, usedNo):
        auconttime = int(time.time())*1000
        sql = "SELECT gg.id, ss.quality, ss.shopId, ss.productName, gg.endTime FROM usedName ss INNER JOIN " \
              " goods gg  ON ss.usedNo = gg.usedNo WHERE ss.usedNo = {0} AND gg.endTime >= {1}".format(
            usedNo, auconttime)
        try:
            self.cursor.execute(sql)
            # 执行sql语句
            self.myqllink.commit()
            results = self.cursor.fetchall()
        except:
            # 发生错误时回滚
            logging.error(traceback.format_exc())
            print("查询商品 usedNo {0} 出错".format(usedNo))
            results = ()
        finally:
            return results





    def getUsedNo(self, condition, shop = 0):
        #根据条件获取商品的usedNo 可以考虑将新旧程度也加上去
        #条件基本时允许商品名或者usedNo
        if shop != 0:
            shopcondition = ""
        else:
            shopcondition = "AND ss.shopId = 0"

        auconttime = int(time.time())*1000

        sql = "SELECT ss.usedNo, ss.quality, ss.shopId, ss.productName,COUNT(*) num FROM usedName ss INNER JOIN " \
              " goods gg  ON ss.usedNo = gg.usedNo WHERE ss.productName LIKE '%{0}%' AND gg.endTime >= {1} {2} GROUP BY ss.usedNo".format(
            condition, auconttime, shopcondition)
        try:
            self.cursor.execute(sql)
            # 执行sql语句
            self.myqllink.commit()
            results = self.cursor.fetchall()
        except:
            # 发生错误时回滚
            logging.error(traceback.format_exc())
            print("查询商品 usedNo {0} 出错".format(condition))
            results = ()
        finally:
            return results

    # def gethistory(self, auction):
    #     try:
    #         #https://used-api.paipai.com/auction/detail?callback=jQuery32108877681006626417_1574400875551&auctionId=120934440&p=2
    #         url = (
    #             "https://used-api.paipai.com/auction/detail?callback=jQuery32108877681006626417_1574400875551&auctionId={0}&p=2").format(
    #             auction)
    #         r = requests.get(url)
    #         result_json = re.search(r'{.*}', r.text)
    #         result_dict = json.loads(result_json.group())
    #         # print(result_dict)
    #         if result_dict['code'] == 200:
    #             pricelist = result_dict['data']['historyRecord']
    #             historyPrice = ''
    #             for nb in pricelist:
    #                 # print(nb['offerPrice'])
    #                 historyPrice = historyPrice + "/" + str(nb['offerPrice'])
    #         else:
    #             historyPrice = "数据出错"
    #     except:
    #         historyPrice = '获取历史价格错误'
    #     return historyPrice


