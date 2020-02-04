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


    def paimai(self, goodsid,offerlist , endtime):
        #开始拍卖
        #拍卖的时候可以需要商品的usedNo 和价格
        #根据usedNo 获取商品的id 根据结束时间排序
        #查询最近时间商品的价格，如果高于规定价格就拍卖
        #查询自己出的价格是否有效，是否超过了自己定的价格
        #如果没有超过自己的定价就继续出价
        #拍卖结束后，如果拍到了，待拍数量减一。如果没有拍到，计入下一个时间段的任务
        # print("paimai")
        # offerlist = self.goodssend(sqlNo)
        # print(offerlist)
        # if not offerlist:
        #     print("没有本次拍卖")
        #     return

        theMaxprice = round(float(offerlist[0][2]))

        print(theMaxprice)

        #满足这个条件是才开始竞价
        # pass
        firsttime = 1
        myprice = 0
        result = {'code': 400, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": 0}

        while firsttime > 0:
            #计算时间
            firsttime = int(endtime) - round(time.time() * 1000) + 50

            if firsttime <= 200:
                thestatus = self.biPrice(goodsid, myprice, theMaxprice)
                print( offerlist[0][0],thestatus)
                if thestatus[0] == 400:
                    #超过了价格
                    result = {'code':400, 'goodsid':goodsid, "usedNo":offerlist[0][1], "price":1 }
                    break
                elif thestatus[0] == 300:
                    #新改出价方案
                    for i in range(thestatus[1],theMaxprice):
                        if i >= 93 and i <= 99:
                            i = 99
                        bb = self.chujia(goodsid, i)
                        if bb == 200:
                            result = {'code': 200, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": myprice}
                            myprice = i
                        elif bb == 304:
                            result = {'code': 300, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": myprice}
                            myprice = 0
                            # 拍卖出价过低
                        elif bb == 305:
                            # result = {'code': 300, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": myprice}
                            # 拍卖结束
                            break
                    # myprice = thestatus[1] + 1
                    #
                    # if myprice >= theMaxprice:
                    #     myprice = theMaxprice
                    # if myprice >= 93 and myprice <= 99:
                    #     myprice = 99

                    # myprice2 = thestatus[1] + 6
                    #
                    # if myprice2 >= theMaxprice:
                    #     myprice2 = theMaxprice
                    # if myprice2 >= 93 and myprice2 <= 99:
                    #     myprice2 = 99
                    # print(myprice)
                    #
                    # bb = self.chujia(goodsid, myprice)
                    #
                    # if bb == 200:
                    #     result = {'code': 200, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": myprice}
                    # elif bb == 304:
                    #     result = {'code': 300, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": myprice}
                    #     myprice = 0
                    #     # 拍卖出价过低
                    # elif bb == 305:
                    #     result = {'code': 300, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": myprice}
                    #     #拍卖结束
                    #     break
                    # else:
                    #     result = {'code': 300, 'goodsid': goodsid, "usedNo":offerlist[0][1], "price": 1}
                    #     myprice = 0
                        # 如果出价失败，不记录出价记录
                else:
                    #记录拍卖状态
                    result = {'code': 200, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": myprice}
            else:
                # print('还没到出价格时机')
                pass

        if result['code'] == 200:
            #将成功的计入到数据库，并消除代拍任务
            #UPDATE Person SET Address = 'Zhongshan 23', City = 'Nanjing' WHERE LastName = 'Wilson'
            try:
                if myprice < 99:
                    myprice = myprice + 8
                sql = "UPDATE  offorlog SET goodsid = '{0}', officePrice = '{1}' , endtime = '{2}',status = 1 \
    WHERE id ='{3}'".format(goodsid, myprice, time.strftime("%Y-%m-%d", time.localtime()),offerlist[0][0] )
                self.cursor.execute(sql)
                # 执行sql语句
                self.myqllink.commit()
                usedno = offerlist[0][1]
                usedno =  usedno[:-4]
                print(usedno)
                self.redislink.lpop(usedno)
            except:
                # logging.error(traceback.format_exc())
                # self.errordata['setsqlerror'].append(data)
                print("拍卖存入失误")
                self.myqllink.rollback()
            print("拍卖成功")

        else:
            # UPDATE Person SET Address = 'Zhongshan 23', City = 'Nanjing' WHERE LastName = 'Wilson'
            # try:
            #     sql = "UPDATE  offorlog SET status = 0 WHERE id ='{0}'".format(offerlist[0][0])
            #     self.cursor.execute(sql)
            #     # 执行sql语句
            #     self.myqllink.commit()
            #
            # except:
            #     # logging.error(traceback.format_exc())
            #     # self.errordata['setsqlerror'].append(data)
            #     print("拍卖存入失误")
            #     self.myqllink.rollback()
            print("本次拍卖失败", result['code'])




    def biPrice(self, goodsid, myprice,theMaxprice):
        print("对价",myprice)
        goodsinfo = self.duobaoClass.goodsinfo(goodsid)
        if not goodsinfo:
            #没有信息
            print("没有信息")
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
            return [200, currentPrice]
        else :
            print("价格对比错误",currentPrice,myprice)
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
        print('根据usedno获取订单编号',usedno)
        if self.redislink.llen(usedno):
            sqlNo = self.redislink.lindex(usedno, 0)
            print('订单号',sqlNo)
            #验证订单状态，查看订单是否取消或完成
            offerlist = self.goodssend(sqlNo)

            print(offerlist)
            if offerlist:
                #更改订单状态添加3在抢购中
                # try:
                #     sql = "UPDATE  offorlog SET status = 3 WHERE id ='{0}'".format(offerlist[0][0])
                #     self.cursor.execute(sql)
                #     # 执行sql语句
                #     self.myqllink.commit()
                # except:
                #     print("订单状体没有改变")
                #     self.myqllink.rollback()

                print('拍卖订单号',sqlNo)
                # return sqlNo
                return offerlist
            else:
                print('删除订单',sqlNo)
                self.redislink.lpop(usedno)
                print('继续获取有用的订单')
                self.surestatus(usedno)
        else:
            print('没有列表为',usedno )
            return

    def goodssend(self, offerid):
        #查询订单
        sql = "SELECT id, usedNo, officePrice  FROM offorlog WHERE id = {0} AND status = 0".format(offerid)

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

    # def tets(self):
    #     sql = "UPDATE  offorlog SET goodsid = '{0}', officePrice = '{1}' , endtime = '{2}'  ,status = 1 \
    #     WHERE id = '{3}'".format(111, 111, time.strftime("%Y-%m-%d", time.localtime()), 1)
    #     self.cursor.execute(sql)
    #     # 执行sql语句
    #     self.myqllink.commit()
