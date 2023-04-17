import scrapy
import json

from ..items import WebcarDataItem


class JietuSpider(scrapy.Spider):
    name = "jietu"
    allowed_domains = ["jetour.com.cn", "shop.jetour.com.cn"]
    start_urls = ["https://shop.jetour.com.cn/wxapi/api-basic/api/region/findAllProvinces"]

    city_url = 'https://shop.jetour.com.cn/wxapi/api-basic/api/region/findCityByProvinceId/{}'

    data_url = 'https://shop.jetour.com.cn/wxapi/api-dealer/dealer-info/searchDealerListByCondition'

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    def parse(self, response):
        data = response.json()
        for i in data:
            id_ = i['id']

            yield scrapy.Request(url=self.city_url.format(id_), callback=self.city_requests)

    def city_requests(self, response):
        data = response.json()

        for i in data:
            cityId = i['id']
            provinceId = i['provinceId']
            body = {
                'provinceId': str(provinceId),
                'cityId': cityId,
                'type': '1'
            }
            body = json.dumps(body)

            yield scrapy.Request(url=self.data_url, body=body, method='POST', callback=self.data_requests, headers=self.headers)

    def data_requests(self, response):
        data = response.json()['data']

        if data is None:
            return

        for i in data:
            print(i)
            web_car_data_item = WebcarDataItem()
            # 省
            web_car_data_item['provinces'] = i['provinceName']
            # 城市
            web_car_data_item['city'] = i['cityName']
            # 经销商名称
            web_car_data_item['dealerName'] = i['name']
            # 地址
            web_car_data_item['address'] = i['address']
            # 销售电话
            web_car_data_item['salesTel'] = i['salesTel']

            yield web_car_data_item
