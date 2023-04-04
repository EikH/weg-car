import scrapy

from ..items import WebcarDataItem


class QiruiSpider(scrapy.Spider):
    name = "qirui"
    allowed_domains = ["www.chery.cn"]
    start_urls = ["https://www.chery.cn/Umbraco/Surface/ajax/GetProvinces"]

    def parse(self, response):
        data = response.json()
        url = "https://www.chery.cn/Umbraco/Surface/ajax/GetCitysByProvinceId"
        for i in data:
            border = {
                "provinceid": i['PROVINCE_ID']
            }
            yield scrapy.FormRequest(url=url, formdata=border, callback=self.province_parse, meta={
                "province": i["PROVINCE_NAME"],
                "provinceid": i['PROVINCE_ID']
            })

    def province_parse(self, response):

        url = "https://www.chery.cn/Umbraco/Surface/ajax/GetDealersAndProvider"

        province = response.meta['province']
        province_id = response.meta['provinceid']

        data = response.json()
        for i in data:
            border = {
                "PROVINCE_ID": province_id,
                "CITY_ID": i['CITY_ID'],
            }
            yield scrapy.FormRequest(url=url, formdata=border, callback=self.data_parse, meta={
                "province": province,
                "city": i["CITY_NAME"]
            })

    def data_parse(self, response):

        provinces = response.meta['province']
        city = response.meta['city']

        data = response.json()
        for i in data:
            print(i)
            web_car_data_item = WebcarDataItem()
            # 省
            web_car_data_item['provinces'] = provinces
            # 城市
            web_car_data_item['city'] = city
            # 经销商名称
            web_car_data_item['dealerName'] = i['Name']
            # 销售电话
            web_car_data_item['salesTel'] = i['SalesPhone']
            # 地址
            web_car_data_item['address'] = i['Address']
            yield web_car_data_item
