import scrapy
import re

from ..items import WebcarDataItem

class XiaopengSpider(scrapy.Spider):
    name = "xiaopeng"
    allowed_domains = ["www.xiaopeng.com"]
    start_urls = ["https://www.xiaopeng.com/pengmetta.html?forcePlat=h5"]

    url = "https://www.xiaopeng.com/api/store/queryAll"

    def parse(self,response):
        data = response.text
        # 正则表达式提取这段文本中的csrf字段值
        csrf = re.search(r'"csrf":"(.*?)"', data).group(1)

        # 发送 POST 请求并携带参数
        yield scrapy.FormRequest(
            url=self.url,
            formdata={
                '_csrf': csrf
            },
            callback=self.parse_result
        )

    def parse_result(self, response):
        # 处理响应结果
        data = response.json()['data']

        for i in data:
            web_car_data_item = WebcarDataItem()
            # 省
            web_car_data_item['provinces'] = i['provinceName'].strip()
            # 城市
            web_car_data_item['city'] = i['cityName'].strip()
            # 经销商名称
            web_car_data_item['dealerName'] = i['storeName']
            # 销售电话
            web_car_data_item['salesTel'] = i['mobile']
            # 地址
            web_car_data_item['address'] = i['address']
            # 营业时间
            web_car_data_item['businessHours'] = i['businessHours']
            yield web_car_data_item

