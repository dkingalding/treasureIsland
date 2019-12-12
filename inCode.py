import time
class inCode(object):
    #接受指令，并在本类中完成对其他基本类的调用，完成所有功能
    def __init__(self, allgoods, duobaoClass, loginClass):
        #将所有传入的实例都赋值给类内部
        #定义一个全局变量或者内部变量记录获取输入的内容
        self.allgoods = allgoods
        self.duobaoClass = duobaoClass
        self.loginClass = loginClass


    def startWork(self):
        #记录输入的操作和产生的关键数字
        #根据操作提示不同的信息
        while True:
            print(
                """
                    #     根据需要选择操作符：
                    #     getgoods、采集第二天可以买的所以商品
                    #     seach、查询商品
                    #     请输入你想拍卖商品的usedNo和价格使用*隔开
                    #     exit、返回上级
                    #     """
            )
            codetime = int(time.time())
            print(codetime)
            usecode =input()
            usecode = usecode.replace(' ','')
            if usecode == str("getgoods"):
                # 采集第二天可以买的所以商品
                self.allgoods.clearRedis()
                self.allgoods.getAllGoods()
            elif usecode == str("seach"):
                self.seachgoods()
            elif usecode == "exit":
                #退出输入
                break
            else:
                #记得舒服卖出去的价格
                #最高出价会根据输入的价格的95%，保证最少有5%的收益
                usecode = usecode.replace(' ','')
                coodusedNo = usecode.split('*')
                if len(coodusedNo) <2:
                    print('请输入价格')
                    continue
                print(coodusedNo)
                self.paimai(coodusedNo[0], coodusedNo[1])



    def seachgoods(self):
        goodinfo = set()
        # while True:
        print("""
            请输入你想查询的商品或者usedNo：
            1、输入查所有店铺
            2、输入只查京东备件库
            3、退出
             """)
        inUsedNo = input()
        inUsedNo = inUsedNo.replace(' ', '')
        coodusedNo = inUsedNo.split('*')
        if len(coodusedNo)==1:
            coodusedNo.append(0)
        goodsinfo = self.allgoods.getUsedNo(coodusedNo[0],coodusedNo[1])
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

    def paimai(self, usedNo, price):
        #开始拍卖
        #拍卖的时候可以需要商品的usedNo 和价格
        #根据usedNo 获取商品的id 根据结束时间排序
        #查询最近时间商品的价格，如果高于规定价格就拍卖
        #查询自己出的价格是否有效，是否超过了自己定的价格
        #如果没有超过自己的定价就继续出价
        # print("paimai")
        goodlist = self.allgoods.getGoodsid(usedNo)
        theMaxprice = str(round(int(price) * 0.95))
        print(goodlist, theMaxprice)
        nowtime = round(time.time() * 1000)
        #需要那结束时间对比，在结束前一秒开始拍卖
        firsttime = int(goodlist[0][2]) - nowtime

        # if goodlist[0][1] > str(nowtime):
        #     print("拍卖还没有开始")
        #     return
        if firsttime <=1000 and firsttime > 0:
            #满足这个条件是才开始竞价
            # pass
            goodsinfo = self.duobaoClass.goodsinfo(goodlist[0][0])

            #采集到目前最高的价格
            currentPrice = goodsinfo['data'][str(goodlist[0][0])]['currentPrice']

            print(currentPrice)

            myprice = 1

            if currentPrice >= float(theMaxprice):
                print("已经超过限定价格")
                return
            elif currentPrice < float(myprice):
                print("已经超过我的价格")
                return
            else:
                # youcookies = self.loginClass.getCookies()
                myprice = currentPrice + 3
                if myprice >= 93 and myprice <= 99:
                    myprice = 99
                print(myprice)
                thecode = self.duobaoClass.sendPrice(goodlist[0][0] ,myprice)
                print(thecode)
                # if thecode['code'] != 200:
                #     print(thecode)


