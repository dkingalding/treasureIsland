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

# 先对一些变量定义事先实例化了几个对象

redislink = redis.Redis(host=myredis['host'], port=myredis['port'], decode_responses=True)
myqllink = pymysql.connect(host=mymysql['host'], user=mymysql['user'], passwd=mymysql['passwd'], db=mymysql['db'])

loginClass = loginCook()

allgoods = getgoods(redislink, myqllink)
duobaoClas = duobao()
thecode = inCode(allgoods, duobaoClas, loginClass, redislink, myqllink)

# 使用队列
qpaimai = Queue('low', connection=redislink)
queue = Queue('high', connection=redislink)
qcaiji = queue




def paimairenwu(goodsid, sqlNo , endScore):
    # 任务的队列生产者
    # 循环取出redis 有序集合trealist中当前时间的mapping
    # 查看相依的商品redis 的list中是否有待拍卖的
    # 有带拍卖的就将其计入到任务队列中
    thecode.paimai(goodsid, sqlNo, endScore)


if __name__ == '__main__':
    # 需要任务队列，线程可以修改任务队列中的数据
    # 每次开启需要验证登录
    theclick = int(time.strftime('%H', time.localtime(time.time())))
    #早上10点和下午两点之间采集数据时视为补充数据，不需要清楚历史数据
    if theclick <=10 :
        loginClass.longduomingdao()
    loginClass.longduomingdao()
    while True:
        startScore = int(time.time() + 1) * 1000
        endScore = startScore+ 2000
        goodslist = redislink.zrangebyscore('treadlist', startScore, endScore)
        if goodslist:
            print(goodslist)
            print(startScore)
            print(endScore)
            for value in goodslist:
                threads = []
                dd = value.split('*')
                print(dd)
                if redislink.llen(dd[0]):
                    # 满足这些条件才开始进入任务队列
                    # 在这里开启线程
                    # 目前按照这逻辑在同一时间段只能拍卖一个商品
                    print("有订单要拍卖")
                    sqlNo = redislink.lindex(dd[0], 0)
                    print(sqlNo)
                    threads.append(threading.Thread(target=paimairenwu, name=sqlNo, args=(dd[1], sqlNo, endScore)))
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        redislink.zremrangebyscore('treadlist', 0, endScore)


