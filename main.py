from Getgoods import getgoods
from login import loginCook
from taobao import duobao
from inCode import inCode
import time
import re,json


if __name__ == '__main__':
    allgoods = getgoods()
    chujia = duobao()
    thecode = inCode(allgoods, chujia)


    # allgoods.getUsedNo("米家(MIJIA)小米米家行车记录仪1S")
    # # allgoods.test()
    # # allgoods.clearRedis()
    # allgoods.index()
    # print(allgoods.gethistory(121973386))
    #
    # logintest = loginCook()
    # # logintest.longduomingdao()
    # thecookies = logintest.getCookies()
    #
    # # print(current.sendPrice(thecookies))
    # chujia.sendPrice(thecookies, 121953003, 1002)
    # print(chujia.goodsinfo(121973386))


    while True:
        #根据输入选着执行什么操作
        print("""
        根据需要选择操作符：
        1、采集第二天可以买的所以商品
        2、查询商品
        3、拍卖
        4、返回上级
        """)
        auconttime = int(time.time()) + 60
        print(auconttime)
        theinput = input()
        #需要对输入进行处理


        if theinput == str(1):
            # 采集第二天可以买的所以商品
            allgoods.clearRedis()
            allgoods.getAllGoods()
        elif theinput == str(2):
            thecode.seachgoods()
            pass
        elif theinput == "3":
            #拍卖
            pass
        elif theinput == "4":
            continue
            pass
        elif theinput == "exit":
            #退出输入
            break
        else:
            continue