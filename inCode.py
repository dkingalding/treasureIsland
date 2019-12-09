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
            if usecode == str("getgoods"):
                # 采集第二天可以买的所以商品
                self.allgoods.clearRedis()
                self.allgoods.getAllGoods()
            elif usecode == str("seach"):
                self.seachgoods()
            elif usecode == "3":
                #拍卖
                pass
            elif usecode == "4":
                continue
                pass
            elif usecode == "exit":
                #退出输入
                break
            else:
                coodusedNo = usecode.split('*')
                print(coodusedNo)
                if coodusedNo[0] == "exit":
                    print("aaaa")
                    break
                else:
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
        coodusedNo = inUsedNo.split('*')
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
            # while True:
            #     print("""
            #          请输入你想拍卖商品的usedNo和价格使用*隔开：
            #           1、退出exit """)
            #     thebb = input()
            #     coodusedNo = thebb.split('*')
            #     print(coodusedNo)
            #     if coodusedNo[0] == "exit":
            #         print("aaaa")
            #         break
            #     else:
            #         self.paimai(coodusedNo[0], coodusedNo[1])
        else:
            print("没有相关商品")

    def paimai(self, usedNo, price=99):
        #开始拍卖
        #拍卖的时候可以需要商品的usedNo 和价格
        #根据usedNo 获取商品的id 根据结束时间排序
        #查询最近时间商品的价格，如果高于规定价格就拍卖
        #查询自己出的价格是否有效，是否超过了自己定的价格
        #如果没有超过自己的定价就继续出价
        print("paimai")
        goodlist = self.allgoods.getGoodsid(usedNo)
        goodsinfo = self.duobaoClass.goodsinfo(goodlist[0][0])
        currentPrice = goodsinfo['data'][str(goodlist[0][0])]['currentPrice']
        print(currentPrice)
        myprice = 1
        if currentPrice >= float(price):
            print("已经超过限定价格")
            return
        elif currentPrice < float(myprice):
            print("已经超过我的价格")
            return
        else:
            youcookies = self.loginClass.getCookies()
            myprice = currentPrice + 3
            thecode = self.duobaoClass.sendPrice( youcookies, goodlist[0][0] ,myprice)
            # print(thecode)
            if thecode['code'] != 200:
                print(thecode)


