import scrapy

from ..items import WebcarDataItem


class NezhaSpider(scrapy.Spider):
    name = "nezha"
    allowed_domains = ["www.hozonauto.com"]
    start_urls = ["https://www.hozonauto.com/api_new/api_dealer_list_new1"]

    def parse(self, response):
        data = response.json()['data']['list']
        for i in data:
            web_car_data_item = WebcarDataItem()
            web_car_data_item['dealerName'] = i['dealer_name']
            web_car_data_item['provinces'] = i['province_region_name']
            web_car_data_item['address'] = i['dealer_address']

            try:
                web_car_data_item['city'] = i['dealer_tel']
            except:
                web_car_data_item['city'] = "无"

            try:
                web_car_data_item['salesTel'] = i['dealer_tel']
            except:
                web_car_data_item['salesTel'] = "无"

            yield web_car_data_item
