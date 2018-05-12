# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import pymongo
import scrapy
from scrapy.exporters import CsvItemExporter
from scrapy.pipelines.images import ImagesPipeline

from JingDong.items import CommentItem, JingdongItem
from JingDong.settings import IMAGES_STORE


class JingdongPipeline(object):
    def open_spider(self, spider):
        # 保存csv数据的文件对象
        self.p = open("/home/python/Desktop/jingdong_info/jingdong_phone.csv", "w")
        self.c = open("/home/python/Desktop/jingdong_info/jingdong_computer.csv", "a")
        self.c_c = open("/home/python/Desktop/jingdong_info/jingdong_comment.csv", "w")

        # 创建csv文件读写对象
        self.csv_exporter_p = CsvItemExporter(self.p)
        self.csv_exporter_c = CsvItemExporter(self.c)
        self.csv_exporter_c_c = CsvItemExporter(self.c_c)
        # 开始进行csv文件读写
        self.csv_exporter_p.start_exporting()
        self.csv_exporter_c.start_exporting()
        self.csv_exporter_c_c.start_exporting()

    def process_item(self, item, spider):
        # 每次写入一个item数据
        if isinstance(item, JingdongItem):
            if item['big_type'] == u'手机':
                print u'[INFO]  正在写入手机商品csv文件'
                self.csv_exporter_p.export_item(item)
            elif item['big_type'] == u'电脑、办公':
                print u'[INFO]  正在写入电脑商品csv文件'
                self.csv_exporter_c.export_item(item)
        elif isinstance(item, CommentItem):
            print u'[INFO]  正在写入评论信息csv文件'
            self.csv_exporter_c_c.export_item(item)
        return item

    def close_spider(self, spider):
        # 结束csv文件读写
        self.csv_exporter_c.finish_exporting()
        self.csv_exporter_p.finish_exporting()
        self.csv_exporter_c_c.finish_exporting()
        # 关闭文件
        self.p.close()
        self.c.close()
        self.c_c.close()


class JingdongMongoDBPipline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['JINGDONG']
        self.collection_comment = self.db['jingdong_comment']
        self.collection_goods = self.db['jingdong_goods']

    def process_item(self, item, spider):
        if isinstance(item, CommentItem):
            print u'[INFO]  正在保存%s评论信息到mongoDB' % item['title']
            self.collection_comment.insert(dict(item))
        elif isinstance(item, JingdongItem):
            print u'[INFO]  正在保存商品信息%s到mongoDB' % item['good_name']
            self.collection_goods.insert(dict(item))
        return item

    def close_spider(self, spider):
        pass


class JingDongImagePipline(ImagesPipeline):
    # 保存图片到默认位置
    def get_media_requests(self, item, info):
        if isinstance(item, JingdongItem):
            print u'[INFO]  正在保存图片%s' % item['img_src']
            yield scrapy.Request(item['img_src'])

    def item_completed(self, results, item, info):
        if isinstance(item, JingdongItem):
            print u'[INFO]  正在修改图片路径%s' % item['img_src']
            # 原来图片存储路径
            img_path = [x['path'] for ok, x in results if ok][0]
            if '/' in item['good_name']:
                item['good_name'] = item['good_name'].replace('/', '')
            if '-' in item['good_name']:
                item['good_name'] = item['good_name'].replace('-', '')
            item['good_name'] = item['good_name'].strip().replace(' ', '')
            # 现在图片路径
            item['img_src'] = IMAGES_STORE + item['good_name'] + item['img_src'][-4:]
            # 修改名字
            try:
                os.rename(
                    IMAGES_STORE + img_path,
                    item['img_src']
                )
                print u'[INFO]  修改图片路径成功%s' % item['img_src']
            except Exception as e:
                print e
                print img_path
                print u'[ERROR] 修改图片路径失败%s' % item['img_src']
            return item
