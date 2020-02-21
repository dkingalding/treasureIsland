import pymysql
from offer import offer
from random import randint
from config import mymysql
from config import myredis
from config import Agent
import redis


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
        price = self.duijia.biPrice(goodslist[0],0,0)
        #使用offer类中的biprice 获取价格
        #如果返回的不是500就记录价格
        if price[0] != 400:
            print(price[1])



if __name__ == '__main__':
    jiage = tongji()
    bb = jiage.getgoodsid()
    # print(bb)
    jiage.getcurrentPrice(bb)
