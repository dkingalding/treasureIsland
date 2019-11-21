# import requests
# import os
# import re
# import time
# import json
# from userAgent import Agent
# from random import randint
# from lxml import etree
# from selenium import  webdriver

from Getgoods import getgoods
from login import loginCook

if __name__ == '__main__':
    # allgoods = getgoods()
    # allgoods.index()
    logintest = loginCook()
    thecookies = logintest.getCookies()
    # print(thecookies)
    # allgoods.setRedis('测试数据')
