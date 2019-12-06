class inCode(object):
    #接受指令，并在本类中完成对其他基本类的调用，完成所有功能
    def __init__(self, allgoods, duobaoClass, loginClass):
        #将所有传入的实例都赋值给类内部
        #定义一个全局变量或者内部变量记录获取输入的内容
        self.allgoods = allgoods
        self.duobaoClass = duobaoClass
        self.loginClass = loginClass


    def startWork(self):
        print(
            """
                #     根据需要选择操作符：
                #     1、采集第二天可以买的所以商品
                #     2、查询商品
                #     3、拍卖
                #     4、返回上级
                #     """
        )



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
            if goodsinfo != None:
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

