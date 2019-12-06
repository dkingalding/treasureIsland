import re
class inCode(object):
    def __init__(self, allgoods, duobao):
        # print("""
        # 根据需要选择操作符：
        # 1、输入商品信息或者商品号查看是是否有该商品和该商品信息
        # 2、
        # 3、拍卖该商品
        # 4、返回上级
        # """)
        self.allgoods = allgoods
        self.duobao = duobao
        pass

    def trytest(self):
        print('测试')

    def seachgoods(self):
        goodinfo = set()
        while True:
            print("""
                请输入你想查询的商品或者usedNo：
                1、输入查所有店铺
                2、输入只查京东备件库
                3、退出
                 """)
            inUsedNo = input()
            if inUsedNo == "back":
                break
            else:
                goodsinfo = self.allgoods.getUsedNo(inUsedNo,0)
                if goodsinfo != None:
                    for value in goodsinfo:
                        goodsid = self.allgoods.getGoodsid(value[0])
                        if goodsid != None:
                            value = value + (self.allgoods.gethistory(goodsid[0][0]),)
                        print(value)
                    print("是否拍卖以上中的一个商品,请输入usedno 和价格 中间使用*隔开")
                    theUsedNo = input()
                    if theUsedNo != None:
                        result_json = re.split(r'\*', theUsedNo)
                        # print(result_json)
                        self.offerPrice(result_json[0], result_json[1])
                else:
                    print("没有相关商品")


    def offerPrice(self, theUsedNo, price):
        #根据usedNo查询活动goodid
        #price为最高价格,目前是自己输入,再往后可以是存入数据库
        #步骤 :1\根据usedNo 获取最近一段时间还可以拍卖的商品
               # 2\获取商品id 后获取目前的商品信息,查看当前的价格,和最高价对比,决定是否可以拍卖,如果不行就换下一时间段商品
               # 3如果可以拍卖就出价,并一直循环对比此商品出价是否高过来自己的出价,
               # 4\循环第二步
        if price == None:
            print("请输入价格")
        goodsid = self.allgoods.getGoodsid(theUsedNo)
        print(goodsid[0][0])
        nowPrice = self.duobao.goodsinfo(goodsid[0][0])

        print(nowPrice)
        # if nowPrice >= price:
        #     pass
        #       self.duobao.sendPrice()
# {'code': 200,
#  'data':
#      {'122159158':
#           {'auctionId': 122159158, 'auctionRecordId': 66705801, 'currentPrice': 101.0, 'num': 2, 'currentBidder': 'R***9', 'bidderNickName': 'R***9', 'bidderImage': None, 'status': None, 'offerPrice': None, 'actualEndTime': 1575612120000, 'delayCount': 0, 'virtualDelayCount': 0, 'spectatorCount': 183}
#       },
#  'list': [1575612027797], 'message': '查询成功'}
