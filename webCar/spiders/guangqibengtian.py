import json

import scrapy
from ..items import web

# 广汽丰田
class GuangqibengtianSpider(scrapy.Spider):
    name = "guangqibengtian"
    allowed_domains = ["https://www.ghac.cn/api/honda/v1/Leads/GetAllDealerProCitys"]
    start_urls = ["https://www.ghac.cn/api/honda/v1/Leads/GetAllDealerProCitys"]

    def parse(self, response):
        data = json.loads(response.text)['Data']['Dealers']
        for i in data:
            webcar_guangqibengtian_item = WebcarGuangqibengtianItem()
            webcar_guangqibengtian_item['dealerName'] = i['dealer_name']
            webcar_guangqibengtian_item['registName'] = i['regist_name']
            webcar_guangqibengtian_item['city'] = i['city_name']
            webcar_guangqibengtian_item['address'] = i['address']
            webcar_guangqibengtian_item['salesTel'] = i['sales_tel']
            webcar_guangqibengtian_item['afterSalesTel'] = i['after_sales_tel']
            yield webcar_guangqibengtian_item
