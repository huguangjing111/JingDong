# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongItem(scrapy.Item):
    # define the fields for your item here like:
    # 大类
    big_type = scrapy.Field()
    # 中间类
    mid_type = scrapy.Field()
    # 小类
    lit_type = scrapy.Field()
    # 图片地址
    img_src = scrapy.Field()
    # 商品详情页面链接
    good_url = scrapy.Field()
    # 商品标题
    good_name = scrapy.Field()
    # 商品价格
    good_price = scrapy.Field()
    # 评论数目
    comment_count = scrapy.Field()
    # 商店信息
    good_store = scrapy.Field()
    # 页面url
    url = scrapy.Field()


class CommentItem(scrapy.Item):
    #商品id
    productId = scrapy.Field()
    # 商品名称
    title = scrapy.Field()
    # 好评度
    goodRateShow= scrapy.Field()
    # 评论数量
    commentCount = scrapy.Field()
    # 好评数量
    goodCount = scrapy.Field()
    # 中评数量
    generalCount = scrapy.Field()
    # 差评数量
    poorCount = scrapy.Field()
    # 晒图数量
    imageListCount = scrapy.Field()
    # 热评名称和数量
    hotCommentTag = scrapy.Field()




