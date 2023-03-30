import json

import scrapy
from ..items import WebcarDataItem


# 别克网页
class BiekeSpider(scrapy.Spider):
    name = "bieke"
    allowed_domains = ["https://static.buick.com.cn"]
    start_urls = ["https://static.buick.com.cn/resource/dealer.json"]

    def parse(self, response):
        # 加载数据
        data = json.loads(response.text)
        for i in data:
            print(i)
            webCar_data_item = WebcarDataItem()
            webCar_data_item['dealerName'] = i['dealerName']
            webCar_data_item['provinces'] = i['provinceName']
            webCar_data_item['city'] = i['cityName']
            webCar_data_item['districtName'] = i['districtName']
            webCar_data_item['address'] = i['address']
            webCar_data_item['phone'] = i['tel']
            yield webCar_data_item
