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
            # 省
            web_car_data_item['provinces'] = i['provinceName'].strip()
            # 城市
            web_car_data_item['city'] = i['cityName'].strip()
            # 经销商名称
            web_car_data_item['dealerName'] = i['dealerName']
            # 销售瘦电话
            web_car_data_item['salesTel'] = i['tel']
            # 地址
            web_car_data_item['address'] = i['address']
            # 地区名
            web_car_data_item['districtName'] = i['districtName']
            yield web_car_data_item




