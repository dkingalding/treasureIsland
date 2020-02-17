import time
from config import myredis
import redis
from config import mymysql
import pymysql
from taobao import duobao
from seachgoods import seachgoods
from mailtongzhi import dingmail

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


    def paimai(self, goodsid,offerlist , endtime, usedno):
        #开始拍卖
        #拍卖的时候可以需要商品的usedNo 和价格
        #根据usedNo 获取商品的id 根据结束时间排序
        #查询最近时间商品的价格，如果高于规定价格就拍卖
        #查询自己出的价格是否有效，是否超过了自己定的价格
        #如果没有超过自己的定价就继续出价
        #拍卖结束后，如果拍到了，待拍数量减一。如果没有拍到，计入下一个时间段的任务
        theMaxprice = round(float(offerlist[0][2]))
        myprice = 0
        result = {'code': 400, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": 0}
        while True:
            #计算时间
            firsttime = int(endtime) - round(time.time() * 1000)+100
            #获取数列使用
            stopprice = theMaxprice + 1
            if firsttime <= 1000:
                #获取此时的出价

                thestatus = self.biPrice(goodsid, myprice, theMaxprice)
                print(offerlist[0][0], thestatus)
                if thestatus[0] == 400:
                    #超过了价格
                    result = {'code':400, 'goodsid':goodsid, "usedNo":offerlist[0][1], "price":1 }
                    break
                elif thestatus[0] == 300:
                    #获取现在价格到自己最高价格之间的所有价格，组成列表
                    timeover = 0
                    startprice = thestatus[1]+1
                    result = {'code': 300, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": 1}
                    if startprice >= 93 and startprice <= 99:
                        startprice = 99
                    if startprice >= theMaxprice:
                        startprice = theMaxprice

                    while True:
                        if timeover ==1:
                            break
                        pricelist = range(startprice+3, stopprice, 3)
                        for i in pricelist:
                            if i >= 93 and i <= 99:
                                i = 99
                            bb = self.chujia(goodsid, i)
                            if bb == 200:
                                result = {'code': 200, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": i}
                                myprice = i
                                startprice = i
                                break
                            elif bb == 304:
                                #价格过低
                                startprice = i
                                if i == theMaxprice:
                                    result = {'code': 300, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": i}
                                    break
                            elif bb == 305:
                                timeover =1
                                # 时间已经结束
                                # result = {'code': 300, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": myprice}
                                break
                            else:
                                pass
                        if myprice == theMaxprice:
                            break
                elif thestatus[0] == 500 :
                    continue

                else:
                    # 记录拍卖状态
                    result = {'code': 200, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": myprice}
                if firsttime < 50:
                    print('超时',firsttime)
                    break
            else:
                continue
                # print('还没到出价格时机')
                pass

        if result['code'] == 200:

            self.saveorder( myprice, goodsid, offerlist, usedno)
        else:
            print("本次拍卖失败", result['code'])




    def paimaibaozhen(self, goodsid,offerlist , endtime, usedno):
        #最高价出价
        #防止漏拍
        #开主线程中为一个拍卖开启两个进程，一个正常拍卖，一个在最后提供最高价，防止漏拍
        theMaxprice = round(float(offerlist[0][2]))
        result = {'code': 400, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": 0}
        myprice = 0
        while True:
            #计算时间
            firsttime = int(endtime) - round(time.time() * 1000)+100
            if firsttime <= 300:
                #在这里开始出价
                bb = self.chujia(goodsid, theMaxprice)
                if bb == 200:
                    result = {'code': 200, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": theMaxprice}
                    myprice = theMaxprice
                    break
                elif bb == 304:
                    #出价过低
                    result = {'code': 300, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": theMaxprice}
                    break
                elif bb == 305:
                    # 时间已经结束
                    result = {'code': 300, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": theMaxprice}
                    break
                else:
                    #其他状态不改变状态
                    pass
                if firsttime < 50:
                    print('超时', firsttime)
                    break
        thestatus = self.biPrice(goodsid, myprice, theMaxprice)
        if thestatus[0] == 200:
            self.saveorder( myprice, goodsid, offerlist, usedno)
        else:
            print("本次拍卖失败", result['code'])


    def saveorder(self, myprice, goodsid, offerlist, usedno):
        # 将成功的计入到数据库，并消除代拍任务
        # UPDATE Person SET Address = 'Zhongshan 23', City = 'Nanjing' WHERE LastName = 'Wilson'
        try:
            if myprice < 99:
                myprice = myprice + 8
            sql = "UPDATE  offorlog SET goodsid = '{0}', officePrice = '{1}' , endtime = '{2}',status = 1 \
           WHERE id ='{3}'".format(goodsid, myprice, time.strftime("%Y-%m-%d", time.localtime()), offerlist[0][0])
            self.cursor.execute(sql)
            # 执行sql语句
            self.myqllink.commit()
            # usedno = offerlist[0][1]
            # usedno = usedno[:-4]
            print(usedno)
            self.redislink.lpop(usedno)
            titl = '%s订单拍卖成功，填写地址付钱' % offerlist[0][0]
            content = 'http://120.27.22.37/admin/offerlogs/%s/edit' % offerlist[0][0]
            mailclass = dingmail()
            mailclass.sendmail(titl, content)
        except:
            print("拍卖存入失误")
            self.myqllink.rollback()
        print("拍卖成功")
    

    def biPrice(self, goodsid, myprice,theMaxprice):
        # print("对价",myprice)
        goodsinfo = self.duobaoClass.goodsinfo(goodsid)
        if not goodsinfo:
            #没有信息
            # print("没有信息")
            return [500, myprice]
        # print(goodsinfo['data'])
        currentPrice = int(goodsinfo['data'][str(goodsid)]['currentPrice'])
        if currentPrice > int(theMaxprice):
            #返回通知结束进程，并取消着次竞拍
            print("已经超过限定价格")
            return [400, currentPrice]
        elif currentPrice > int(myprice):
            #继续出价
            # print("已经超过我出价格")
            return [300, currentPrice]
        elif currentPrice == int(myprice):
            #返回200，如果超过时间了，还是200，那就竞拍成功
            return [200, currentPrice]
        else :
            # print("价格对比错误",currentPrice,myprice)
            return [300, currentPrice]

    def chujia(self, goodsid, myprice):
        # print("在出价",myprice)
        thecode = self.duobaoClass.sendPrice(goodsid, myprice)
        if thecode['code'] != 200:
            # print(thecode)
            return thecode['code']
        else:
            # print("出价成功")
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
        offerlist = ''
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


                # return sqlNo
                return offerlist
            else:
                print('删除订单',sqlNo)
                self.redislink.lpop(usedno)
                print('继续获取有用的订单')
                self.surestatus(usedno)
        else:
            print('没有列表为',usedno )
            return offerlist

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
