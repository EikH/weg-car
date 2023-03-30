import json

import scrapy

from ..items import WebcarYiqidazhongItem


# 一汽大众
class DazhongSpider(scrapy.Spider):
    name = "yiqidazhong"
    allowed_domains = ["https://contact.faw-vw.com"]
    start_urls = ["https://contact.faw-vw.com/uploadfiles/js/dealer.js"]

    def parse(self, response):
        data = str(response.text)
        data = data.split('=')[1]
        data = json.loads(data)
        for i in data:
            webCar_Yiqidazhong_item = WebcarYiqidazhongItem()
            webCar_Yiqidazhong_item['dealerName'] = i['vd_dealerName']
            webCar_Yiqidazhong_item['provinces'] = i['vp_name'].split(" ")[1]
            webCar_Yiqidazhong_item['city'] = i['vc_name']
            webCar_Yiqidazhong_item['address'] = i['vd_address']
            webCar_Yiqidazhong_item['phone'] = i['vd_salePhone']
            yield webCar_Yiqidazhong_item
