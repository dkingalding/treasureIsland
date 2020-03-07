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
from mailtongzhi import dingmail

class huodan(object):

    def __init__(self, conredis):
        self.myqllink = pymysql.connect(host=mymysql['host'], user=mymysql['user'], passwd=mymysql['passwd'],
                                        db=mymysql['db'])
        self.cursor = self.myqllink.cursor()
        self.redislink = redis.Redis(connection_pool = conredis)
        # self.redispool = conredis
    #

    def getwords(self):
        #商品的关键词表  可以存入数据库， 也可以存入redis中
        #后台可以管理这些关键词， 一个关键词 生成一份货物清单

        sql = "SELECT keywords FROM qingdan"
        self.cursor.execute(sql)
        # 执行sql语句
        self.myqllink.commit()
        results = self.cursor.fetchall()
        return results



    def getlist(self, keyword):

        # 根据每天采集到的货物根据种类生成邮件发送到邮箱里
        # 货物的栓选条件：
        #     第一、必须有货，可以根据goods来填写
        #     第二、出价价格。出价价格为平均价格+5~10%，如果出价超过了 cappedPrice 就放弃
        #           如果平均价格为空，就取cappedPrice的85%
        #     第三、根据关键字，商品种类发送邮件。 邮件中显示商品名、价格、新旧程度
        #     第四、至采集9新以上的商品

        auconttime = int(time.time()) * 1000

        condition = "(a.quality = '9成新' OR a.quality = '95成新' OR a.quality = '准新品' OR a.quality = '99成新' OR a.quality = '全新')"
        cond = "b.productName LIKE '%{0}%'".format(keyword)

        # sql = "SELECT  a.usedNo, a.quality, a.cappedPrice, b.productName ,c.vagePrice FROM goods as a JOIN usedName as b ON b.usedNo = a.usedNo" \
        #       " JOIN theprice as c ON c.usedNo = a.usedNo WHERE  {1} AND a.endTime >= {2} AND {0}  GROUP BY a.usedNo".format(condition, cond, auconttime)

        sql = "SELECT  a.usedNo, a.quality, a.cappedPrice, b.productName ,c.vagePrice FROM goods as a JOIN usedName as b ON b.usedNo = a.usedNo" \
              " JOIN theprice as c ON c.usedNo = a.usedNo WHERE  {1} AND a.endTime >= {2} AND {0}  GROUP BY a.usedNo  ORDER BY  b.productName ".format(condition, cond, auconttime)

        self.cursor.execute(sql)

        self.myqllink.commit()
        results = self.cursor.fetchall()
        content = ''
        for goods in results:
            #如果有价格记录
            if self.redislink.sismember('kuchun', goods[0]) == False:
                ableprice = round(int(goods[2]) * 0.85)

                if goods[4]:
                    bb = int(goods[4])
                    if bb < 99:
                        bb = bb +7
                    myprice = round(int(bb) * 1.1)

                    #如果价格没有

                else:
                    myprice = round(goods[2] *0.85)
                if myprice <= ableprice:
                    content = content + "\r\n" + goods[3] + '----' + goods[1] + '----原价' + str(
                        goods[2]) + '----包邮价' + str(myprice)+ "\r\n"
                else:
                    print(goods, ableprice, myprice)
                self.redislink.sadd('kuchun', goods[0])

        # print(content)
        return content
        # if content:


    def shengchengliebieo(self):
        try:
            keywordlist = self.getwords()
            # print(keywordlist)
            mailcontent = ''
            self.redislink.delete('kuchun')
            self.redislink.sadd('kuchun', 0)
            for keyword in keywordlist:
                onecontent = self.getlist(keyword[0])
                # print(onecontent)
                mailcontent = mailcontent+ "\r\n" + keyword[0] + "===库存列表" + "\r\n" + onecontent
    
            titl = '库存清单'
            mailclass = dingmail()
            mailclass.sendmail(titl, mailcontent)
    
            self.redislink.delete('kuchun')


        except:
            print('chucuo')



