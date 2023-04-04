import scrapy

from ..items import WebcarDataItem

class WeipaiSpider(scrapy.Spider):

    name = "weipai"
    allowed_domains = ["www.wey.com","cmsmanage-siteapi.gwm.com.cn"]
    start_urls = ["https://cmsmanage-siteapi.gwm.com.cn/dealer/province-zh","https://cmsmanage-siteapi.gwm.com.cn/dealer/city-zh","https://cmsmanage-siteapi.gwm.com.cn/dealer/dealer-zh"]

    def start_requests(self):
        border = {
            "dealer_type": "2",
        }
        yield scrapy.FormRequest(url=self.start_urls[0], formdata=border, callback=self.province_requests)

    def province_requests(self, response):
        data = response.json()["data"]
        for i in data:
            border = {
                "dealer_type": "2",
                "province": i['province'],
            }
            yield scrapy.FormRequest(url=self.start_urls[1], formdata=border, callback=self.city_requests)

    def city_requests(self, response):
        data = response.json()["data"]
        for i in data:
            border = {
                "dealer_type": "2",
                "city": i['city'],
            }
            yield scrapy.FormRequest(url=self.start_urls[2], formdata=border, callback=self.data_requests)

    def data_requests(self, response):
        data = response.json()["data"]
        for i in data:
            print(i)
            web_car_data_item = WebcarDataItem()
            # 省
            web_car_data_item['provinces'] = i['province'].strip()
            # 城市
            web_car_data_item['city'] = i['city'].strip()
            # 经销商名称
            web_car_data_item['dealerName'] = i['name']
            # 销售电话
            web_car_data_item['salesTel'] = i['hotline']
            # 地址
            web_car_data_item['address'] = i['address']
            # 地区
            web_car_data_item['districtName'] = i['county']
            yield web_car_data_item
