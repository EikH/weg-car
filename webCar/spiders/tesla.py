import scrapy

from ..items import WebcarDataItem

class TeslaSpider(scrapy.Spider):
    name = "tesla"
    allowed_domains = ["www.tesla.cn"]
    start_urls = ["https://www.tesla.cn/cua-api/tesla-locations?translate=zh_CN&map=baidu&usetrt=true"]

    url_child= "https://www.tesla.cn/cua-api/tesla-location?id={}"

    def parse(self, response):
        data = response.json()
        for i in data:
            location_id = i['location_id']
            yield scrapy.Request(url=self.url_child.format(location_id), callback=self.parse_child)

    def parse_child(self, response):
        data = response.json()
        if isinstance(data,list):
            print("数据异常")
            return
        web_car_data_item = WebcarDataItem()
        web_car_data_item['dealerName'] = data['title']

        web_car_data_item['provinces'] = data['province_state']
        web_car_data_item['city'] = data['city']
        web_car_data_item['address'] = data['address']

        # 电话号码
        phone = ""
        for j in data['sales_phone']:
            phone = "{}{}:{},".format(phone,j['label'],j['number'])

        web_car_data_item['salesTel'] = phone
        try:
            web_car_data_item['businessHours'] = data['hours'].replace('<p><strong>','').replace("</strong><br />",":").replace("</p>",",")
        except:
            web_car_data_item['businessHours'] = "无"
        yield web_car_data_item
