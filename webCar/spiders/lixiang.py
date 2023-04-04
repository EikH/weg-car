import scrapy

from ..items import WebcarDataItem

class LixiangSpider(scrapy.Spider):
    name = "lixiang"
    allowed_domains = ["www.lixiang.com"]
    start_urls = ["https://api-web.lixiang.com/mall-unit-api/v1-0/service-centers?types=RETAIL,DELIVER,AFTERSALE,SPRAY,TEMPORARY_EXHIBITION,TEMPORARY_AFTERSALE_SUPPORT&sortType=CITY"]

    def parse(self, response):
        data = response.json()['data']
        for i in data:
            web_car_data_item = WebcarDataItem()
            # 省
            web_car_data_item['provinces'] = i['provinceName'].strip()
            # 城市
            web_car_data_item['city'] = i['cityName'].strip()
            # 经销商名称
            web_car_data_item['dealerName'] = i['name']
            # 销售瘦电话
            web_car_data_item['salesTel'] = i['telephone']

            # 地址
            web_car_data_item['address'] = i['address']
            # 营业时间
            web_car_data_item['businessHours'] = i['openingHours']
            # 地区
            try:
                web_car_data_item['districtName'] = i['countyName']
            except:
                web_car_data_item['districtName'] = ""
            yield web_car_data_item


