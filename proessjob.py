from login import loginCook
from offer import offer
import threading, time
from config import myredis
import redis
from Getgoods import getgoods
import os
import multiprocessing
from mailtongzhi import dingmail
from huodan import huodan

os.environ['TZ'] = 'Asia/Shanghai'
redisPool = redis.ConnectionPool(host= myredis['host'], port= myredis['port'], max_connections=10, decode_responses=True)

# 从池子中拿一个链接

# loginClass = loginCook()

def paimairenwu(goodsid, sqlNo , endScore,usedno ):
    # 任务的队列生产者
    # 循环取出redis 有序集合trealist中当前时间的mapping
    # 查看相依的商品redis 的list中是否有待拍卖的
    # 有带拍卖的就将其计入到任务队列中

    tt = offer(redisPool)
    tt.paimai(goodsid, sqlNo, endScore, usedno)

def paimaibaozhen(goodsid, sqlNo , endScore,usedno ):
    # 拍卖保证
    tt = offer(redisPool)
    tt.paimaibaozhen(goodsid, sqlNo, endScore, usedno)




def caijirenwu(redislink, groupid):
    #控制采集

    #数值2表示正在采集中
    # conn = redis.Redis(connection_pool=redislink)
    print('需要采集任务',groupid)

    #判断现在是否是新的一天，如果是新的一天就清除goodlist（redis）和goods（数据库）

    #早上10点和下午两点之间采集数据时视为补充数据，不需要清楚历史数据
    caijigoods = getgoods(redislink)
    # allgoods.clearRedis()
    xianyu = huodan(redislink)
    #开始采集数据并返回采集结果
    theresult = caijigoods.getAllGoods(groupid)

    #如果采集结果返回为200 就将数据状态码改会0
    if theresult == 200:
        caijigoods.reorder()
        xianyu.shengchengliebieo()
        del(caijigoods)




if __name__ == '__main__':
    # 需要任务队列，线程可以修改任务队列中的数据
    # 每次开启需要验证登录
    #每次启动程序就登录保证cookies有效
    # thecode = offer(Pool)
    # offerno = thecode.tets()

    try:
        loginClass = loginCook()
        theclick = int(time.strftime('%H', time.localtime(time.time())))

        # if theclick <=10 :
        #     loginClass.longduomingdao()
        #开启进程池
        pool = multiprocessing.Pool()

        while True:
            conn = redis.Redis(connection_pool=redisPool)
            try:
                conn.ping()
                singin = conn.get("singin")
            except:
                conn = redis.Redis(connection_pool=redisPool)
                continue
            #查看是否需要登录
            singin = conn.get("singin")

            if singin == '1':
                loginClass.longduomingdao()
                conn.set("singin", 0)

            # 获取采集数据的状态码，是否开启采集线程
            value = conn.get("getgoods")
            groupids = conn.smembers("groupgoods")
            theclick = int(time.strftime('%H', time.localtime(time.time())))
            if value == '1':
                # groupids = [1000005,1999999]
                groupids = conn.smembers("groupgoods")
                caijiduilie = []

                conn.getset("getgoods", 2)

                print(groupids)
                if groupids:
                    for groupid in groupids:
                        caijiduilie.append(threading.Thread(target=caijirenwu, name='shuchu', args=(redisPool, groupid)))

                    for t in caijiduilie:
                        t.start()
                    for t in caijiduilie:
                        t.join()
                else:
                    t2 = threading.Thread(target=caijirenwu, name='shuchu', args=(redisPool, '1000005'))
                    t2.start()
                    t2.join()
                xianyu = huodan(redisPool)
                xianyu.shengchengliebieo()
                del (conn)
                # caijiduilie = []
                # caiji = getgoods(redisPool)
                # conn.getset("getgoods", 2)
                # if 'all' in  groupids:
                #     t2 = threading.Thread(target=caijirenwu, name='shuchu', args=(redisPool, ''))
                #     t2.start()
                #
                # else:
                #
                #     print(groupids)
                #     if groupids:
                #         for groupid in groupids:
                #             caijiduilie.append(threading.Thread(target=caijirenwu, name='shuchu', args=(redisPool,groupid)))
                #
                #         for t in caijiduilie:
                #             t.start()
                #     else:
                #         t2 = threading.Thread(target=caijirenwu, name='shuchu', args=(redisPool, '1000005'))
                #         t2.start()
                #
                # del(caiji)

            # #开始获取在一定时间段内的
            #开始抢购
            startScore = int(time.time() + 1) * 1000
            endScore = startScore+ 4000
            # endScore =2000000000000
            goodslist = conn.zrangebyscore('treadlist', startScore, endScore)
            # print(goodslist)
            # break
            if goodslist:
                print('获取treadlist',goodslist)
                thecode = offer(redisPool)
                for value in goodslist:
                    # threads = []
                    dd = value.split('*')
                    #传的是usedno 去调后四位新旧的 数据
                    offerno = thecode.surestatus(dd[0])

                    if offerno:
                        print('进程开启')
                        pool.apply_async(paimairenwu,(dd[1], offerno, endScore, dd[0]))
                        pool.apply_async(paimaibaozhen,(dd[1], offerno, endScore, dd[0]))
                        # threads.append(threading.Thread(target=paimairenwu, name=offerno, args=(dd[1], offerno, endScore)))
                del(thecode)
            #删除已经过时的记录
            conn.zremrangebyscore('treadlist', 0, endScore)
            del(conn)
    except (OSError, TypeError) as reason:
        titl = '程序启动错误，请快登录电脑重启'
        content = '错误的原因是:', str(reason)
        mailclass = dingmail()
        mailclass.sendmail(titl, content)
