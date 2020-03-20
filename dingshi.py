from login import loginCook
from offer import offer
import threading, time
from config import myredis
import redis
from Getgoods import getgoods
import os
from huodan import huodan

os.environ['TZ'] = 'Asia/Shanghai'
Pool = redis.ConnectionPool(host= myredis['host'], port= myredis['port'], max_connections=10, decode_responses=True)

# 从池子中拿一个链接

# loginClass = loginCook()






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

    conn = redis.Redis(connection_pool=Pool)
    value = conn.get("getgoods")
    # groupids = [1000005,1999999]
    groupids = conn.smembers("groupgoods")
    caijiduilie = []
    caiji = getgoods(Pool)
    conn.getset("getgoods", 2)

    caiji.clearRedis()
    print(groupids)
    if groupids:
        for groupid in groupids:
            caijiduilie.append(threading.Thread(target=caijirenwu, name='shuchu', args=(Pool,groupid)))

        for t in caijiduilie:
            t.start()
    else:
        t2 = threading.Thread(target=caijirenwu, name='shuchu', args=(Pool, '1000005'))
        t2.start()
    del(caiji)

    del(conn)
    xianyu = huodan(conn)
    xianyu.shengchengliebieo()

