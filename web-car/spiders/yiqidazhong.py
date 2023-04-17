import json

import scrapy

from ..items import WebcarDataItem


# 一汽大众
class DazhongSpider(scrapy.Spider):
    name = "yiqidazhong"
    allowed_domains = ["contact.faw-vw.com"]
    start_urls = ["https://contact.faw-vw.com/uploadfiles/js/dealer.js"]

    def parse(self, response):
        data = str(response.text)
        data = data.split('=')[1]
        data = json.loads(data)
        for i in data:
            web_car_data_item = WebcarDataItem()
            # 省
            web_car_data_item['provinces'] = i['vp_name'].split(" ")[1].strip()
            # 城市
            web_car_data_item['city'] = i['vc_name'].strip()
            # 经销商名称
            web_car_data_item['dealerName'] = i['vd_dealerName']
            # 销售电话
            web_car_data_item['salesTel'] = i['vd_salePhone']
            # 地址
            web_car_data_item['address'] = i['vd_address']
            yield web_car_data_item

