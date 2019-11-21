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

if __name__ == '__main__':
    allgoods = getgoods()
    allgoods.index()
    # allgoods.setRedis('测试数据')
