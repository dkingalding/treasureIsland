import requests
from urllib import request
import os
import time
from selenium import webdriver
basedir = os.path.abspath(os.path.dirname(__file__))

class loginCook(object):

    def __init__(self):
        #几个类属性定义
        self.loginUrl = "https://passport.jd.com/new/login.aspx?sso=1&ReturnUrl=https://sso.paipai.com/sso/redirect"
        # self.brower = webdriver.Chrome()

    def longduomingdao(self):
        #登录并保存cookies
        # print("ddd")
        # self.brower.get("https://paipai.jd.com/auction-list/")
        # time.sleep(2)
        brower = webdriver.Chrome()
        brower.get(self.loginUrl)
        time.sleep(20)
        if brower.current_url == 'https://www.paipai.com/':
            cookie = [item["name"] + "=" + item["value"] for item in brower.get_cookies()]
            cookiestr = ';'.join(item for item in cookie)
            with open(basedir + '/cookies.txt', 'w') as f:
                f.write(cookiestr)
        else:
            print("登录出现错误")
        brower.close()

    def getCookies(self):

        theCookies = ''
        try:
            with open(basedir + '/cookies.txt', 'r') as f:
                theCookies = f.readline()
        except:
            self.longduomingdao()
            with open(basedir + '/cookies.txt', 'r') as f:
                theCookies = f.readline()
        finally:
            return theCookies

