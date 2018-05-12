# -*- coding: utf-8 -*-
import json
import re
import sys

from scrapy_redis.spiders import RedisSpider

from JingDong.items import JingdongItem, CommentItem

reload(sys)
sys.setdefaultencoding('utf-8')

import scrapy


class JingdongSpider(RedisSpider):
    name = 'jingdong'
    allowed_domains = ['p.3.cn', 'jd.com']
    # start_urls = ['https://www.jd.com/allSort.aspx']
    redis_key = "jingdong:start_urls"

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'accept - encoding': 'gzip, deflate, sdch',
        'accept - language': 'zh - CN, zh;q = 0.8'
    }
    page = 0

    def parse(self, response):
        print u'[INFO]  正在初始化请求%s' % response.url
        # 手机通讯子列链接(也可更换下面的分类进行爬取)
        node_phone_list = response.xpath('//div/div[1]/div[@class="category-item m"][2]/div[last()]//dl')
        # 家用电器
        # node_appliances_list = response.xpath('//div/div[1]/div[@class="category-item m"][3]/div[last()]//dl')
        # 数码
        # node_cameras_list = response.xpath('//div/div[1]/div[@class="category-item m"][4]/div[last()]//dl')
        # 家居家装
        # node_family_list = response.xpath('//div/div[1]/div[@class="category-item m"][5]/div[last()]//dl')
        # 厨具
        # node_cook_list = response.xpath('//div/div[1]/div[@class="category-item m"][7]/div[last()]//dl')
        # 个护化妆
        # node_beauty_list = response.xpath('//div/div[1]/div[@class="category-item m"][8]/div[last()]//dl')
        # 服饰内衣
        # node_clothes_list = response.xpath('//div/div[1]/div[@class="category-item m"][9]/div[last()]//dl')
        # 钟表
        # node_watch_list = response.xpath('//div/div[1]/div[@class="category-item m"][10]/div[last()]//dl')
        # 鞋靴
        # node_shoes_list = response.xpath('//div/div[1]/div[@class="category-item m"][11]/div[last()]//dl')
        for node in node_phone_list:
            # 商品页链接列表
            href_list = node.xpath('dd/a/@href').extract()
            for href in href_list:
                # 子列链接
                url = 'https:' + href
                print u'[INFO]  正在请求手机通讯子列链接%s' % url
                yield scrapy.Request(
                    url=url,
                    # headers=self.headers,
                    callback=self.parse_page
                )
        # 电脑办公子列链接
        node_computer_list = response.xpath('//div/div[1]/div[@class="category-item m"][6]/div[last()]//dl')
        for node in node_computer_list:
            href_list = node.xpath('dd/a/@href').extract()
            for href in href_list:
                # 子列链接
                url = 'https:' + href
                print u'[INFO]  正在请求电脑子列链接%s' % url
                yield scrapy.Request(
                    url=url,
                    # headers=self.headers,
                    callback=self.parse_page
                )

    def parse_page(self, response):
        print u'[INFO]  正在解析链接%s' % response.url
        title = response.xpath('//title/text()').extract_first()
        # 手机 手机通讯 手机【行情 价格 评价 图片】- 京东
        title_list = title.encode('utf-8').split(' ')
        # 类型
        big_type = response.xpath('//div[@class="crumbs-nav"]/div/div[1]//a/text()').extract_first()
        mid_type = response.xpath('//div[@class="crumbs-nav"]/div/div[2]//span/text()').extract_first()
        lit_type = response.xpath('//div[@class="crumbs-nav"]/div/div[3]//span/text()').extract_first()

        node_list = response.xpath('//li[@class="gl-item"]')
        # 下一页链接
        next_link = response.xpath('//span[@class="p-num"]/a[@class="pn-next"]')

        for node in node_list:
            item = JingdongItem()

            # 类型
            if not big_type or not mid_type or not lit_type:
                item['big_type'] = title_list[2].split('【')[0]
                item['mid_type'] = title_list[1]
                item['lit_type'] = title_list[1]
            else:
                item['big_type'] = big_type
                item['mid_type'] = mid_type
                item['lit_type'] = lit_type

            # 页面url
            item['url'] = response.url

            # 取出所有标签的venderid
            venderid = node.xpath('div/@venderid').extract_first()

            # 图片路径 解决
            img_src = node.xpath('div//div[@class="p-img"]//img/@src')
            if not img_src:
                img_src = node.xpath('div//div[@class="p-img"]//img/@data-lazy-img')
            img_src = "https:" + img_src.extract_first()
            item['img_src'] = img_src

            # 商品链接 解决
            good_url = "https:" + node.xpath('div//div[@class="p-img"]//a/@href').extract_first()
            item['good_url'] = good_url

            # 商品名称 已解决
            # 由于标题钱存在空格，所以标题格式[    ,真实标题]
            title = node.xpath('div//div[@class="p-name"]//em/text()').extract()[-1].strip()
            if '/' in title:
                title = title.replace('/', '')
            # 去掉标题中的-
            if '-' in title:
                title = title.replace('-', '')
            # 将空格去掉
            title = title.replace(' ','')
            item['good_name'] = title
            item['good_name'] = title

            # 提取商品的id
            good_id = re.search(r'/(\d+)\.', good_url).group(1)

            # 评论信息链接
            # 第一页 https://sclub.jd.com/comment/productPageComments.action?productId=11955374462&score=0&sortType=5&page=0&pageSize=10
            # 第二页 https://sclub.jd.com/comment/productPageComments.action?productId=11955374462&score=0&sortType=5&page=1&pageSize=10
            comment_info_url = 'https://sclub.jd.com/comment/productPageComments.action?productId=' + good_id + '&score=0&sortType=5&page=' + str(
                self.page) + '&pageSize=1'

            print u'[INFO]  正在请求评论详情页%s' % comment_info_url
            yield scrapy.Request(
                url=comment_info_url,
                callback=self.parse_comment_info,
                meta={'good_name': title}
            )

            # 提取价格信息url
            # https://p.3.cn/prices/mgets?skuIds=22042025230
            price_url = 'https://p.3.cn/prices/mgets?skuIds=' + good_id

            # 提取评论信息url
            # https://club.jd.com/comment/productCommentSummaries.action?referenceIds=22042025230
            commmet_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds=' + good_id

            # 提取商店信息url
            # https://chat1.jd.com/api/checkChat?pidList=22042025230
            store_url = 'https://chat1.jd.com/api/checkChat?pidList=' + good_id
            print u'[INFO]  正在请求价格信息链接%s' % price_url
            yield scrapy.Request(
                url=price_url,
                callback=self.parse_price,
                # headers={'Referer': response.url},
                meta={'item': item, 'commmet_url': commmet_url, 'store_url': store_url, 'next_link': next_link,
                      'venderid': venderid}
            )

        # 下一页的链接
        if next_link:
            next_link = 'https://list.jd.com' + response.xpath(
                '//span[@class="p-num"]/a[@class="pn-next"]/@href').extract_first()
            # 下一页的回调解析
            print u'[INFO]  正在请求下一页链接%s' % next_link
            yield scrapy.Request(
                url=next_link,
                callback=self.parse_page
            )

    def parse_price(self, response):
        # 京东价格

        item = response.meta['item']
        commmet_url = response.meta['commmet_url']
        content = json.loads(response.body)[0]
        good_price = content['p'] + '￥'
        item['good_price'] = good_price
        print u'[INFO]  正在请求评论数量信息链接%s' % commmet_url
        yield scrapy.Request(
            url=commmet_url,
            callback=self.parse_comment,
            meta=response.meta
        )

    def parse_store(self, response):
        item = response.meta['item']
        # 判断是否ids为0
        if 'ids=0' in response.url:
            item['good_store'] = u'没有显示商店信息'
        else:
            content = json.loads(response.body.decode('gbk'))
            item['good_store'] = content[0]['name']
        yield item

    def parse_comment(self, response):

        item = response.meta['item']
        venderid = response.meta['venderid']
        content = json.loads(response.body.decode('gbk'))
        comment_count = content['CommentsCount'][0]['CommentCountStr']
        # https://rms.shop.jd.com/json/pop/shopInfo.action?ids=1000002076
        url = 'https://rms.shop.jd.com/json/pop/shopInfo.action?ids=' + venderid
        item['comment_count'] = comment_count
        print u'[INFO]  正在请求商店信息链接%s' % url
        yield scrapy.Request(
            url=url,
            callback=self.parse_store,
            meta=response.meta,
            dont_filter=True
        )

    def parse_comment_info(self, response):
        content = response.body.decode('gbk')
        comment_dict = json.loads(content)
        productCommentSummary = comment_dict['productCommentSummary']
        item = CommentItem()
        # 商品id
        item['productId'] = productCommentSummary['productId']
        # 商品名称
        item['title'] = response.meta['good_name']
        # 好评度
        item['goodRateShow'] = productCommentSummary['productId']
        # 评论数量
        item['commentCount'] = productCommentSummary['commentCount']
        # 好评数量
        item['goodCount'] = productCommentSummary['goodCount']
        # 中评数量
        item['generalCount'] = productCommentSummary['generalCount']
        # 差评数量
        item['poorCount'] = productCommentSummary['poorCount']
        # 晒图数量
        item['imageListCount'] = comment_dict['imageListCount']
        # 热评名称和数量
        hotCommentTagStatistics_list = comment_dict['hotCommentTagStatistics']
        hotCommentTag = ''
        for node in hotCommentTagStatistics_list:
            count = node['count']
            name = node['name']
            name_count = name + '(' + str(count) + ')'
            hotCommentTag += name_count + '  '
        item['hotCommentTag'] = hotCommentTag[:-2]
        yield item
