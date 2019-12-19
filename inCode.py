import time
# from config import myredis
# import redis

class inCode(object):
    #接受指令，并在本类中完成对其他基本类的调用，完成所有功能
    def __init__(self, allgoods, duobaoClass, loginClass, redislink, myqllink):
        #将所有传入的实例都赋值给类内部
        #定义一个全局变量或者内部变量记录获取输入的内容
        self.allgoods = allgoods
        self.duobaoClass = duobaoClass
        self.loginClass = loginClass
        self.redislink = redislink
        self.myqllink = myqllink
        self.cursor = self.myqllink.cursor()


    # def startWork(self):
    #     #记录输入的操作和产生的关键数字
    #     #根据操作提示不同的信息
    #     #需要进行多线程或者多进程
    #     #将获取所有数据的加入到任务队列
    #     #将商品拍卖的加入的任务队列
    #     while True:
    #         print(
    #             """
    #                 #     根据需要选择操作符：
    #                 #     getgoods、采集第二天可以买的所以商品
    #                 #     seach、查询商品使用*将要查询的商品分开
    #                 #     请输入你想拍卖商品的usedNo和价格使用*隔开
    #                 #     exit、返回上级
    #                 #     """
    #         )
    #         usecode =input()
    #         usecode = usecode.replace(' ', '')
    #         coodusedNo = usecode.split('*')
    #         if coodusedNo[0] == str("getgoods"):
    #             # 采集第二天可以买的所有商品
    #             #todo 选择添加是采集所有商品还是只采集数码电子类的商品
    #             caijistatus = self.redislink.get("getgoods")
    #             if caijistatus != '0' and caijistatus != None:
    #                 print("已经在采集或者已发送采集命令")
    #             else:
    #                 self.redislink.getset("getgoods", 1)
    #         elif coodusedNo[0] == str("seach"):
    #             #查询商品就直接查询
    #             if len(coodusedNo) < 2:
    #                 print('请你要查询的商品')
    #                 continue
    #             elif len(coodusedNo) < 3:
    #                 coodusedNo.append(0)
    #             self.seachgoods(coodusedNo[1], coodusedNo[2])
    #         elif usecode == "exit":
    #             #退出输入
    #             break
    #         else:
    #             #记得输入卖出去的价格
    #             #最高出价会根据输入的价格的95%，保证最少有5%的收益
    #             #先确认下是否输入正确，
    #             #将要拍卖的商品记录到队列中
    #             #根据时间设置成key存入redis中任务队列
    #             if len(coodusedNo) <2:
    #                 print('请输入价格')
    #                 continue
    #             thestatus = self.sureGood(coodusedNo[0])
    #             if thestatus == 1:
    #                 # print("确定购买")
    #                 self.addgoodsjob(coodusedNo[0], coodusedNo[1])
    #             else :
    #                 continue

    def startWork(self):
        #记录输入的操作和产生的关键数字
        #根据操作提示不同的信息
        #需要进行多线程或者多进程
        #将获取所有数据的加入到任务队列
        #将商品拍卖的加入的任务队列
        print(
            """
                #     根据需要选择操作符：
                #     getgoods、采集第二天可以买的所以商品
                #     seach、查询商品使用*将要查询的商品分开
                #     请输入你想拍卖商品的usedNo和价格使用*隔开
                #     exit、返回上级
                #     """
        )
        usecode =input()
        usecode = usecode.replace(' ', '')
        coodusedNo = usecode.split('*')
        if coodusedNo[0] == str("getgoods"):
            # 采集第二天可以买的所有商品
            #todo 选择添加是采集所有商品还是只采集数码电子类的商品
            caijistatus = self.redislink.get("getgoods")
            if caijistatus != '0' and caijistatus != None:
                print("已经在采集或者已发送采集命令")
            else:
                self.redislink.getset("getgoods", 1)
        elif coodusedNo[0] == str("seach"):
            #查询商品就直接查询
            if len(coodusedNo) < 2:
                print('请你要查询的商品')
            elif len(coodusedNo) < 3:
                coodusedNo.append(0)
            self.seachgoods(coodusedNo[1], coodusedNo[2])
        elif usecode == "exit":
            #退出输入
            self.allgoods.clearRedis()

        else:
            #记得输入卖出去的价格
            #最高出价会根据输入的价格的95%，保证最少有5%的收益
            #先确认下是否输入正确，
            #将要拍卖的商品记录到队列中
            #根据时间设置成key存入redis中任务队列
            if len(coodusedNo) <2:
                print('请输入价格')
                return
            thestatus = self.sureGood(coodusedNo[0])
            if thestatus == 1:
                # print("确定购买")
                self.addgoodsjob(coodusedNo[0], coodusedNo[1])
            else :
                # continue
               return

    def sureGood(self, unsedno):
        #todo 需要提示还剩余多少，还有待拍多少，选择是在这里显示还是在seach中显示
        goodsinfo = self.allgoods.getGoodInfo(unsedno)
        # print(goodsinfo)
        print("你是要拍卖---{0}---{1}确定请输入yes否则输入no".format(goodsinfo[0][3], goodsinfo[0][1]))
        surestatus =input()
        usecode = surestatus.replace(' ', '')
        if usecode == "yes":
            return 1
        else:
            return 0


    def addgoodsjob(self, unsedno, price):

        #将需要拍卖商品的信息存入数据库
        #统计同一商品待拍卖的数量
        #记录商品的拍卖时间记录到redis的有序集合中
        #todo 是否需要验证剩余拍卖量和待拍卖量

        sql = "INSERT INTO offorlog (usedNo, xianyuprice ) VALUES ('{0}', '{1}')".format(unsedno, price)
        getid ="select max(id) from offorlog"
        try:
            self.cursor.execute(sql)
            # 执行sql语句
            self.myqllink.commit()
            self.cursor.execute(getid)
            # 执行sql语句
            self.myqllink.commit()
            sqlid = self.cursor.fetchall()
            # print(sqlid)
        except:
            # 发生错误时回滚1000033031280901
            print("拍卖录入出错")
            self.myqllink.rollback()
            return

        self.redislink.rpush(unsedno, sqlid[0][0])
        #将所有拍卖时间记录到队列中
        #todo 存在逻辑错误，如果前一天的待拍卖商品还没有拍到，新一天的队列可能会为空
        #do 每一次增加都获取商品所有的可拍卖时间，并记录下来

        goodslist = self.allgoods.getGoodsid(unsedno)
        mapping = {}
        if goodslist:
            print(goodslist)
            for key in goodslist:
                #将所有该商品的拍卖时间都记录到treadinfo中
                mapping[str(unsedno)+"*"+ str(key[0])] = key[2]
                print(key[2])
            # treadscore = int(endTime)
            # treadinfo = unsedno+"*"+ goodsid
            self.redislink.zadd('treadlist', mapping = mapping)
            # self.allgoods.clearRedis()


    def seachgoods(self, unsedno,  shopid):
        goodsinfo = self.allgoods.getUsedNo(unsedno, shopid)

        if goodsinfo :
            for value in goodsinfo:
                goodslist = self.allgoods.getGoodsid(value[0])
                # print(value)
                # print(goodslist)
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
        offerlist = self.allgoods.goodssend(sqlNo)
        if not offerlist:
            print("没有本次拍卖")
            return

        theMaxprice = round(int(offerlist[0][2]) * 0.95)

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
            myprice = 1
            result = {'code': 400, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": 0}
            # while firsttime <=1000 and firsttime > -500 and iscontend:
            while firsttime > 0 and iscontend:
                thestatus = self.biPrice(goodsid, myprice, theMaxprice)
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

                        #如果出价成功，记录出价记录
                    else:
                        result = {'code': 300, 'goodsid': goodsid, "usedNo":offerlist[0][1], "price": 1}
                        # myprice = 1
                        # 如果出价失败，不记录出价记录
                else:
                    #记录拍卖状态
                    result = {'code': 200, 'goodsid': goodsid, "usedNo": offerlist[0][1], "price": myprice}

            if result['code'] == 200:
                #将成功的计入到数据库，并消除代拍任务
                #UPDATE Person SET Address = 'Zhongshan 23', City = 'Nanjing' WHERE LastName = 'Wilson'
                try:
                    sql = "UPDATE  offerlog SET goodsid = '{0}', officePrice = '{1}' WHERE id = '{2}'".format(goodsid, myprice, sqlNo)
                    self.cursor.execute(sql)
                    # 执行sql语句
                    self.myqllink.commit()
                    self.redislink.lpop(offerlist[0][1])
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
        if currentPrice >= int(theMaxprice):
            #返回通知结束进程，并取消着次竞拍
            print("已经超过限定价格")
            return [400, currentPrice]
        elif currentPrice > int(myprice):
            #继续出价
            print("已经超过我出价格")
            return [300, currentPrice]
        else:
            #返回200，如果超过时间了，还是200，那就竞拍成功
            #在拍卖的主程序中将拍卖删除，代拍数列中也删除一个任务
            return [200, currentPrice]

    def chujia(self, goodsid, myprice):
        print("在出价")
        thecode = self.duobaoClass.sendPrice(goodsid, myprice)
        if thecode['code'] != 200:
            print(thecode)
            return 444
        else:
            print("出价成功")
            return 200


