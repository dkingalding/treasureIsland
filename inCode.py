import time
from config import myredis
import redis
from config import mymysql
import pymysql

class inCode(object):
    #接受指令，并在本类中完成对其他基本类的调用，完成所有功能
    #只接受命令操作
    #开启采集
    #查询商品
    #添加订单
    def __init__(self, allgoods):
        #将所有传入的实例都赋值给类内部
        #定义一个全局变量或者内部变量记录获取输入的内容
        self.allgoods = allgoods
        self.redislink = redis.Redis(host=myredis['host'], port=myredis['port'], decode_responses=True)
        self.myqllink = pymysql.connect(host=mymysql['host'], user=mymysql['user'], passwd=mymysql['passwd'], db=mymysql['db'])
        self.cursor = self.myqllink.cursor()

    def startWork(self):
        #记录输入的操作和产生的关键数字
        #根据操作提示不同的信息
        #需要进行多线程或者多进程
        #将获取所有数据的加入到任务队列
        #将商品拍卖的加入的任务队列
        print(
            """
                #     根据需要选择操作符：
                #     getgoods、采集第二天可以买的所以商品如果采集所有就加&1
                #     seach、查询商品使用&将要查询的商品分开
                #     请输入你想拍卖商品的usedNo和价格使用*隔开
                #     ding查看订单相关redis 
                #     dele删除待拍卖列表
             """
        )
        usecode =input()
        usecode = usecode.replace(' ', '')
        coodusedNo = usecode.split('&')
        if coodusedNo[0] == str("getgoods"):
            # 采集第二天可以买的所有商品
            #todo 选择添加是采集所有商品还是只采集数码电子类的商品
            caijistatus = self.redislink.get("getgoods")
            print(caijistatus)
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
        elif usecode == "ding":
            #查看订单相关的redis
            self.dinghis()
        elif usecode == "dele":
            #查看订单相关的redis
            self.deleoffer()
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

    def deleoffer(self):
        print("你确定要删除redis中订单么，确定输入yes否则输入no：")
        theinput = input()
        if theinput == "yes":
            keys = self.redislink.keys()
            for key in keys:
                # print(key)
                type = self.redislink.type(key)
                # if type == 'string':
                #     vals = self.redislink.get(key)
                if type == 'list':
                    print(key)
                    # vals = self.redislink.lrange(key, 0, -1)
                    self.redislink.delete(key)
                # elif type == 'set':
                #     vals = self.redislink.smembers(key);
                elif type == 'zset':
                    print(key)
                    self.redislink.delete(key)
                # elif type == "hash":
                #     vals = self.redislink.hgetall(key)
                else:
                    pass
        else:
            pass

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
        officePrice = int(price)*0.95
        usedno = unsedno[:-4]
        sql = "INSERT INTO offorlog (usedNo, xianyuprice,officePrice ,status ) VALUES ('{0}', '{1}',{2},0)".format(unsedno, price, officePrice)
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

        self.redislink.rpush(usedno, sqlid[0][0])
        #将所有拍卖时间记录到队列中
        #todo 存在逻辑错误，如果前一天的待拍卖商品还没有拍到，新一天的队列可能会为空
        #do 每一次增加都获取商品所有的可拍卖时间，并记录下来
        goodslist = self.allgoods.getGoodsid(usedno)
        mapping = {}
        if goodslist:
            print(goodslist)
            for key in goodslist:
                #将所有该商品的拍卖时间都记录到treadinfo中
                mapping[str(usedno)+"*"+ str(key[0])] = key[2]
                print(key[2])
            # treadscore = int(endTime)
            # treadinfo = unsedno+"*"+ goodsid
            self.redislink.zadd('treadlist', mapping = mapping)
            # self.allgoods.clearRedis()


    def seachgoods(self, unsedno,  shopid):
        goodsinfo = self.allgoods.getUsedNo(unsedno, shopid)

        if goodsinfo :
            for value in goodsinfo:
                # goodslist = self.allgoods.getGoodsid(value[0])
                # if goodslist:
                    # hisprice = self.allgoods.gethistory(goodslist[0][0])
                    # value = value + (hisprice, )
                print(value)
        else:
            print("没有相关商品")




    def dinghis(self):
        #删除订单了列表
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
            elif type == 'zset':
                print(key)
                vals = self.redislink.zrange(key, 0, -1)
                print(vals)
            else:
                pass
