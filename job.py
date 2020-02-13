from login import loginCook
from offer import offer
import threading, time
from config import myredis
import redis
from Getgoods import getgoods
import os

os.environ['TZ'] = 'Asia/Shanghai'
redisPool = redis.ConnectionPool(host= myredis['host'], port= myredis['port'], max_connections=10, decode_responses=True)

# 从池子中拿一个链接

# loginClass = loginCook()




def paimairenwu(goodsid, sqlNo , endScore):
    # 任务的队列生产者
    # 循环取出redis 有序集合trealist中当前时间的mapping
    # 查看相依的商品redis 的list中是否有待拍卖的
    # 有带拍卖的就将其计入到任务队列中

    tt = offer(redisPool)
    tt.paimai(goodsid, sqlNo, endScore)

def caijirenwu(redislink, groupid):
    #控制采集

    #数值2表示正在采集中
    # conn = redis.Redis(connection_pool=redislink)
    print('有采集任务',groupid)

    #判断现在是否是新的一天，如果是新的一天就清除goodlist（redis）和goods（数据库）

    #早上10点和下午两点之间采集数据时视为补充数据，不需要清楚历史数据
    caijigoods = getgoods(redislink)
    # allgoods.clearRedis()

    #开始采集数据并返回采集结果
    theresult = caijigoods.getAllGoods(groupid)

    #如果采集结果返回为200 就将数据状态码改会0
    if theresult == 200:
        caijigoods.reorder()
        del(caijigoods)




if __name__ == '__main__':
    # 需要任务队列，线程可以修改任务队列中的数据
    # 每次开启需要验证登录
    #每次启动程序就登录保证cookies有效
    # thecode = offer(Pool)
    # offerno = thecode.tets()
    loginClass = loginCook()
    theclick = int(time.strftime('%H', time.localtime(time.time())))
    # caijigoods = getgoods(conn)
    # caijigoods.reorder()
    # conn = redis.Redis(connection_pool=Pool)
    # caijigoods = getgoods(conn)
    # caijigoods.clearRedis()
    #早上10点和下午两点之间采集数据时视为补充数据，不需要清楚历史数据
    # if theclick <=10 :
    #     loginClass.longduomingdao()
    # loginClass.longduomingdao()
    while True:
        conn = redis.Redis(connection_pool=redisPool)
        try:
            conn.ping()
        except:
            conn = redis.Redis(connection_pool= redisPool)
        singin = conn.get("singin")
        if singin == '1':
            loginClass.longduomingdao()
            conn.set("singin", 0)
        value = conn.get("getgoods")
        groupids = conn.smembers("groupgoods")
        #
        # 获取采集数据的状态码，是否开启采集线程
        theclick = int(time.strftime('%H', time.localtime(time.time())))
        if value == '1':
            caijiduilie = []
            caiji = getgoods(redisPool)
            conn.getset("getgoods", 2)

            print(groupids)
            if groupids:
                for groupid in groupids:

                    caijiduilie.append(threading.Thread(target=caijirenwu, name=groupid, args=(redisPool,groupid)))
                    # caijiduilie.append(threading.Thread(target=caijirenwu, name=bb, args=(redisPool, groupid)))
                for t in caijiduilie:
                    t.start()
            else:
                t2 = threading.Thread(target=caijirenwu, name='shuchu', args=(redisPool, '1000005'))
                t2.start()
            del(caiji)
        # #开始获取在一定时间段内的
        startScore = int(time.time() + 1) * 1000
        endScore = startScore+ 2000
        # print(startScore,endScore)
        # # startScore = 0
        # endScore = 1579174980000
        goodslist = conn.zrangebyscore('treadlist', startScore, endScore)
        # print(goodslist)
        # break
        if goodslist:
            print(goodslist)

            # print(startScore, endScore)
            # print(startScore)
            # print(endScore)
            thecode = offer(redisPool)
            for value in goodslist:
                threads = []
                dd = value.split('*')
                offerno = thecode.surestatus(dd[0])
                if offerno:
                    print('拍卖订单号', dd[0])

                    threads.append(threading.Thread(target=paimairenwu, name=dd[1], args=(dd[1], offerno, endScore)))

            for t in threads:
                t.start()
            for t in threads:
                t.join(5.0)
            del(thecode)
        #删除已经过时的记录,保证了任务不重复进行
        conn.zremrangebyscore('treadlist', 0, endScore)
        del(conn)

