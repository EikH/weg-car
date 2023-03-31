import json

import scrapy

from ..items import WebcarDataItem

# 广汽丰田
class GuangqibengtianSpider(scrapy.Spider):
    name = "guangqibengtian"
    allowed_domains = ["www.ghac.cn"]
    start_urls = ["https://www.ghac.cn/api/honda/v1/Leads/GetAllDealerProCitys"]

    def parse(self, response):
        data = response.json()['Data']['Dealers']
        for i in data:
            web_car_data_item = WebcarDataItem()
            web_car_data_item['dealerName'] = i['dealer_name']
            web_car_data_item['provinces'] = i['address'].split('省')[0]
            web_car_data_item['companyName'] = i['regist_name']
            web_car_data_item['city'] = i['city_name']
            web_car_data_item['address'] = i['address']
            web_car_data_item['salesTel'] = i['sales_tel']
            web_car_data_item['afterSalesTel'] = i['after_sales_tel']
            yield web_car_data_item