from Getgoods import getgoods
from login import loginCook
from taobao import duobao
from inCode import inCode
<<<<<<< HEAD
import time
import re,json
=======

>>>>>>> dev


if __name__ == '__main__':
    #将所有的类进行实例化，并传入到需要的类中
    loginClass = loginCook()
    allgoods = getgoods()
<<<<<<< HEAD
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

=======
    duobaoClas = duobao()
    thecode = inCode(allgoods, duobaoClas, loginClass)
    # noll = 122328470
    # yy = duobaoClas.goodsinfo(noll)
    # print(yy['data'][str(noll)]['currentPrice'])
>>>>>>> dev

    # 122328470
    thecode.startWork()
    #在主程序中只执行in code类的输入函数
