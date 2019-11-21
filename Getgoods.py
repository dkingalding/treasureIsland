import requests,json
import pymysql

class getgoods(object):


    def __init__(self):
        #全部商品  "https://sell.paipai.com/auction-list?groupId=-1&entryid=p0120003dbdlogo"
        #https://used-api.jd.com/auction/list?pageNo=2&pageSize=50&category1=&status=&orderDirection=1&auctionType=1&orderType=1&callback=__jp116
        #电脑数码 https://sell.paipai.com/auction-list?groupId=1000005&entryid=p0120003dbdlogo
        #食品饮料 https://sell.paipai.com/auction-list?groupId=1000442&entryid=p0120003dbdlogo
        #珠宝配饰 https://sell.paipai.com/auction-list?groupId=1000009&entryid=p0120003dbdlogo
        #品牌家电 https://sell.paipai.com/auction-list?groupId=1000004&entryid=p0120003dbdlogo
        #运动户外 https://sell.paipai.com/auction-list?groupId=1000003&entryid=p0120003dbdlogo
        #厨房用品 https://sell.paipai.com/auction-list?groupId=1000011&entryid=p0120003dbdlogo
        #礼品箱包 https://sell.paipai.com/auction-list?groupId=1000010&entryid=p0120003dbdlogo
        #母婴玩具 https://sell.paipai.com/auction-list?groupId=1000002&entryid=p0120003dbdlogo
        #美妆个护 https://sell.paipai.com/auction-list?groupId=1000404&entryid=p0120003dbdlogo
        #居家日用 https://sell.paipai.com/auction-list?groupId=1000007&entryid=p0120003dbdlogo
        #服饰鞋靴 https://sell.paipai.com/auction-list?groupId=1000008&entryid=p0120003dbdlogo
        #手机通讯 https://sell.paipai.com/auction-list?groupId=1000006&entryid=p0120003dbdlogo
        #其它分类 https://sell.paipai.com/auction-list?groupId=1999999&entryid=p0120003dbdlogo
        self.url = "https://used-api.jd.com/auction/list?pageNo=200&pageSize=50&category1=&status=&orderDirection=1&auctionType=1&orderType=2"
        self.headers = {
            "Host": "used-api.jd.com",
            "Connection": "keep-alive",
            "Referer": "https: // paipai.jd.com / auction - list",
            # "Connection": "close",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        }
        # self.redisLink = redis.Redis(host='127.0.0.1', port=6379, password='')

    def index(self):
        #开始获取页面中的产品信息
        #对产品进行分类
        #页面中的分类
        #返回的数据格式
        #{'code': 200,
        # 'data':
        #   {'category1List': [{'code': 13765, 'name': None}, {'code': 12259, 'name': None}, {'code': 6144, 'name': None}, {'code': 1320, 'name': None}, {'code': 670, 'name': None}, {'code': 6233, 'name': None}, {'code': 737, 'name': None}, {'code': 1316, 'name': None}, {'code': 1315, 'name': None}, {'code': 1672, 'name': None}, {'code': 652, 'name': None}, {'code': 1318, 'name': None}, {'code': 15248, 'name': None}, {'code': 1319, 'name': None}, {'code': 9192, 'name': None}, {'code': 9855, 'name': None}, {'code': 15901, 'name': None}, {'code': 6196, 'name': None}, {'code': 16750, 'name': None}, {'code': 12218, 'name': None}, {'code': 5025, 'name': None}, {'code': 9987, 'name': None}, {'code': 11729, 'name': None}, {'code': 1620, 'name': None}, {'code': 6728, 'name': None}, {'code': 17329, 'name': None}, {'code': 9847, 'name': None}, {'code': 6994, 'name': None}],
        #    'categoryGroupList': [{'id': 10, 'categoryId': 1000005, 'categoryName': '电脑数码', 'superId': 0, 'sortNum': 0, 'slogan': '数码办公', 'imageUrl': 'jfs/t1/53695/24/347/7489/5cd45c32E9bb1f5e0/44bc771e01882298.png', 'groupStatus': 1, 'creator': None, 'createAt': None, 'modifier': None, 'modifyAt': None, 'categoryType': 0}, {'id': 172, 'categoryId': 1000442, 'categoryName': '食品饮料', 'superId': 0, 'sortNum': 2, 'slogan': '食品饮料', 'imageUrl': 'jfs/t1/47922/3/294/5456/5cd42be5Eca5fb1d4/f357085413fc2d8a.png', 'groupStatus': 1, 'creator': None, 'createAt': None, 'modifier': None, 'modifyAt': None, 'categoryType': 0}, {'id': 112, 'categoryId': 1000009, 'categoryName': '珠宝配饰', 'superId': 0, 'sortNum': 2, 'slogan': '珠宝配饰', 'imageUrl': 'jfs/t1/33636/21/11721/8712/5cd46116E68cba5a8/605966c0bf438794.png', 'groupStatus': 1, 'creator': None, 'createAt': None, 'modifier': None, 'modifyAt': None, 'categoryType': 0}, {'id': 8, 'categoryId': 1000004, 'categoryName': '品牌家电', 'superId': 0, 'sortNum': 2, 'slogan': '品牌家电', 'imageUrl': 'jfs/t1/56785/7/358/7331/5cd45f84E774f5f7f/9c49a51876350b13.png', 'groupStatus': 1, 'creator': None, 'createAt': None, 'modifier': None, 'modifyAt': None, 'categoryType': 0}, {'id': 6, 'categoryId': 1000003, 'categoryName': '运动户外', 'superId': 0, 'sortNum': 3, 'slogan': '户外', 'imageUrl': 'jfs/t1/53777/13/311/9364/5cd460a8E7d770cf7/5e92299844b7642e.png', 'groupStatus': 1, 'creator': None, 'createAt': None, 'modifier': None, 'modifyAt': None, 'categoryType': 0}, {'id': 416, 'categoryId': 1000011, 'categoryName': '厨房用品', 'superId': 0, 'sortNum': 4, 'slogan': '厨房用品', 'imageUrl': 'jfs/t1/68134/2/8321/8870/5d635220E53687b61/40830231fed39686.png', 'groupStatus': 1, 'creator': None, 'createAt': None, 'modifier': None, 'modifyAt': None, 'categoryType': 0}, {'id': 344, 'categoryId': 1000010, 'categoryName': '礼品箱包', 'superId': 0, 'sortNum': 5, 'slogan': '大牌箱包，品质配饰', 'imageUrl': 'jfs/t26347/283/2633642708/7180/13c6ef7c/5cd64c2cNc3c5d265.png', 'groupStatus': 1, 'creator': None, 'createAt': None, 'modifier': None, 'modifyAt': None, 'categoryType': None}, {'id': 3, 'categoryId': 1000002, 'categoryName': '母婴玩具', 'superId': 0, 'sortNum': 6, 'slogan': '母婴用品', 'imageUrl': 'jfs/t1/43430/26/4527/8977/5cd45f0dEc173c0ac/e23267bd9175d1d8.png', 'groupStatus': 1, 'creator': None, 'createAt': None, 'modifier': None, 'modifyAt': None, 'categoryType': 0}, {'id': 368, 'categoryId': 1000109, 'categoryName': '中外名酒', 'superId': 0, 'sortNum': 7, 'slogan': '夺宝岛酒类', 'imageUrl': 'jfs/t1/69775/2/8206/5456/5d63527dEe99baabc/613cc2ae9eaf63f0.png', 'groupStatus': 1, 'creator': None, 'createAt': None, 'modifier': None, 'modifyAt': None, 'categoryType': 0}, {'id': 167, 'categoryId': 1000404, 'categoryName': '美妆个护', 'superId': 0, 'sortNum': 8, 'slogan': '美妆个护', 'imageUrl': 'jfs/t1/52395/7/326/7520/5cd42c95E9cb492ee/6af04466679e700b.png', 'groupStatus': 1, 'creator': None, 'createAt': None, 'modifier': None, 'modifyAt': None, 'categoryType': 0}, {'id': 54, 'categoryId': 1000007, 'categoryName': '居家日用', 'superId': 0, 'sortNum': 9, 'slogan': '家居日用', 'imageUrl': 'jfs/t1/59067/20/248/6398/5cd45da2E948928ce/e8e5c63cf3531270.png', 'groupStatus': 1, 'creator': None, 'createAt': None, 'modifier': None, 'modifyAt': None, 'categoryType': 0}, {'id': 71, 'categoryId': 1000008, 'categoryName': '服饰鞋靴', 'superId': 0, 'sortNum': 10, 'slogan': '服饰家居', 'imageUrl': 'jfs/t1/51775/19/316/6887/5cd45cbaEa2e869fe/2c67c9ec05a9268a.png', 'groupStatus': 1, 'creator': None, 'createAt': None, 'modifier': None, 'modifyAt': None, 'categoryType': 0}, {'id': 49, 'categoryId': 1000006, 'categoryName': '手机通讯', 'superId': 0, 'sortNum': 11, 'slogan': '手机通讯', 'imageUrl': 'jfs/t1/40772/39/4542/5718/5cd46027Ea82190b5/79eaf3d3808870b9.png', 'groupStatus': 1, 'creator': None, 'createAt': None, 'modifier': None, 'modifyAt': None, 'categoryType': 0}, {'id': 14, 'categoryId': 1999999, 'categoryName': '其它分类', 'superId': 0, 'sortNum': 9999, 'slogan': '超值商品，尽在其中', 'imageUrl': 'jfs/t1/48157/3/322/10884/5cd45fe8E903c7d36/e8b294e79b271718.png', 'groupStatus': 1, 'creator': None, 'createAt': None, 'modifier': None, 'modifyAt': None, 'categoryType': 0}],
        #    'qualityList': ['全新', '9成新', '7成新', '99成新', '准新品', '99新', '95成新', '8成新', '官翻；95成新', '95新', '官翻', '准新品；官翻', '租赁商品', '官翻；9成新', '二手99新', '二手95新', '准新品；8成新', '内10'],
        #    'brandList': ['阿玛尼（ARMANI）', '飞利浦（PHILIPS）', '小米（MI）', 'VAKADA', '贝恩施', '北极绒（Bejirog）', '巴布瑞', '枝江', '沃德雷（VODREY XO）', '大象', '施华洛世奇（SWAROVSKI）', '卡豪朗（KAHAOLANG）', '米家（MIJIA）', 'APPLE苹果', '格雅（GEYA）', '胡汉和亲（HHHQ）', '其他'],
        #    'selectedCategory1': None, 'selectedCategoryGroupId': None, 'selectedStatus': None, 'selectedQuality': None, 'selectedQualityList': None, 'selectedBrand': None, 'selectedOtherBrand': None, 'totalNumber': 32447, 'hasNext': True, '
        #    auctionInfos': [
        #       {'id': 120622290, 'usedNo': 11931134309, 'productName': '天然白玉手镯女款【赠国检证书 假一赔百】乳白款送礼佳品 送鉴定证书 代写贺卡 62-63适合120-130斤', 'startTime': 1574148439000, 'endTime': 1574151139000, 'startPrice': 1.0, 'minPrice': 1.0, 'maxPrice': 400.0, 'cappedPrice': 520.0, 'category1': 6144, 'category1Name': '珠宝首饰', 'category2': 19934, 'category2Name': '其它玉石', 'category3': 19948, 'category3Name': '其它玉石', 'primaryPic': 'jfs/t1/59264/13/14452/96685/5dc3c0ffEa5747194/8b95728c98caec03.jpg', 'currentPrice': 98.0, 'recordCount': 1, 'bidder': 'j***8', 'status': 2, 'quality': '全新', 'spectatorCount': 48, 'reminding': 0, 'shopId': 648389, 'shopName': '玉有情珠宝首饰官方旗舰店', 'productType': 6, 'size': None, 'brandId': 233826, 'brandName': '玉有情', 'auctionType': 1, 'actualEndTime': 1574151139000, 'delayCount': None, 'shortProductName': '天然白玉手镯女款赠国检证书 假一赔百乳白款送礼佳品 送鉴定证书 代写贺卡 62-63适合120-130斤', 'hasSameAuctions': False},
        #       {'id': 120657485, 'usedNo': 59625810672, 'productName': '2457630收纳博士真空压缩袋收纳袋衣物真空打包整理袋16件套送电泵 收纳博士', 'startTime': 1574148440000, 'endTime': 1574151140000, 'startPrice': 1.0, 'minPrice': 1.0, 'maxPrice': 90.0, 'cappedPrice': 90.0, 'category1': 1672, 'category1Name': '礼品', 'category2': 2599, 'category2Name': '礼品', 'category3': 5266, 'category3Name': '礼品', 'primaryPic': 'jfs/t1/44967/33/13756/165916/5dabfec6E03293ed5/3f91dff46677ede5.jpg', 'currentPrice': 38.0, 'recordCount': 10, 'bidder': '1***p', 'status': 2, 'quality': '全新', 'spectatorCount': 51, 'reminding': 0, 'shopId': 10230987, 'shopName': '逸欣德礼品专营店', 'productType': 6, 'size': None, 'brandId': 400367, 'brandName': 'VAKADA', 'auctionType': 1, 'actualEndTime': 1574151140000, 'delayCount': None, 'shortProductName': '2457630收纳博士真空压缩袋收纳袋衣物真空打包整理袋16件套送电泵 收纳博士', 'hasSameAuctions': False},
        #       {'id': 120669092, 'usedNo': 61591798339, 'productName': '4档调温德国谷格（GUGE）饮水机 家用迷你小型台式家用免安装秒速加热G78A假一赔三', 'startTime': 1574148440000, 'endTime': 1574151140000, 'startPrice': 1.0, 'minPrice': 1.0, 'maxPrice': 600.0, 'cappedPrice': 1299.0, 'category1': 13765, 'category1Name': '二手商品', 'category2': 17170, 'category2Name': '二手邮票', 'category3': 17184, 'category3Name': '二手邮票', 'primaryPic': 'jfs/t1/100379/17/2278/186985/5dccf7e4Ef2dca535/bc20d27afc6ae49d.jpg', 'currentPrice': 609.0, 'recordCount': 12, 'bidder': 'j***4', 'status': 2, 'quality': None, 'spectatorCount': 73, 'reminding': 0, 'shopId': 760699, 'shopName': '优品折扣专营店', 'productType': 3, 'size': None, 'brandId': 23231, 'brandName': 'APPLE苹果', 'auctionType': 1, 'actualEndTime': 1574151140000, 'delayCount': None, 'shortProductName': '4档调温德国谷格饮水机 家用迷你小型台式家用免安装秒速加热G78A假一赔三', 'hasSameAuctions': False},
        #       {'id': 120622291, 'usedNo': 11286083650, 'productName': '天然正品巴西红玛瑙玉手镯女款【赠国检证书 假一赔百】送妈妈女友情人礼物 送鉴定证书代写贺卡 60-61', 'startTime': 1574148441000, 'endTime': 1574151141000, 'startPrice': 1.0, 'minPrice': 1.0, 'maxPrice': 400.0, 'cappedPrice': 520.0, 'category1': 6144, 'category1Name': '珠宝首饰', 'category2': 19934, 'category2Name': '其它玉石', 'category3': 19948, 'category3Name': '其它玉石', 'primaryPic': 'jfs/t6328/293/1572099024/79265/ae63b4f6/595327c2N1b5a6b99.jpg', 'currentPrice': 164.0, 'recordCount': 1, 'bidder': 'j***8', 'status': 2, 'quality': '全新', 'spectatorCount': 55, 'reminding': 0, 'shopId': 648389, 'shopName': '玉有情珠宝首饰官方旗舰店', 'productType': 6, 'size': None, 'brandId': 233826, 'brandName': '玉有情', 'auctionType': 1, 'actualEndTime': 1574151141000, 'delayCount': None, 'shortProductName': '天然正品巴西红玛瑙玉手镯女款赠国检证书 假一赔百送妈妈女友情人礼物 送鉴定证书代写贺卡 60-61', 'hasSameAuctions': False},
        #       {'id': 120669093, 'usedNo': 61591814279, 'productName': '德国谷格（GUGE）饮水机台面即热直饮机家用办公小型免安装加热一体G78B假一赔三 白色', 'startTime': 1574148442000, 'endTime': 1574151142000, 'startPrice': 1.0, 'minPrice': 1.0, 'maxPrice': 600.0, 'cappedPrice': 1580.0, 'category1': 13765, 'category1Name': '二手商品', 'category2': 17170, 'category2Name': '二手邮票', 'category3': 17184, 'category3Name': '二手邮票', 'primaryPic': 'jfs/t1/91344/19/2250/183678/5dccef66E982187af/cb3a8b3b1b05d6f6.jpg', 'currentPrice': 759.0, 'recordCount': 12, 'bidder': 'j***4', 'status': 2, 'quality': None, 'spectatorCount': 73, 'reminding': 0, 'shopId': 760699, 'shopName': '优品折扣专营店', 'productType': 3, 'size': None, 'brandId': 23231, 'brandName': 'APPLE苹果', 'auctionType': 1, 'actualEndTime': 1574151142000, 'delayCount': None, 'shortProductName': '德国谷格饮水机台面即热直饮机家用办公小型免安装加热一体G78B假一赔三 白色', 'hasSameAuctions': False}
        #       ],
        #       'systemTime': 1574151135790,
        #       'newerFieldInfo': None,
        #       'newerFirstAccess': False,
        #       'jdBeanFieldInfo': None,
        #       'plusFieldInfo': None,
        #       'fieldResourceConfig': None,
        #       'fieldName': None}, 'list': None, 'message': '查询成功'}

        r = requests.Session()
        r = requests.get(self.url,headers = self.headers)
        # print(r.text)
        tt =json.loads(r.text)
        # print(tt["data"][])
        # print(tt["data"]["auctionInfos"][0])



# {'id': 120688564,
#  'usedNo': 57782915323,
#  'productName': '三星（SAMSUNG)玄龙MR+ VR眼镜体感游戏机 智能3D头盔 3D体感手柄套装VR设备',
#  'startTime': 1574177264000,
#  'endTime': 1574179964000,
#  'startPrice': 1.0,
#  'minPrice': 1.0,
#  'maxPrice': 1000.0,
#  'cappedPrice': 3999.0,
#  'category1': 13765,
#  'category1Name': '二手商品',
#  'category2': 14430,
#  'category2Name': '二手生活电器',
#  'category3': 14776,
#  'category3Name': '二手生活电器',
#  'primaryPic': 'jfs/t1/84047/32/11379/31676/5d8c97adEf57261e9/b3113c737e868202.jpg',
#  'currentPrice': 2613.0,
#  'recordCount': 11,
#  'bidder': '公***哥',
#  'status': 2,
#  'quality': '95成新',
#  'spectatorCount': 223,
#  'reminding': 0,
#  'shopId': 10124744,
#  'shopName': '愚人拍拍优品家电专营店',
#  'productType': 3,
#  'size': None, 'brandId': 0,
#  'brandName': None,
#  'auctionType': 1, 'actualEndTime': 1574179964000, 'delayCount': None, 'shortProductName': '三星玄龙MR+ VR眼镜体感游戏机 智能3D头盔 3D体感手柄套装VR设备', 'hasSameAuctions': False}






