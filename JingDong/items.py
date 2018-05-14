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
    # 商品名称
    good_title = scrapy.Field()
    # 用户id
    user_id = scrapy.Field()
    # 评论信息
    content = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()
    # 产品评分星级
    score = scrapy.Field()
    # 产品颜色
    color = scrapy.Field()




