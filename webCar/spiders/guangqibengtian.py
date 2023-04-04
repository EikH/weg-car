import json

import scrapy
import re

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
            # 省
            provinces = i['address'].split('省')[0]
            if len(provinces) > 3:
                if provinces[:3] == '内蒙古':
                    provinces = '内蒙古'
                else:
                    provinces = provinces[:2]
            web_car_data_item['provinces'] = provinces

            # 城市
            web_car_data_item['city'] = i['city_name'].strip()
            # 经销商名称
            web_car_data_item['dealerName'] = i['dealer_name'].strip()
            # 销售瘦电话
            web_car_data_item['salesTel'] = i['sales_tel'].strip()
            # 售后电话
            web_car_data_item['afterSalesTel'] = i['after_sales_tel'].strip()
            # 地址
            web_car_data_item['address'] = i['address']
            yield web_car_data_item

