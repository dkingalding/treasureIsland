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

redislink = redis.Redis(host=myredis['host'], port=myredis['port'], decode_responses=True)
myqllink = pymysql.connect(host= mymysql['host'], user = mymysql['user'], passwd = mymysql['passwd'], db = mymysql['db'])


loginClass = loginCook()

allgoods = getgoods(redislink, myqllink)
duobaoClas = duobao()
thecode = inCode(allgoods, duobaoClas, loginClass, redislink, myqllink)

#使用队列
qpaimai = Queue('low', connection = redislink)
qcaiji = Queue('high', connection = redislink)


def shuru():

    thecode.startWork()

def caijirenwu(redislink):
    #采集数据的进程

    #数值2表示正在采集中
    redislink.getset("getgoods", 2)
    allgoods.clearRedis()
    theresult = allgoods.getAllGoods()
    if theresult == 200:
        redislink.getset("getgoods", 0)

def paimairenwu(goodsid, price, sqlNo):
    #任务的队列生产者
    #循环取出redis 有序集合trealist中当前时间的mapping
    #查看相依的商品redis 的list中是否有待拍卖的
    #有带拍卖的就将其计入到任务队列中
    thecode.paimai(goodsid, price, sqlNo)



if __name__ == '__main__':

    allgoods.clearRedis()
    #需要任务队列，线程可以修改任务队列中的数据
    # print(time.time())
    # redislink.getset("getgoods", 0)
    # threads = []
    # thecode.paimai(123201716, 27, 17)
    # print(duobaoClas.goodsinfo(123213509))
    while True:
        print(time.time())
        t = threading.Thread(target=shuru, name='LoopThread')
        # threads.append(t)
        t.start()
        t.join()
        value = redislink.get("getgoods")
        if value == '1':
            t2 = threading.Thread(target=caijirenwu, name='shuchu', args=(redislink,))
            # threads.append(t2)
            t2.start()


