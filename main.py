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
from seachgoods import seachgoods
from mailtongzhi import dingmail
from rq import Queue
from huodan import huodan

#先对一些变量定义事先实例化了几个对象
#redislink = redis.Redis(host = '120.27.22.37', port = 6347, decode_responses=True)
redislink = redis.Redis(host=myredis['host'], port=myredis['port'], decode_responses=True)
myqllink = pymysql.connect(host= mymysql['host'], user = mymysql['user'], passwd = mymysql['passwd'], db = mymysql['db'])
redisPool = redis.ConnectionPool(host= myredis['host'], port= myredis['port'], max_connections=10, decode_responses=True)



#实例化采集类
# allgoods = getgoods()
seachgoods = seachgoods()


#实例化操作输入类
thecode = inCode(seachgoods)

#使用队列
# qpaimai = Queue('low', connection = redislink)
# qcaiji = Queue('high', connection = redislink)


def shuru():
    #使用线程开始输入控制管理
    thecode.startWork()

# def caijirenwu(redislink):
#     #控制采集
#
#     #数值2表示正在采集中
#     redislink.getset("getgoods", 2)
#     #判断现在是否是新的一天，如果是新的一天就清除goodlist（redis）和goods（数据库）
#     theclick = int(time.strftime('%H', time.localtime(time.time())))
#     #早上10点和下午两点之间采集数据时视为补充数据，不需要清楚历史数据
#     if theclick <=10 or theclick >=14:
#         allgoods.clearRedis()
#     #开始采集数据并返回采集结果
#     theresult = allgoods.getAllGoods()
#
#     #如果采集结果返回为200 就将数据状态码改会0
#     if theresult == 200:
#         redislink.getset("getgoods", 0)

# def paimairenwu(goodsid, price, sqlNo):
#     #任务的队列生产者
#     #循环取出redis 有序集合trealist中当前时间的mapping
#     #查看相依的商品redis 的list中是否有待拍卖的
#     #有带拍卖的就将其计入到任务队列中
#     thecode.paimai(goodsid, price, sqlNo)



if __name__ == '__main__':
    redisPool = redis.ConnectionPool(host=myredis['host'], port=myredis['port'], max_connections=10,
                                     decode_responses=True)

    myqllink = pymysql.connect(host=mymysql['host'], user=mymysql['user'], passwd=mymysql['passwd'],
                                    db=mymysql['db'])
    cursor = myqllink.cursor()
    # sql ="SELECT usedNo FROM usedName  GROUP BY usedNo HAVING count(usedNo)>1"


    sql ="DELETE FROM usedName WHERE id IN (select id from (select id from usedName where usedNo in (SELECT usedNo FROM usedName GROUP BY usedNo HAVING count(usedNo)>1) AND" \
         " id NOT IN (SELECT min(id) FROM usedName  GROUP BY usedNo HAVING count(usedNo)>1))as bb)"
    # # cursor.execute(sql)
    # # 执行sql语句
    # myqllink.commit()

    cursor.execute(sql)
    # 执行sql语句
    myqllink.commit()
    # results2 = cursor.fetchall()
    # #
    # #
    # exit(print(results2))
    #y
    # caijigoods = getgoods(redisPool)
    # caijigoods.clearRedis()

    # caijigoods.reorder()
    # redislink.getset("getgoods", 0)

    # offerlist =9
    # titl = '%s订单拍卖成功，填写地址付钱' % offerlist
    # content = 'http://120.27.22.37/admin/offerlogs/%s/edit' % offerlist
    # mailclass = dingmail()
    # mailclass.sendmail(titl, content)
    # keys = redislink.keys()
    # for key in keys:
    #     redislink.delete(key)
        # # print(key)
        # # type = redislink.type(key)
        # if type == 'string':
        #     pass
        # #     vals = redislink.get(key)
        # # elif type == 'list':
        # #     vals = redislink.lrange(key, 0, -1)
        # #     print(vals)
        # elif type == 'set':
        #     vals = redislink.smembers(key);
        #     print(vals)
        # # elif type == 'zset':
        # #     vals = redislink.zrange(key, 0, -1)
        # # elif type == "hash":
        # #     vals = redislink.hgetall(key)
        # else:
        #     pass

    #     if key != "goodslist"or key != "shop" or key != "usedName" or key != "getgoods"or key !='groupgoods':
    #         redislink.delete(key)
    #
    # while True:
    #
    #     shuru()

    xianyu = huodan(redisPool)
    xianyu.shengchengliebieo()

