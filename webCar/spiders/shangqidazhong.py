import json

import scrapy

from ..items import WebcarDataItem


class ShangqidazhongSpider(scrapy.Spider):
    name = "shangqidazhong"
    allowed_domains = ["mall.svw-volkswagen.com"]
    start_urls = ["https://mall.svw-volkswagen.com/cop-uaa-adapter/api/v1/city/trees"]

    url = "https://mall.svw-volkswagen.com/cop-uaa-adapter/api/v1/dealers?&regionCode={}&sort=level&current=1&size=5000"

    def parse(self, response):
        data = response.json()["data"]["children"]
        for i in data:
            regionCode = i['code']
            yield scrapy.Request(url=self.url.format(regionCode),callback=self.parse_child)

    def parse_child(self,response):
        data = response.json()['data']['records']
        for i in data:
            web_car_data_item = WebcarDataItem()
            web_car_data_item['dealerName'] = i['orgName']
            web_car_data_item['provinces'] = i['province']
            web_car_data_item['city'] = i['city']
            web_car_data_item['address'] = i['address']
            web_car_data_item['salesTel'] = i['servicePhone']
            web_car_data_item['businessHours'] = i['businessHours']
            web_car_data_item['districtName'] = i['region']
            yield web_car_data_item


