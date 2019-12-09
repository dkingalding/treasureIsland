from Getgoods import getgoods
from login import loginCook
from taobao import duobao
from inCode import inCode



if __name__ == '__main__':
    #将所有的类进行实例化，并传入到需要的类中
    loginClass = loginCook()
    allgoods = getgoods()
    duobaoClas = duobao()
    thecode = inCode(allgoods, duobaoClas, loginClass)
    # noll = 122328470
    # yy = duobaoClas.goodsinfo(noll)
    # print(yy['data'][str(noll)]['currentPrice'])

    # 122328470
    thecode.startWork()
    #在主程序中只执行in code类的输入函数
