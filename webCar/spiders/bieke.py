import json

import scrapy
from ..items import WebcarDataItem


# 别克网页
class BiekeSpider(scrapy.Spider):
    name = "bieke"
    allowed_domains = ["static.buick.com.cn"]
    start_urls = ["https://static.buick.com.cn/resource/dealer.json"]

    def parse(self, response):
        # 加载数据
        data = response.json()
        for i in data:
            web_car_data_item = WebcarDataItem()
            web_car_data_item['dealerName'] = i['dealerName']
            web_car_data_item['provinces'] = i['provinceName']
            web_car_data_item['city'] = i['cityName']
            web_car_data_item['address'] = i['address']
            web_car_data_item['districtName'] = i['districtName']
            web_car_data_item['salesTel'] = i['tel']
            yield web_car_data_item

