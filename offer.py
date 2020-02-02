import time
from config import myredis
import redis
from config import mymysql
import pymysql
from taobao import duobao
from seachgoods import seachgoods

class offer(object):
    #接受指令，并在本类中完成对其他基本类的调用，完成所有功能
    def __init__(self,  Pool):
        #将所有传入的实例都赋值给类内部
        #定义一个全局变量或者内部变量记录获取输入的内容
        self.allgoods = seachgoods()
        self.duobaoClass = duobao()
        # self.loginClass = loginClass

        self.redislink = redis.Redis(connection_pool=Pool)
        self.myqllink = pymysql.connect(host=mymysql['host'], user=mymysql['user'], passwd=mymysql['passwd'], db=mymysql['db'])

        self.cursor = self.myqllink.cursor()

    def seachgoods(self, unsedno,  shopid):

        goodsinfo = self.allgoods.getUsedNo(unsedno, shopid)

        if goodsinfo :
            for value in goodsinfo:
                goodslist = self.allgoods.getGoodsid(value[0])
                if goodslist:
                    hisprice = self.allgoods.gethistory(goodslist[0][0])
                    value = value + (hisprice, )
                print(value)
        else:
            print("没有相关商品")


    def paimai(self, goodsid, sqlNo, endtime):
        #开始拍卖
        #拍卖的时候可以需要商品的usedNo 和价格
        #根据usedNo 获取商品的id 根据结束时间排序
        #查询最近时间商品的价格，如果高于规定价格就拍卖
        #查询自己出的价格是否有效，是否超过了自己定的价格
        #如果没有超过自己的定价就继续出价
        #拍卖结束后，如果拍到了，待拍数量减一。如果没有拍到，计入下一个时间段的任务
        # print("paimai")
        offerlist = self.goodssend(sqlNo)
        print(offerlist)
        if not offerlist:
            print("没有本次拍卖")
            return

        theMaxprice = round(float(offerlist[0][2]))

        print(theMaxprice, theMaxprice)
        nowtime = round(time.time() * 1000)
        print(nowtime)
        #需要那结束时间对比，在结束前一秒开始拍卖
        firsttime = int(endtime) - nowtime
        print(firsttime)

        # if firsttime <=2000 and firsttime > 0:
        if firsttime > 0:
            #满足这个条件是才开始竞价
            # pass
            iscontend = 1
            myprice = 0
            result = {'code': 400, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": 0}
            # while firsttime <=1000 and firsttime > -500 and iscontend:
            while firsttime > 0 and iscontend:
                thestatus = self.biPrice(goodsid, myprice, theMaxprice)
                firsttime = int(endtime) - round(time.time() * 1000)
                print(thestatus)
                if thestatus[0] == 400:
                    result = {'code':400, 'goodsid':goodsid, "usedNo":offerlist[0][1], "price":1 }
                    iscontend = 0
                    break
                elif thestatus[0] == 300:
                    myprice = thestatus[1] + 3
                    print(myprice)
                    if myprice >= theMaxprice:
                        myprice = theMaxprice
                    if myprice >= 93 and myprice <= 99:
                        myprice = 99
                    bb = self.chujia(goodsid, myprice)
                    if bb ==200:
                        result = {'code': 200, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": myprice}
                    elif bb == 304:
                        result = {'code': 300, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": myprice}
                    elif bb == 305:
                        result = {'code': 300, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": myprice}
                        #如果出价成功，记录出价记录
                        break
                    else:
                        result = {'code': 300, 'goodsid': goodsid, "usedNo":offerlist[0][1], "price": 1}
                        myprice = 0
                        # 如果出价失败，不记录出价记录
                else:
                    #记录拍卖状态
                    result = {'code': 200, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": myprice}

            if result['code'] == 200:
                #将成功的计入到数据库，并消除代拍任务
                #UPDATE Person SET Address = 'Zhongshan 23', City = 'Nanjing' WHERE LastName = 'Wilson'
                try:
                    if myprice < 99:
                        myprice = myprice + 8
                    sql = "UPDATE  offorlog SET goodsid = '{0}', officePrice = '{1}' , endtime = '{2}',status = 1 \
        WHERE id ='{3}'".format(goodsid, myprice, time.strftime("%Y-%m-%d", time.localtime()),sqlNo )
                    self.cursor.execute(sql)
                    # 执行sql语句
                    self.myqllink.commit()
                    self.redislink.lpop(sqlNo)
                except:
                    # logging.error(traceback.format_exc())
                    # self.errordata['setsqlerror'].append(data)
                    print("拍卖存入失误")
                    self.myqllink.rollback()
                print("拍卖成功")
                pass
            else:
                print("本次拍卖失败", result['code'])
        else:
            print("还没有到出价的最后一秒")



    def biPrice(self, goodsid, myprice,theMaxprice):
        print("对价",myprice)
        goodsinfo = self.duobaoClass.goodsinfo(goodsid)
        if not goodsinfo:
            return [300, myprice]
        currentPrice = int(goodsinfo['data'][str(goodsid)]['currentPrice'])
        if currentPrice > int(theMaxprice):
            #返回通知结束进程，并取消着次竞拍
            print("已经超过限定价格")
            return [400, currentPrice]
        elif currentPrice > int(myprice):
            #继续出价
            print("已经超过我出价格")
            return [300, currentPrice]
        elif currentPrice == int(myprice):
            #返回200，如果超过时间了，还是200，那就竞拍成功
            #在拍卖的主程序中将拍卖删除，代拍数列中也删除一个任务
            return [200, currentPrice]
        else :
            return [300, currentPrice]

    def chujia(self, goodsid, myprice):
        print("在出价")
        thecode = self.duobaoClass.sendPrice(goodsid, myprice)
        if thecode['code'] != 200:
            print(thecode)
            return thecode['code']
        else:
            print("出价成功")
            return 200

    def dinghis(self):
        keys = self.redislink.keys()
        for key in keys:
            # print(key)
            type = self.redislink.type(key)
            if type == 'list':
                print(key)
                vals = self.redislink.lrange(key, 0, -1)
                print(vals)
            elif type == 'zset':
                print(key)
                vals = self.redislink.zrange(key, 0, -1)
                print(vals)
            else:
                pass

    def surestatus(self, usedno):
        print('dd',usedno)
        if self.redislink.llen(usedno):
            sqlNo = self.redislink.lindex(usedno, 0)
            print(sqlNo)
            offerlist = self.goodssend(sqlNo)
            print(offerlist)
            if offerlist:
                return sqlNo
            else:
                print('删除订单',sqlNo)
                self.redislink.lpop(usedno)
                self.surestatus(usedno)
        else:
            return

    def goodssend(self, offerid):
        #查询订单
        sql = "SELECT id, usedNo, officePrice  FROM offorlog WHERE id = {0} AND status = 0".format(offerid)
        # print(sql)
        # self.cursor.execute(sql)
        # # 执行sql语句
        # self.myqllink.commit()
        # results = self.cursor.fetchall()
        # return results
        try:
            self.cursor.execute(sql)
            # 执行sql语句
            self.myqllink.commit()
            results = self.cursor.fetchall()
        except:
            #将错误信息计入，并输出错误信息
            # logging.error(traceback.format_exc())
            print("查询商品拍卖记录{0} 出错".format(offerid))
            results = ()
        finally:
            return results

    def tets(self):
        sql = "UPDATE  offorlog SET goodsid = '{0}', officePrice = '{1}' , endtime = '{2}'  ,status = 1 \
        WHERE id = '{3}'".format(111, 111, time.strftime("%Y-%m-%d", time.localtime()), 1)
        self.cursor.execute(sql)
        # 执行sql语句
        self.myqllink.commit()
