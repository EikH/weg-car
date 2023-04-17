import scrapy

from ..items import WebcarDataItem


class JiliSpider(scrapy.Spider):
    name = "jili"
    allowed_domains = ["www.geely.com"]
    start_urls = ["https://www.geely.com/api/geely/official/common/GetArea"]

    city_url = "https://www.geely.com/api/geely/official/common/GetArea?regionId={}"

    data_url = "https://www.geely.com/api/geely/official/common/GetDealerList?provinceId={}&cityId={}"

    def parse(self, response):
        data = response.json()['data']

        for i in data:
            provinceId = i['regionId']
            provinces = i['regionName']

            yield scrapy.Request(url=self.city_url.format(provinceId), callback=self.city_request, meta={"provinces": provinces, "provinceId":provinceId})


    def city_request(self, response):

        data = response.json()['data']

        provinces = response.meta['provinces']
        provinceId = response.meta['provinceId']


        for i in data:
            cityId = i['regionId']
            city = i['regionName']
            yield scrapy.Request(url=self.data_url.format(provinceId,cityId), callback=self.data_request,
                                 meta={
                                     "provinces": provinces,
                                     "city":city
                                 })



    def data_request(self, response):
        data = response.json()['data']

        provinces = response.meta['provinces']
        city = response.meta['city']

        for i in data:
            web_car_data_item = WebcarDataItem()
            # 省
            web_car_data_item['provinces'] = provinces
            # 城市
            web_car_data_item['city'] = city
            # 经销商名称
            web_car_data_item['dealerName'] = i['DealerName']
            # 地址
            web_car_data_item['address'] = i['Address']
            # 销售电话
            web_car_data_item['salesTel'] = i['HotLine']

            yield web_car_data_item
