import json

import scrapy

from ..items import WebcarDataItem

# 广汽丰田
class GuangqibengtianSpider(scrapy.Spider):
    name = "guangqibengtian"
    allowed_domains = ["www.ghac.cn"]
    start_urls = ["https://www.ghac.cn/api/honda/v1/Leads/GetAllDealerProCitys"]

    def parse(self, response):
        data = json.loads(response.text)['Data']['Dealers']
        for i in data:
            webCar_data_item = WebcarDataItem()
            webCar_data_item['dealerName'] = i['dealer_name']
            webCar_data_item['companyName'] = i['regist_name']
            webCar_data_item['city'] = i['city_name']
            webCar_data_item['address'] = i['address']
            webCar_data_item['salesTel'] = i['sales_tel']
            webCar_data_item['afterSalesTel'] = i['after_sales_tel']
            yield webCar_data_item