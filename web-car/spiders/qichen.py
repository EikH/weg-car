import scrapy

from ..items import WebcarDataItem

class QichenSpider(scrapy.Spider):
    name = "qichen"
    allowed_domains = ["www.venucia.com","digital-official-api.dongfeng-nissan.com.cn","dongfeng-nissan.com.cn"]
    start_urls = ["https://www.venucia.com/api/VenuciaXDMApp/GetProvinceList"]

    data_url = "https://digital-official-api.dongfeng-nissan.com.cn/platform/api/venucia/store-list"

    def parse(self, response):
        data = response.json()['result']

        province_data = {}
        city_data = {}

        for i in data:
            province_data[str(i['id'])] = i['name']
            for j in i['city_list']:
                city_data[str(j['id'])] = j['name']

        yield scrapy.Request(url=self.data_url,callback=self.data_request, meta={'province_data':province_data,'city_data':city_data})

    def data_request(self, response):
        data = response.json()['result']

        province_data = response.meta['province_data']
        city_data = response.meta['city_data']

        for i in data:
            web_car_data_item = WebcarDataItem()
            # 省
            if str(i['province_id']) == '0':
                continue
            web_car_data_item['provinces'] = province_data[str(i['province_id'])]
            # 城市
            web_car_data_item['city'] = city_data[str(i['city_id'])]
            # 经销商名称
            web_car_data_item['dealerName'] = i['name']
            # 地址
            web_car_data_item['address'] = i['address']
            # 销售电话
            web_car_data_item['salesTel'] = i['sale_tel']
            # 售后电话
            web_car_data_item['afterSalesTel'] = i['service_tel']

            yield web_car_data_item

