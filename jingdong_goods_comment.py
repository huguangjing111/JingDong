# -*- encoding:utf-8 --
import csv
import json
import sys
import time
import random

reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from bs4 import BeautifulSoup


class JingdongSpider(object):
    def __init__(self):
        self.keyword = raw_input('请输入需要查看的商品名称:')
        self.page = 1
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "user-key=6085c897-ddf8-48d4-b398-5bf69edfda3b; cn=0; __jdu=204824368; PCSYCityID=1607; ipLocation=%u5317%u4EAC; areaId=1; ipLoc-djd=1-72-2799-0; 3AB9D23F7A4B3C9B=ACZIR3T53FU2R4YT77FV5DTHDU3COD3BS7D3CTEUCWHQ7XVAJE3OWL6FAUVGWDQQKN7UFPBN7YHCH72ICGZT5BCIB4; unpl=V2_ZzNtbUBeRUF2DkNQexEIUWJXFVlLA0cRdwxGVCgeWAA3ChYOclRCFXwUR1FnGVsUZAIZXkNcRx1FCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2V3ocVQZiARVUcmdEJUU4Ql1zHVkAVwIiXHIVF0lxDkFTchwRBmYGG15HVUQcRQl2Vw%3d%3d; CCC_SE=ADC_2%2bdLSIk8e8aGul6M8dZyF3%2b3s%2bwPV%2bh68I9F9aq45ddUMYqLj9QE8%2budL6dMWoTEF7ZHu%2bxaFQf1Cu8Fi6IZpaTceQU1eU%2bJziqAn82H%2bZGKyrHT7y48WuMzo7Gzwl69ka6iiwO%2fwlVpQRuRoF5z3Rda%2bc6XBxjd1HxziCSrcTDgzix1vymzpzq3%2blBr%2fIaW%2fd%2bKW1zoK3Cs%2byw%2bNy78O07fVc93WlO22kAvdZj63iZRZ8svHcNe0GLyRqrGFY%2flFCqjS6QAlaX4vT%2btj7Njiuz7aKUx8adxxcZeYOK85nUxMqYrDHo6P6lOF8qJKRXiUgI7O8FllyYr439pj2bpFM8dzNyxfCp5VojcpgRiUAdmfDJpk63rdhPKAkyg5T69nXHyYrv7pIa%2fP9JFq8Gxb8ZxE6Ezsj95wYgBs0JwPxtXp%2f97V7tNhEVfcnjO%2btvPXQ%2fyF2iuAG6d4TOal7cB%2bVeuuRYoUrl2VsEB5Y5LCX3saeRUaSEudD5NRvVly2bk%2bmwCNVIQ2lCieWjC6Jd8v8iUFpYrTrSEmoSsfJpMzpuBG6zST1H1Rw89NT%2fHFdW2; __jda=122270672.204824368.1523282235.1523523453.1523881261.3; __jdc=122270672; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_387e274519ee4e658e553511b654a85b|1523881499590; xtest=2699.cf6b6759; qrsc=3; __jdb=122270672.11.204824368|3.1523881261; rkv=V0600",
            "Host": "search.jd.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36"
        }
        self.proxies = {'http': 'http://maozhaojun:ntkn0npx@114.67.224.167:16819'}
        self.url = url = "https://search.jd.com/Search?keyword=" + self.keyword + "&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=" + self.keyword + "&page=" + str(
            self.page) + "&s=54&click=0"
        self.data_list = []
        self.total_page = 1
        self.goods_href_list = []
        self.sku_id_list = []
        self.comment_list = []
        self.comment_page = 0
        self.total_comment_page = 0
    # 发送请求
    def send_request(self, url, headers):
        # time.sleep(random.randint(1,3))
        html = requests.get(url, headers=headers, proxies=self.proxies).content
        return html

    def send_request_commment(self, data_sku):
        # time.sleep(random.randint(1, 3))
        url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1290&productId=' + data_sku + '&score=0&sortType=5&page=' + str(
            self.comment_page) + '&pageSize=10&isShadowSku=0&fold=1'
        headers = {
            "accept": "*/*",
            # "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "user-key=6085c897-ddf8-48d4-b398-5bf69edfda3b; cn=0; __jdu=204824368; PCSYCityID=1607; ipLocation=%u5317%u4EAC; areaId=1; ipLoc-djd=1-72-2799-0; 3AB9D23F7A4B3C9B=ACZIR3T53FU2R4YT77FV5DTHDU3COD3BS7D3CTEUCWHQ7XVAJE3OWL6FAUVGWDQQKN7UFPBN7YHCH72ICGZT5BCIB4; mt_xid=V2_52007VwATV1RbV1gYQClbVjVUEQdVUU5STEhKQAAwAUFOVA9RWwMcGghRMlBHUlxbWlovShhcDHsCF05dXkNZHEIbXQ5iCiJQbVhiWR5OGFoEZQQSYl1dVF0%3D; __jdc=122270672; unpl=V2_ZzNtbRADEUUiXRIGeExZUmICRVtLBUdAJQ8SVnlKWFBlARMKclRCFXwUR1FnGVUUZwEZXkdcQRVFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2V3ocVQZiARVUcmdEJUU4Tlx%2fHlsMVwIiXHIVF0l9C0ZcfRARBmYGG15HVUQcRQl2Vw%3d%3d; CCC_SE=ADC_tPtU75YOW80GahHzFHShI018uY4%2fB2fa3rZq8z5uPCwzPrFAYCeDLZx9CCgzw0IAj4EACHFXermV1cDrxNeTJXHKcls6jiMq55EJMsRaTqsQtWG88scPSSkmDs5%2ffacQHKjlm%2bVQfWnz%2b9OKjKanlHUcv7YR6uKQml9Ql6n35EPOMsqYyAbh%2buswXUChnjhd5U%2fJmUC2EjktaqqctBPSpvlzfsmmoi0pOksHdQ4b8%2fy7hZtAnghXCJ7jQDXeNgmYBQHEx6nyTmuWSM5av0uSAhFtzCkyGLXndzmolD%2fbrVIOYVtJlV49WqK82ChuPmmunnGaM8%2b5jt37bdJHt5bI9C5%2bBkIBJGcREPLTCbvYG1tmoxl%2fUBxEfUWsSIiIlNC56PP3NKPBGGd4AAltg4%2fPM3o3LBrFnIaCNvrranLNnagVUhC%2f2M64ECmYbjPiybKbO7C7htsbQHdpWwXE08FHxUhgSUuS1CUhIeBrEjK%2f04Rk%2fUmMkb0ARJpqyqIY4CevJqHvE1kAZ%2fShLu8bFJwiZOTfd86I9Zz3E7lufMVDqqjO%2b3EKuuZfJy8YDznBsGwGvMy3%2bMkG1aKNcBndjuPG2KrrSHWrvgSgZu%2f7JKUtYax%2fxgDyWDYD%2fflqDEvNpX5A4p6Es%2fRxMWYVqC2FjtkjoE5wiCMY03xdMs%2bpHB%2b3R%2b2MMnmx2yPXPlXrleWZYb%2fVBCFcbvf%2bRgJvuplKkY67taJpZRDbqKLK%2fYVsSAZzskE%3d; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_cecafdec2d4f40f78c5da6e33b5d330f|1524029073862; __jda=122270672.204824368.1523282235.1524032762.1524034813.10; __jdb=122270672.2.204824368|10.1524034813",
            "referer": "https://item.jd.com/18026504772.html",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36"
        }
        html_json = requests.get(url, headers=headers, proxies=self.proxies)
        try:
            dict_str = html_json.content[25:][1:-2].decode('gbk').encode('utf-8')
            dict = json.loads(dict_str)
            comments = dict['comments']
            self.deal_comment(comments)
        except Exception as e:
            print e

    def get_data_sku(self, html):
        soup = BeautifulSoup(html, 'lxml')
        li_list = soup.find_all('li', attrs={'class': 'gl-item'})
        show_items = ''
        for li in li_list:
            show_items += li.get('data-sku') + ','
            data_sku = li.get('data-sku')
            self.sku_id_list.append(li.get('data-sku'))
            i = 0
            while i < 3:
                try:
                    self.send_request_commment(data_sku)
                except Exception as e:
                    print e
                    continue
                self.comment_page += 1
                self.total_comment_page += 1
                print self.total_comment_page
                i += 1
            self.comment_page = 0

        show_items = show_items[:-1]
        return show_items

    def deal_comment(self, comments):
        for comment in comments:
            item = {'user_id': comment['id'], 'user_content': comment['content'],
                    'creationTime': comment['creationTime'], 'referenceName': comment['referenceName'],
                    'score': comment['score'], 'productColor': comment['productColor'],
                    'productSize': comment['productSize'], 'userLevelName': comment['userLevelName'],
                    'userClientShow': comment['userClientShow']}
            self.comment_list.append(item)

    def write(self):
        json.dump(self.comment_list, open('./demo/jingdong_comment_all.json', 'w'))

    def json_to_csv(self):
        json_file = open('./demo/jingdong_comment_all.json', 'r')
        csv_file = open('./demo/jingdong_comments_all.csv', 'w')
        # 创建操作对象
        writer = csv.writer(csv_file)
        # 打开json文件并转为python字符串
        comments_list = json.load(json_file)
        # 表头部分
        sheet_header = comments_list[0].keys()
        # body部分
        sheet_body = [item.values() for item in comments_list]

        # 写入文件
        writer.writerow(sheet_header)
        writer.writerows(sheet_body)

        json_file.close()
        csv_file.close()

    def get_data_sku_double(self, html):
        soup = BeautifulSoup(html, 'lxml')
        li_list = soup.find_all('li')
        for li in li_list:
            self.sku_id_list.append(li.get('data-sku'))
            data_sku = li.get('data-sku')
            i = 0
            while i < 3:
                try:
                    self.send_request_commment(data_sku)
                except Exception as e:
                    print e
                    continue
                self.comment_page += 1
                self.total_comment_page += 1
                i += 1

    def main(self):
        while self.total_page <= 199:
            while True:
                html = None
                try:
                    html = self.send_request(self.url, self.headers)
                except Exception as e:
                    print '111'
                    print e
                if not html:
                    continue
                else:
                    self.page += 1
                    self.total_page += 1
                    show_items = self.get_data_sku(html)
                    break

            while True:
                html = None
                try:
                    url = 'https://search.jd.com/s_new.php?keyword=' + self.keyword + '&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=' + self.keyword + '&page=' + str(
                        self.page) + '&s=27&scrolling=y&log_id=&tpl=1_M&show_items=' + show_items
                    headers = {
                        # ":authority": "search.jd.com",
                        # ":method": "GET",
                        # ":path": "/s_new.php?keyword=%E7%94%B5%E8%84%91&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E7%94%B5%E8%84%91&page=2&s=27&scrolling=y&log_id=1523958279.23030&tpl=1_M&show_items=4624505,5512841,5225346,5029717,4335674,4824715,5696028,4335139,5483596,5020872,4161503,4338107,5334717,6339280,5352358,5113099,5148275,4431213,5005927,4752515,4410292,5456134,6031973,5148309,6072622,4994913,4888355,1378536,15437775297,5834183",
                        # ":scheme": "https",
                        "accept": "*/*",
                        "accept-encoding": "gzip, deflate, br",
                        "accept-language": "zh-CN,zh;q=0.9",
                        "cookie": "user-key=6085c897-ddf8-48d4-b398-5bf69edfda3b; cn=0; __jdu=204824368; PCSYCityID=1607; ipLocation=%u5317%u4EAC; areaId=1; ipLoc-djd=1-72-2799-0; 3AB9D23F7A4B3C9B=ACZIR3T53FU2R4YT77FV5DTHDU3COD3BS7D3CTEUCWHQ7XVAJE3OWL6FAUVGWDQQKN7UFPBN7YHCH72ICGZT5BCIB4; xtest=2699.cf6b6759; qrsc=3; __jda=122270672.204824368.1523282235.1523945123.1523953091.5; __jdc=122270672; rkv=V0600; mt_xid=V2_52007VwATV1RbV1gYQClVVWEAQQdaC04OSEhOQABiChVOVQoADgNNHV5SNAJAUVxbAF0vShhcDHsCF05dXkNaGUIYWg5iBSJQbVhiWhdBGlwGbwMRYl1dVF0%3D; unpl=V2_ZzNtbRIEEEd0XEEBfhoMB2IDFVoRUEMdcwtFAXpLCFFkB0EIclRCFXwUR1FnGVoUZwUZXkRcRxxFCHZXchBYAWcCGllyBBNNIEwHDCRSBUE3XHxcFVUWF3RaTwEoSVoAYwtBDkZUFBYhW0IAKElVVTUFR21yVEMldQl2V3ocVQZiARVUcmdEJUU4Q1d9Hl8AVwIiXHIVF0lyCEdXeBgRBmYGG15HVUQcRQl2Vw%3d%3d; CCC_SE=ADC_cj6vbVyJXQOPKIU%2b8SklkO1zrFKx%2bXhdvYSlOs65ZlgOEJI7GEV9ChPnMc1Tx3iKBjx77OSYHBp8m%2b5crvjb%2fFU3QS1QuYfw6%2f%2b140J8ZCEYFEQe1p7z4jFOMap9DnTh7OY9j2IRmSaausgWrEXf1UqRRg0s87nsBXWDYe2tKFMsvsq%2bOkWUZqx4pRCbk%2fVYNMXVcgWe4kq2D7%2bAZ%2by7gQM7lQ0SLSHaBbx141qk3wPMhW0I6yPRaz5A1GGV0oNoyeuj5Eooj8AxBrnCP4KRw4Gj0PJw6BX0hQCzZ%2ff6nZ%2bgkMQIjvUM%2f1e%2bWI0TBXcxoyguqVixR9TLD5vN9wXo8ZDUUKAeH5NelDHn%2bI46FfgXNbI1JqWvJ%2fU3nenZUvH6lDcjr0oxrWmsIdwgyZz1EJAUC4qfmSM1A6g6Uu87BCCcTtHZFuw0A%2fR1jd83W44F%2fFop0R%2fo4nEFONoq2OXgJhhXyRXIiPlVpJPQBg04S1LfWBhK%2b%2bwY%2fzPJbaLx5Fo8q3rlvIrPSgEJIYycoUz759UN2fD9LeN0A9LiHIL7FCfw1Lv87CCpuvm7n6z0TtcHP4h1fiU%2bTnxAb8t%2bnL4Z0yK9VnxgHObU%2f%2bJH5VtzBcDQz%2bbjqwJoekKCH0lzAmo9N%2bL%2f0DHxrcx6EkPJ1D2F8E6AT9UIFW%2ba5luMpnW0u9yHDfgzGF5BRLGSGWza6NCy78pG%2bGpBBwxuZelviLjvK78UojTLlgT%2b8QBcOephjLY%3d; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_abbc0e6d42a34166b619722d0cee25bd|1523957280784; __jdb=122270672.11.204824368|5.1523953091",
                        "referer": "https://search.jd.com/Search?keyword=%E7%94%B5%E8%84%91&enc=utf-8&wq=%E7%94%B5%E8%84%91&pvid=e8dcdcf68fb341848215bb5a9d583bfd",
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36",
                        "x-requested-with": "XMLHttpRequest"
                    }

                    html = self.send_request(url, headers)

                except Exception as e:
                    print '222'
                    print e
                if html:
                    self.page += 1
                    self.total_page += 1
                    self.get_data_sku_double(html)
                    break
                else:
                    continue
        self.write()
        self.json_to_csv()


if __name__ == '__main__':
    spider = JingdongSpider()
    spider.main()
