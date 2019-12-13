from Getgoods import getgoods
from login import loginCook
from taobao import duobao
from inCode import inCode
from multiprocessing import Process
import threading, time
from config import myredis
import redis

#先对一些变量定义事先实例化了几个对象

redislink = redis.Redis(host=myredis['host'], port=myredis['port'], decode_responses=True)
loginClass = loginCook()
allgoods = getgoods()
duobaoClas = duobao()
thecode = inCode(allgoods, duobaoClas, loginClass, redislink)

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
    while True:
        print("11")
        time.sleep(10)





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
    threads = []
    t = threading.Thread(target=shuru, name='LoopThread')
    threads.append(t)
    t2 = threading.Thread(target=caijirenwu, name='shuchu', args=(redislink,))
    threads.append(t2)
    # p = Process(target=paimairenwu )
    # threads.append(p)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # t.start()
    # t.join()
    # t2.start()
    # t2.join()

    # while Tru
    #     pass
