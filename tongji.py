import json
from time import sleep

import pymysql
from offer import offer
from random import randint
from config import mymysql
from config import myredis
from config import Agent
import redis
import datetime


class tongji(object):
    def __init__(self):
        self.headers = {
            # "Host": "used-api.jd.com",
            # "Host" : "used - api.paipai.com",
            # "Connection": "keep-alive",
            # "Referer": "https: // paipai.jd.com / auction - list",
            # "Connection": "close",
            "User-Agent": Agent[randint(0, 3)]['User-Agent'],
        }

        self.errordata = {'geterror': [], 'setsqlerror': []}
        # self.redislink = redis.Redis(connection_pool=conredis)
        # self.redispool = conredis
        # self.redislink = redis.Redis(host=myredis['host'], port=myredis['port'], decode_responses=True)
        self.myqllink = pymysql.connect(host=mymysql['host'], user=mymysql['user'], passwd=mymysql['passwd'],
                                        db=mymysql['db'])
        self.cursor = self.myqllink.cursor()
        redisPool = redis.ConnectionPool(host=myredis['host'], port=myredis['port'], max_connections=10,
                                         decode_responses=True)

        self.duijia = offer(redisPool)
        # logging.basicConfig(filename='log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    def getgoodsid(self):
        sql = "SELECT id, usedNo FROM goods"

        try:
            self.cursor.execute(sql)
            # 执行sql语句
            self.myqllink.commit()
            results = self.cursor.fetchall()
        except:
            results = ()
        finally:
            return results

    def getcurrentPrice(self, goodslist):
        # print(goodslist)
        price = self.duijia.biPrice(goodslist[0],0,0)
        #使用offer类中的biprice 获取价格
        #如果返回的不是500就记录价格
        #并将价格存入数据库
        # print(price)
        if price[0] != 500:

            sql = "SELECT price,id FROM theprice WHERE  useedNo = {0}".format(goodslist[0])
            try:
                self.cursor.execute(sql)
                # 执行sql语句
                self.myqllink.commit()
                results = self.cursor.fetchone()
            except:
                results = ()
            if results:
                vageprice = round(results[0]/2 + price[1]/2)
                sql ="UPDATE theprice SET price ={0}, vagePrice={1} WHERE usedNo = {2}".format( price[1],vageprice, goodslist[0])
                try:
                    self.cursor.execute(sql)
                    # 执行sql语句
                    self.myqllink.commit()
                except:
                    # print('存入价格错误')
                    pass
            else:
                #如果没有就存入数据
                sql = "INSERT INTO theprice (usedNo, vagePrice, price ) VALUES ({0}, {1},{2})".format(goodslist[1],price[1],price[1])
                try:
                    self.cursor.execute(sql)
                    # 执行sql语句
                    self.myqllink.commit()
                except:
                    # print('存入价格错误')
                    pass

    def shuliang(self):
        sql = "SELECT  usedNo, COUNT(*) FROM goods GROUP BY usedNo"
        try:
            self.cursor.execute(sql)
            # 执行sql语句
            self.myqllink.commit()
            results = self.cursor.fetchall()
        except:
            results = ()
        finally:
            return results

    def pinlv(self, pinlv, offset):
        sql = "SELECT  notes FROM theprice where usedNo = {0}".format(pinlv[0])
        self.cursor.execute(sql)
        # 执行sql语句
        self.myqllink.commit()
        results = self.cursor.fetchone()
        # print(results)

        # if results:
        #     jsonresulte = json.loads(results[0])
        #     if len(jsonresulte) >= 10:
        #         jsonresulte.pop()
        # else:
        #     jsonresulte = []
        bb = str(offset) + '*' + str(pinlv[1])
        # jsondata = json.dumps(jsonresulte)
        sql = "UPDATE theprice SET notes ={0} WHERE usedNo = {1}".format(bb, pinlv[0])
        # print(sql)
        self.cursor.execute(sql)
        # 执行sql语句
        self.myqllink.commit()
        # try:
        #     self.cursor.execute(sql)
        #     # 执行sql语句
        #     self.myqllink.commit()
        #     results = self.cursor.fetchone()
        #     # print(results)
        #
        #     if len(results)>= 10:
        #         results.pop()
        #     results.append(offset+'*'+pinlv[1])
        #
        #     sql = "UPDATE theprice SET notes ={0} usedNo = {1}".format(results, pinlv[0])
        #
        #     self.cursor.execute(sql)
        #     # 执行sql语句
        #     self.myqllink.commit()
        # except:
        #     pass


if __name__ == '__main__':
    jiage = tongji()

    bb = jiage.getgoodsid()
    # print(bb)
    for goods in bb:
        jiage.getcurrentPrice(goods)
        sleep(1)
    yesterday = (datetime.date.today() + datetime.timedelta(days = -1)).strftime("%m-%d")

    goodsno = jiage.shuliang()
    # print(goodsno)
    for nou in goodsno:
        # print(nou[0])
        jiage.pinlv(nou, yesterday)
    # print(goodsno)
