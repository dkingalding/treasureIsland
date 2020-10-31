import requests,json,time
import re
import pymysql
import redis
from config import mymysql
from config import myredis
from config import Agent
from random import randint
import logging
import traceback

class getgoods(object):

    def __init__(self, conredis):
        #全部商品  "https://sell.paipai.com/auction-list?groupId=-1&entryid=p0120003dbdlogo"
        #https://used-api.jd.com/auction/list?pageNo=2&pageSize=50&category1=&status=&orderDirection=1&auctionType=1&orderType=1&callback=__jp116
        # https://used-api.paipai.com/auction/list?pageNo=1&pageSize=50&category1=&status=1&orderDirection=1&auctionType=1&orderType=1&groupId=1000005&callback=__jp35
        #电脑数码 groupId=1000005
        #食品饮料 groupId=1000442
        #珠宝配饰 groupId=1000009
        #品牌家电 groupId=1000004
        #运动户外 groupId=1000003
        #厨房用品 groupId=1000011
        #礼品箱包 groupId=1000010
        #母婴玩具 groupId=1000002
        #美妆个护 groupId=1000404
        #居家日用 groupId=1000007
        #服饰鞋靴 groupId=1000008
        #手机通讯 groupId=1000006
        #其它分类 groupId=1999999

        # self.list = (1000005,1000442,1000009,1000004,1000003,1000011,1000010,1000002,1000404,1000007,1000008,1000006,1999999)
        # self.list = (1000005,)
        # self.url = "https://used-api.jd.com/auction/list?pageNo=1&pageSize=50&category1=&status=&orderDirection=1&auctionType=1&orderType=2&callback=__jp116"
        self.headers = {
            # "Host": "used-api.jd.com",
            # "Host" : "used - api.paipai.com",
            # "Connection": "keep-alive",
            # "Referer": "https: // paipai.jd.com / auction - list",
            # "Connection": "close",
            "User-Agent":Agent[randint(0, 3)]['User-Agent'],
        }


        self.errordata = {'geterror':[],'setsqlerror':[]}
        self.redislink = redis.Redis(connection_pool = conredis)
        self.redispool = conredis
        # self.redislink = redis.Redis(host=myredis['host'], port=myredis['port'], decode_responses=True)
        self.myqllink = pymysql.connect(host=mymysql['host'], user=mymysql['user'], passwd=mymysql['passwd'], db=mymysql['db'])
        self.cursor = self.myqllink.cursor()
        logging.basicConfig(filename='log.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    def getAllGoods(self, groupId):
        #对外暴露方法
        #开始获取页面中的产品信息
        #对产品进行分类
        #页面中的分类
        #返回的数据格式
        #开始循环采集每个分类的数据
        print("开始采集数据")

        #开始采集每个分页中商品信息，判断是否成功的依据1、code 是否为200 和采集返回的数据中auctionInfos是否为空
        pageNo = 0
        bb = True
        onlyjindong = self.redislink.get("onlyjindong")
        # print(onlyjindong)
        while bb:
            print(pageNo)
            pageNo = pageNo + 1
            url = "https://used-api.paipai.com/auction/list?pageNo=%d&pageSize=50&fieldNo=30102&groupId=%s" % (
            pageNo, groupId)
            thedata = self.__getGoods(url)
            # print(groupId, pageNo)
            if thedata[0] == 444:
                # print("采集出现错误")
                self.errordata['geterror'].append(url)
                break
            if thedata[1] == None:
                bb = False
            else:
                #将数据存入数据库
                if isinstance(thedata[1], list):
                    # print("list")
                    for data1 in thedata[1]:
                        # print(data1)
                        self.__setdata(data1, onlyjindong)
                    time.sleep(2)
            time.sleep(1)
            if pageNo >= 300:
                pageNo = 0
                bb = False
        print(groupId,"采集结束")
        return 200

    # def test(self):
    #     #对外暴露方法
    #     #测试使用
    #     url = "https://used-api.paipai.com/auction/list?pageNo=1&pageSize=100&category1=&status=1&orderDirection=1&auctionType=1&orderType=1&groupId=1000005&callback=__jp35"
    #     thedata = self.__getGoods(url)
    #     print(thedata)
    #     if thedata[1] == None:
    #         bb = False
    #         print("已经完成采集")
    #     else:
    #         # 将数据存入数据库
    #         print('dddd')
    #         if isinstance(thedata[1], list):
    #             print("list")
    #             for data in thedata[1]:
    #                 self.__setdata(data)
    #                 time.sleep(1)

    def clearRedis(self):

        self.redislink.delete("goodslist")
        # self.redislink.delete("shop")
        # self.redislink.delete("usedName")
        sql = "TRUNCATE  goods"
        self.cursor.execute(sql)
        self.myqllink.commit()
        # sql = "TRUNCATE  shop"
        # self.cursor.execute(sql)
        # self.myqllink.commit()
        # sql = "TRUNCATE  usedName"
        # self.cursor.execute(sql)
        # self.myqllink.commit()



    def __getGoods(self,url):
        #获取每一个分页商品信息
        #基本方法
        try:
            r = requests.get(url,headers = self.headers)
            result_json = re.search(r'{.*}', r.text)
            result_dict = json.loads(result_json.group())
            # print(result_dict)
            # print(result_dict["data"]["auctionInfos"])
            # exit()
            if result_dict['code'] == 200:
                #将数据返回
                code = 200
                if result_dict["data"]["auctionInfos"]:
                    thedata = result_dict["data"]["auctionInfos"]
                else:
                    thedata = None
                return code, thedata
            else:
                #进入下一次循环或者在次查询
                code = False
                thedata = ''
                return code,thedata
            # raise Exception('发生异常错误信息')
        except:
            thedata = ''
            code = 444
            logging.error(traceback.format_exc())
            return code,thedata
        # print(result_dict)
        # print(tt["data"][])
        # print(tt["data"]["auctionInfos"][0])

    def __setdata(self,data, onlyjindong):
        #基本方法用于存储采集下来的数据
        keydata = ''
        valuedata = ''
        if isinstance(data, dict):
            #先查商品是否已经录入，可以使用redis集合
            # 如果商品没有录入就将商品存入到数据库和redis

            #去除数据中的None和单引号，能确保数据能存储进去
            #判断redis 连接是否可用
            try:
                self.redislink.ping()
            except:
                self.redislink = redis.Redis(connection_pool = self.redispool)
            for key in data.keys():
                if data[key] == None:
                    data[key] = 0
                data[key] = str(data[key])
                data[key] = data[key].replace('\'', '')

            #获取只收集备件库产品还是所有的产品都收集。如果只采集京东，当 usedNo 不等于0的时候返回

            if onlyjindong == '1':
                # print('只采集京东')
                # if data['shopId']!='0' and data['shopId']!='1000000127':
                    # print(data['shopId'])
                if data['shopId'] != '0':
                    temp = data['shopName'].encode('utf-8').decode('utf8')
                    find1 = u"(自营+)"
                    pattern = re.compile(find1)
                    results = pattern.findall(temp)
                    if not results:
                        return 0
            if self.redislink.sismember('usedName', data['usedNo']) == False:
                keydata = 'usedNo, productName, primaryPic, quality, shopId, size, brandId, shortProductName'
                valuedata = ("'{0}'" +","+"'{1}'" +","+"'{2}'" +","+"'{3}'" +","+"'{4}'" +","+"'{5}'" +","+"'{6}'" +","+"'{7}'" )\
                    .format(data['usedNo'],data['productName'],data['primaryPic'],data['quality'],data['shopId'],data['size'],data['brandId'],data['shortProductName'])
                # keydata = pymysql.escape_string(keydata)
                # valuedata = pymysql.escape_string(valuedata)
                sql = "INSERT INTO usedName ({0}) VALUES ({1})".format(keydata,valuedata)

                try:
                    self.myqllink.ping(reconnect=True)
                    self.cursor.execute(sql)
                    # 执行sql语句
                    self.myqllink.commit()
                    self.redislink.sadd('usedName', data['usedNo'])
                except:
                    # 发生错误时回滚

                    logging.error(traceback.format_exc())

                    self.errordata['setsqlerror'].append(data)
                    print("存品种错误")
                    self.myqllink.rollback()
                    self.redislink.srem('usedName', data['usedNo'])

            #查商店是否已经录入，没有如入的化将商店存入数据库
            if self.redislink.sismember('shop', data['shopId'])==False:
                keydata = 'shopId,shopName'
                valuedata = ("'{0}'" +","+"'{1}'"  )\
                    .format(data['shopId'],data['shopName'])
                sql = "INSERT INTO shop ({0}) VALUES ({1})".format(keydata,valuedata)
                try:
                    self.myqllink.ping(reconnect=True)
                    self.cursor.execute(sql)
                    # 执行sql语句
                    self.myqllink.commit()
                    self.redislink.sadd('shop', data['shopId'])
                except:
                    # 发生错误时回滚
                    self.errordata['setsqlerror'].append(data)
                    print("存储店铺错误")
                    self.myqllink.rollback()
                    self.redislink.srem('shop', data['shopId'])
                    logging.error(traceback.format_exc())
            #查商品号是否录入
            #如果没有如入就将商品写入数据库
            if self.redislink.sismember('goodslist', data['id'])==False:
                keydata = 'id, usedNo, startTime, endTime, cappedPrice, status, quality'
                valuedata = ("'{0}'" +","+"'{1}'" +","+"'{2}'" +","+"'{3}'" +","+"'{4}'" +","+"'{5}'" +","+"'{6}'")\
                    .format(data['id'],data['usedNo'],data['startTime'],data['endTime'],data['cappedPrice'],data['status'],data['quality'])
                sql = "INSERT INTO goods ({0}) VALUES ({1})".format(keydata,valuedata)
                try:
                    # 执行sql语句
                    self.myqllink.ping(reconnect=True)
                    self.cursor.execute(sql)
                    self.myqllink.commit()
                    self.redislink.sadd('goodslist', data['id'])
                except:
                    # 发生错误时回滚
                    self.errordata['setsqlerror'].append(data)
                    print("存储商品错误")
                    self.myqllink.rollback()
                    self.redislink.srem('goodslist', data['id'])
                    logging.error(traceback.format_exc())
        else:
            #返回数据，并对数据不做处理
            print('数据格式错误不是字典')

    def reorder(self):
        # 在重新采集完商品列表后重新载入抢购任务2
        keys = self.redislink.keys()
        auconttime = int(time.time()) * 1000
        for key in keys:
            # print(key)
            type = self.redislink.type(key)
            if type == 'list':
                # 订单都是以列表的形式存在，只要错作订单就可以了
                # vals = self.redislink.lrange(key, 0, -1)
                # print(vals)
                mapping = {}
                usedno = key[0:-1]
                unsedno = key[-1]

                #套餐如果需要修改只需要修改这里

                if unsedno == 'a':
                    condition = "usedNo = {0} OR usedNo = {1}".format(usedno + '0701', usedno + '0801')
                elif unsedno == 'b':
                    condition = "usedNo = {0}".format(usedno + '0901')
                elif unsedno == 'c':
                    condition ="usedNo = {0} OR usedNo = {1} OR usedNo = {2} OR usedNo = {3}".format(usedno+'3371', usedno + '0951', usedno + '0991', usedno + '0901')
                else:
                    condition = "usedNo = {0}".format(key)

                sql = "SELECT id, usedNo, endTime FROM goods  WHERE {0} AND endTime >= {1}".format(
                    condition, auconttime)
                try:
                    self.cursor.execute(sql)
                    # 执行sql语句
                    self.myqllink.commit()
                    results = self.cursor.fetchall()
                    if results:
                        for goodslist in results:

                            mapping[str(key) + "*" + str(goodslist[0])] = goodslist[2]
                            # print(goodslist[2])
                        self.redislink.zadd('treadlist', mapping=mapping)
                except:
                    # 发生错误时回滚
                    logging.error(traceback.format_exc())
                    print("查询商品 usedNo {0} 出错".format(key))
            else:
                pass


    def __del__(self):
        print(self.errordata)




