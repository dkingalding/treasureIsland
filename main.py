from Getgoods import getgoods
from login import loginCook
from taobao import duobao
from inCode import inCode
from multiprocessing import Process
import threading, time




def shuru():
    loginClass = loginCook()
    allgoods = getgoods()
    duobaoClas = duobao()
    thecode = inCode(allgoods, duobaoClas, loginClass)
    thecode.startWork()

def shuchu():
    while True:
        print(111)
        time.sleep(10)

if __name__ == '__main__':

    #将所有的类进行实例化，并传入到需要的类中
    # loginClass = loginCook()
    # allgoods = getgoods()
    # duobaoClas = duobao()
    # thecode = inCode(allgoods, duobaoClas, loginClass)
    # thecode.startWork()

    # noll = 122328470
    # yy = duobaoClas.goodsinfo(noll)
    # print(yy['data'][str(noll)]['currentPrice'])

    # 122328470
    # thecode.startWork()
    #在主程序中只执行in code类的输入函数
    # p = Process(target=shuru )
    # p.start()
    # p.join()

    #需要任务队列，线程可以修改任务队列中的数据

    threads = []
    t = threading.Thread(target=shuru, name='LoopThread')
    threads.append(t)
    t2 = threading.Thread(target=shuchu, name='shuchu')
    threads.append(t2)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # t.start()
    # t.join()
    # t2.start()
    # t2.join()

    # while True:
    #     pass
