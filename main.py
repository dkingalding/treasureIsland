from Getgoods import getgoods
from login import loginCook
from taobao import duobao
from inCode import inCode
import time


if __name__ == '__main__':
    allgoods = getgoods()
    thecode = inCode(allgoods)
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
        print("""
        根据需要选择操作符：
        1、采集第二天可以买的所以商品
        2、查询商品
        3、拍卖
        4、返回上级          
        """)
        theinput = input()
        #需要对输入进行处理

<<<<<<< HEAD
        if theinput == str(1):
            # 采集第二天可以买的所以商品
=======
        if theinput == "getAllGoods":
            allgoods.clearRedis()
            allgoods.getAllGoods()
            # allgoods = getgoods()
>>>>>>> f4d0929c4a8f6e08ccd53a51ae0d7918b2f799dd
            # allgoods.seachGoods()
            # allgoods.gethistory(121175658)
            # print(allgoods.getUsedNo("k380"))
            # print(allgoods.getGoodsid("1000033031280901"))
            # print(allgoods.gethistory("121262553"))
<<<<<<< HEAD
=======
        elif theinput == "getUsedNo":
            # allgoods = getgoods()
            print(allgoods.getUsedNo("发泥"))
        elif theinput == "getAllGoods":
>>>>>>> f4d0929c4a8f6e08ccd53a51ae0d7918b2f799dd
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