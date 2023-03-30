import json

import scrapy


class ShangqidazhongSpider(scrapy.Spider):
    name = "shangqidazhong"
    allowed_domains = ["mall.svw-volkswagen.com"]
    start_urls = ["https://mall.svw-volkswagen.com/cop-uaa-adapter/api/v1/city/trees"]

    url = "https://mall.svw-volkswagen.com/cop-uaa-adapter/api/v1/dealers?&regionCode={}&sort=level&current=1&size=5000"

    def parse(self, response):
        data = json.loads(response.text)["data"]["children"]
        for i in data:
            print(i['code'])
            regionCode = i['code']
            yield scrapy.Request(url=self.url.format(regionCode),callback=self.parse_child)

    def parse_child(self,response):
        print(response.text)
