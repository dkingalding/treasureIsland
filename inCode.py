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
                    #     paimai、拍卖
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
                continue



    def seachgoods(self):
        goodinfo = set()
        while True:
            print("""
                请输入你想查询的商品或者usedNo：
                1、输入差所有店铺
                2、输入只差京东备件库
                3、退出
                 """)
            inUsedNo = input()
            goodsinfo = self.allgoods.getUsedNo(inUsedNo,1)
            if goodsinfo :
                for value in goodsinfo:
                    print(value)
            else:
                print("没有相关商品")
            # if inUsedNo == str(""):
            #     goodsinfo = self.allgoods.getUsedNo(inUsedNo)
            #     if goodsinfo != None:
            #         for value in goodsinfo:
            #             print(value)
            # elif inUsedNo == str(""):
            #     pass
            # else:
            #     pass

