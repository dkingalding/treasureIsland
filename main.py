from Getgoods import getgoods
from login import loginCook
from taobao import duobao
from inCode import inCode
from multiprocessing import Process
import pymysql
import threading, time
from config import myredis
import redis
from config import mymysql
#先对一些变量定义事先实例化了几个对象

redislink = redis.Redis(host=myredis['host'], port=myredis['port'], decode_responses=True)
myqllink = pymysql.connect(host= mymysql['host'], user = mymysql['user'], passwd = mymysql['passwd'], db = mymysql['db'])

loginClass = loginCook()

allgoods = getgoods(redislink, myqllink)
duobaoClas = duobao()
thecode = inCode(allgoods, duobaoClas, loginClass, redislink, myqllink)

def shuru():
    thecode.startWork()

def caijirenwu(redislink):
    #采集数据的进程
    while True:
        value = redislink.get("getgoods")
        if value == '1':
            #数值2表示正在采集中
            redislink.getset("getgoods", 2)
            allgoods.clearRedis()
            theresult = allgoods.getAllGoods()
            if theresult == 200:
                redislink.getset("getgoods", 0)

def paimairenwu():
    #任务的队列生产者
    #循环取出redis 有序集合trealist中当前时间的mapping
    #查看相依的商品redis 的list中是否有待拍卖的
    #有带拍卖的就将其计入到任务队列中
    while True:
        #开始抢购
        pass




if __name__ == '__main__':

    #将所有的类进行实例化，并传入到需要的类中
    # loginClass = loginCook()
    # allgoods = getgoods()
    # duobaoClas = duobao()
    # thecode = inCode(allgoods, duobaoClas, loginClass)
    # thecode.startWork()

    # noll = 122328470
    # yy = duobaoClas.goodsinfo(noll)
    # print(yy['data'][str(noll)]['currentPrice'])

    # 122328470
    # thecode.startWork()
    #在主程序中只执行in code类的输入函数

    # p.start()
    # p.join()

    #需要任务队列，线程可以修改任务队列中的数据
    redislink.getset("getgoods", 0)
    # keys = redislink.keys()
    #
    # if 'treadlist' in keys:
    #     pass
    # else:
    #     #创建有序集合
    #     pass

    threads = []
    t = threading.Thread(target=shuru, name='LoopThread')
    threads.append(t)
    t2 = threading.Thread(target=caijirenwu, name='shuchu', args=(redislink,))
    threads.append(t2)
    # p = Process(target=paimairenwu )
    # p.start()
    # threads.append(p)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # p.join()
    # t.start()
    # t.join()
    # t2.start()
    # t2.join()

    # while Tru
    #     pass
