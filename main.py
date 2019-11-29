import requests
import json
from Getgoods import getgoods
from login import loginCook
from taobao import duobao


if __name__ == '__main__':
    allgoods = getgoods()
    # allgoods.getUsedNo("米家(MIJIA)小米米家行车记录仪1S")
    # # allgoods.test()
    # # allgoods.clearRedis()
    # allgoods.index()
    # allgoods.gethistory(121175658)

    # logintest = loginCook()
    # thecookies = logintest.getCookies()
    # # print(thecookies)
    # current = duobao()
    # print(current.sendPrice(thecookies))

    while True:
        #根据输入选着执行什么操作
        theinput = input()
        #需要对输入进行处理

        if theinput == "getAllGoods":
            allgoods.clearRedis()
            allgoods.getAllGoods()
            # allgoods = getgoods()
            # allgoods.seachGoods()
            # allgoods.gethistory(121175658)
            # print(allgoods.getUsedNo("k380"))
            # print(allgoods.getGoodsid("1000033031280901"))
            # print(allgoods.gethistory("121262553"))
        elif theinput == "getUsedNo":
            # allgoods = getgoods()
            print(allgoods.getUsedNo("发泥"))
        elif theinput == "getAllGoods":
            allgoods.getAllGoods()
        elif theinput == "exit":
            break