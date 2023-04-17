import scrapy

from ..items import WebcarDataItem


class TankeSpider(scrapy.Spider):
    name = "tanke"
    allowed_domains = ["www.haval.com.cn", "cmsmanage-siteapi.gwm.com.cn"]

    start_urls = ["https://cmsmanage-siteapi.gwm.com.cn/dealer/service-province-zh",
                  "https://cmsmanage-siteapi.gwm.com.cn/dealer/service-city-zh",
                  "https://cmsmanage-siteapi.gwm.com.cn/dealer/dealer-zh",
                  "https://cmsmanage-siteapi.gwm.com.cn/dealer/service-zh"]

    def start_requests(self):
        body = {
            "dealer_type": "2",
        }
        yield scrapy.FormRequest(url=self.start_urls[0], formdata=body, callback=self.province_requests)

    def province_requests(self, response):
        data = response.json()["data"]
        for i in data:
            body = {
                "dealer_type": "2",
                "province": i['province'],
            }
            yield scrapy.FormRequest(url=self.start_urls[1], formdata=body, callback=self.city_requests)

    def city_requests(self, response):
        data = response.json()["data"]
        for i in data:
            for url in self.start_urls[2:]:
                body = {
                    "dealer_type": "2",
                    "city": i['city'],
                }
                yield scrapy.FormRequest(url=url, formdata=body, callback=self.data_requests)


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
