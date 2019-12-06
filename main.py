from Getgoods import getgoods
from login import loginCook
from taobao import duobao
from inCode import inCode
import time


if __name__ == '__main__':
    #将所有的类进行实例化，并传入到需要的类中
    loginClass = loginCook()
    allgoods = getgoods()
    duobaoClas = duobao()
    thecode = inCode(allgoods, duobaoClas, loginClass)
    thecode.startWork()
    #在主程序中只执行incode类的输入函数


    # while True:
    #     #根据输入选着执行什么操作
    #     print("""
    #     根据需要选择操作符：
    #     1、采集第二天可以买的所以商品
    #     2、查询商品
    #     3、拍卖
    #     4、返回上级
    #     """)
    #     # auconttime = int(time.time()) + 60
    #     # print(auconttime)
    #     theinput = input()
    #     #需要对输入进行处理
    #
    #
    #     if theinput == str(1):
    #         # 采集第二天可以买的所以商品
    #         allgoods.clearRedis()
    #         allgoods.getAllGoods()
    #     elif theinput == str(2):
    #         thecode.seachgoods()
    #         pass
    #     elif theinput == "3":
    #         #拍卖
    #         pass
    #     elif theinput == "4":
    #         continue
    #         pass
    #     elif theinput == "exit":
    #         #退出输入
    #         break
    #     else:
    #         continue