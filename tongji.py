import json
import time
import threading
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
        auconttime = int(time.time() ) * 1000
        sql = "SELECT id, usedNo FROM goods WHERE endTime <= {0} ".format(auconttime)

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

            sql = "SELECT vagePrice FROM theprice WHERE  usedNo = {0}".format(goodslist[1])

            self.cursor.execute(sql)
            # 执行sql语句
            self.myqllink.commit()
            results = self.cursor.fetchone()

            if results:
                print(results[0])
                minprice = round(results[0] * 0.8)
                maxprice = round(results[0] * 1.2)
                if int(price[1]) < minprice:
                    pass
                elif int(price[1]) > maxprice:
                    pass
                else:
                    vageprice = round((int(results[0])*7 + int(price[1])*3)/10)
                    sql ="UPDATE theprice SET price = {0} , vagePrice = {1}  WHERE usedNo = '{2}'".format(str(price[1]), str(vageprice), str(goodslist[1]))
                    # print(sql)
                    self.cursor.execute(sql)
                    # 执行sql语句
                    self.myqllink.commit()

            else:
                #如果没有就存入数据
                sql = "INSERT INTO theprice (usedNo, vagePrice, price ) VALUES ({0}, {1},{2})".format(goodslist[1],price[1],price[1])

                self.cursor.execute(sql)
                # 执行sql语句
                self.myqllink.commit()


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

        bb = int(offset)*1000 + int(pinlv[1])
        # exit(print(bb))
        sql = "UPDATE theprice SET notes = '{0}' WHERE usedNo = {1}".format(bb, pinlv[0])

        self.cursor.execute(sql)
        # 执行sql语句
        self.myqllink.commit()

    def countofgood(self):
        #获取有多少数据，将数据分配到几个进程中采集
        auconttime = int(time.time()) * 1000
        sql = "SELECT COUNT(id) FROM  goods WHERE endTime <= {0}".format(auconttime)
        self.cursor.execute(sql)
        # 执行sql语句
        self.myqllink.commit()
        results = self.cursor.fetchall()
        return results


def jigetongji(*bb):
    giugiu = tongji()
    for goods in bb:
        giugiu.getcurrentPrice(goods)
        time.sleep(0.5)


if __name__ == '__main__':
    jiage = tongji()

    yesterday = (datetime.date.today() + datetime.timedelta(days = -1)).strftime("%y%m%d")
    # exit(yesterday)
    goodsno = jiage.shuliang()

    for nou in goodsno:
        jiage.pinlv(nou, yesterday)


    zongshu = jiage.countofgood()
    #获取商品总数，并平均分配给4个线程进行价格采集

    oneNo = round(zongshu[0][0]/4)

    #每个线程安排的商品数量

    #开启四个线程采集价格信息
    # exit(print(oneNo))
    bb = jiage.getgoodsid()
    bb1 = bb[0:oneNo]
    bb2 = bb[oneNo:oneNo*2]
    bb3 = bb[oneNo*2:oneNo*3]
    bb4 = bb[oneNo*3:oneNo*4]

    caijiduilie = []

    caijiduilie.append(threading.Thread(target=jigetongji, name='one', args=(bb1)))
    caijiduilie.append(threading.Thread(target=jigetongji, name='two', args=(bb2)))
    caijiduilie.append(threading.Thread(target=jigetongji, name='three', args=(bb3)))
    caijiduilie.append(threading.Thread(target=jigetongji, name='four', args=(bb4)))
    for t in caijiduilie:
        t.start()






