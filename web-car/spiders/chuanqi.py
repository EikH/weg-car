import scrapy

from ..items import WebcarDataItem

class ChuanqiSpider(scrapy.Spider):
    name = "chuanqi"
    allowed_domains = ["www.gacmotor.com"]
    start_urls = ["https://www.gacmotor.com/index.php/api/getStarDealerListV2"]

    city_list = ['北京','天津','重庆','海南','上海']

    def start_requests(self):
        body = {
            "type": "province",
            "province": "湖南",
            "city": "长沙",
            "level": "4s店"
        }
        yield scrapy.FormRequest(url=self.start_urls[0],formdata=body,callback=self.province_requests)

    def province_requests(self,response):
        data = response.json()["data"]
        for i in data:
            body = {
                "type": "city",
                "province": i['name'],
                "city": "长沙",
                "level": "4s店"
            }
            yield scrapy.FormRequest(url=self.start_urls[0], formdata=body, callback=self.city_requests)

    def city_requests(self,response):
        data = response.json()["data"]
        for i in data:
            try:
                web_car_data_item = WebcarDataItem()
                # 省
                web_car_data_item['provinces'] = i['province'].strip()
                # 城市
                web_car_data_item['city'] = i['province'].strip()
                # 经销商名称
                web_car_data_item['dealerName'] = i['name']
                # 销售电话
                web_car_data_item['salesTel'] = i['tel']
                # 地址
                web_car_data_item['address'] = i['address']
                # 地区
                web_car_data_item['districtName'] = i['district']
                yield web_car_data_item

            except:
                body = {
                    "type": "level",
                    "province": i['parent_name'],
                    "city": i['name'],
                    "level": "4s店"
                }
                yield scrapy.FormRequest(url=self.start_urls[0], formdata=body, callback=self.level_requests)

    def level_requests(self,response):
        data = response.json()["data"]
        for i in data:
            web_car_data_item = WebcarDataItem()
            # 省
            web_car_data_item['provinces'] = i['province'].strip()
            # 城市
            web_car_data_item['city'] = i['city'].strip()
            # 经销商名称
            web_car_data_item['dealerName'] = i['name']
            # 销售电话
            web_car_data_item['salesTel'] = i['tel']
            # 地址
            web_car_data_item['address'] = i['address']
            # 地区
            web_car_data_item['districtName'] = i['district']
            yield web_car_data_item






