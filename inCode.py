from Getgoods import getgoods
class inCode(object):
    def __init__(self,allgoods):
        # print("""
        # 根据需要选择操作符：
        # 1、输入商品信息或者商品号查看是是否有该商品和该商品信息
        # 2、
        # 3、拍卖该商品
        # 4、返回上级
        # """)
        self.allgoods = allgoods
        pass

    def trytest(self):
        print('测试')

    def seachgoods(self):
        goodinfo = set()
        while True:
            print("""
                请输入你想查询的商品或者usedNo：
                 """)
            inUsedNo = input()
            print(self.allgoods.getUsedNo(inUsedNo))
