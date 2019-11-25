import requests
import json
from Getgoods import getgoods
from login import loginCook
from taobao import duobao


if __name__ == '__main__':
    allgoods = getgoods()
    #allgoods.clearRedis()
    allgoods.index()
    # myqllink = pymysql.connect(host='127.0.0.1', user='root', passwd='ding123', db='duobaodao')
    # logintest = loginCook()
    # thecookies = logintest.getCookies()
    # # print(thecookies)
    # current = duobao()
    # print(current.sendPrice(thecookies))

