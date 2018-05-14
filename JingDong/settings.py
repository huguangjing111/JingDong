# -*- coding: utf-8 -*-

# Scrapy settings for JingDong project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'JingDong'

SPIDER_MODULES = ['JingDong.spiders']
NEWSPIDER_MODULE = 'JingDong.spiders'

IMAGES_STORE = '/home/python/Desktop/jingdong_info/'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'JingDong (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'JingDong.middlewares.JingdongSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
   # 'JingDong.middlewares.JingdongDownloaderMiddleware': 543,
   # 'JingDong.middlewares.JingDongProxyMiddleWares': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'JingDong.plines.JingdongPipeline': 300,
   # 'JingDong.pipelines.JingdongPipeline': 100,
   # 'JingDong.pipelines.JingDongImagePipline': 150,
   'JingDong.pipelines.JingdongMongoDBPipline': 200,

   # 'scrapy_redis.pipelines.RedisPipeline': 900
}

# 1(必须). 使用了scrapy_redis的去重组件，在redis数据库里做去重
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 2(必须). 使用了scrapy_redis的调度器，在redis里分配请求
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 3(必须). 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复，也就是不清理redis queues
SCHEDULER_PERSIST = True

# 4(必须). 通过配置RedisPipeline将item写入key为 spider.name : items 的redis的list中，供后面的分布式处理item
# 这个已经由 scrapy-redis 实现，不需要我们写代码，直接使用即可


# 5(必须). 指定redis数据库的连接参数
# REDIS_HOST = '127.0.0.1'
# REDIS_PORT = 6379

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


LOG_ENABLED = True  # 启用logging
LOG_ENCODING = 'utf-8'  # logging使用的编码
LOG_FILE = '/home/python/Desktop/jingdong_info/jingdong.log'  # 在当前目录里创建logging输出文件的文件名
# LOG_FILE = 'jingdong.log'  # 在当前目录里创建logging输出文件的文件名
LOG_LEVEL = 'DEBUG'  # log的最低级别
LOG_STDOUT = False  # 如果为 True，进程所有的标准输出(及错误)将会被重定向到log中。例如，执行 print "hello" ，其将会在Scrapy log中显示。

