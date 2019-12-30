from Getgoods import getgoods
from login import loginCook
from taobao import duobao
from inCode import inCode
# from multiprocessing import Process
import pymysql
import threading, time
from config import myredis
import redis
from config import mymysql
from rq import Queue

#先对一些变量定义事先实例化了几个对象
#redislink = redis.Redis(host = '120.27.22.37', port = 6347, decode_responses=True)
redislink = redis.Redis(host=myredis['host'], port=myredis['port'], decode_responses=True)
myqllink = pymysql.connect(host= mymysql['host'], user = mymysql['user'], passwd = mymysql['passwd'], db = mymysql['db'])


loginClass = loginCook()

allgoods = getgoods(redislink, myqllink)
duobaoClas = duobao()
thecode = inCode(allgoods, duobaoClas, loginClass, redislink, myqllink)

#使用队列
# qpaimai = Queue('low', connection = redislink)
# qcaiji = Queue('high', connection = redislink)


def shuru():

    thecode.startWork()

def caijirenwu(redislink):
    #采集数据的进程

    #数值2表示正在采集中
    redislink.getset("getgoods", 2)
    #判断现在是否是新的一天，如果是新的一天就清除goodlist（redis）和goods（数据库）
    theclick = int(time.strftime('%H', time.localtime(time.time())))
    #早上10点和下午两点之间采集数据时视为补充数据，不需要清楚历史数据
    if theclick <=10 or theclick >=14:
        allgoods.clearRedis()

    theresult = allgoods.getAllGoods()
    if theresult == 200:
        redislink.getset("getgoods", 0)

# def paimairenwu(goodsid, price, sqlNo):
#     #任务的队列生产者
#     #循环取出redis 有序集合trealist中当前时间的mapping
#     #查看相依的商品redis 的list中是否有待拍卖的
#     #有带拍卖的就将其计入到任务队列中
#     thecode.paimai(goodsid, price, sqlNo)



if __name__ == '__main__':
    redislink.getset("getgoods", 0)

    # keys = redislink.keys()
    # for key in keys:
    #     # print(key)
    #     type = redislink.type(key)
    #     if type == 'string':
    #         vals = redislink.get(key)
    #     elif type == 'list':
    #         vals = redislink.lrange(key, 0, -1)
    #         print(vals)
    #     elif type == 'set':
    #         vals = redislink.smembers(key);
    #     elif type == 'zset':
    #         vals = redislink.zrange(key, 0, -1)
    #     elif type == "hash":
    #         vals = redislink.hgetall(key)
    #     else:
    #         pass

    while True:
        print(time.time())
        t = threading.Thread(target=shuru, name='LoopThread')
        t.start()
        t.join()
        value = redislink.get("getgoods")
        if value == '1':
            t2 = threading.Thread(target=caijirenwu, name='shuchu', args=(redislink,))
            t2.start()
<<<<<<< HEAD

            # t2.join()

=======
            t2.join()
>>>>>>> 237b73309bef7f1901db145093c6ce30d7aaeea2


