import scrapy
import re

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
        # 响应数据
        data = response.json()

        # 门店类型
        service = 'service'
        store = 'store'

        # 判断数据是否为空
        if isinstance(data,list):
            print("数据异常")
            return

        # 判断数据是否为体验店和服务中心的数据
        # if service not in data["location_type"] | store not in data["location_type"]:
        #     return

        web_car_data_item = WebcarDataItem()
        # 省
        web_car_data_item['provinces'] = data['province_state']
        # 城市
        web_car_data_item['city'] = data['city']
        # 经销商名称
        web_car_data_item['dealerName'] = data['title']
        # 电话号码
        phone = ""
        for j in data['sales_phone']:
            phone = "{}{}:{},".format(phone,j['label'].strip(),j['number'].strip())
        web_car_data_item['salesTel'] = phone

        # phone = ""
        # for j in data['sales_phone']:
        #     if j['label'] == "服务中心电话":
        #         phone = j['number'].strip()
        # web_car_data_item['salesTel'] = phone

        # 地址
        web_car_data_item['address'] = data['address'].strip()

        yield web_car_data_item

        # 营业时间
        # try:
        #     # 正则表达式匹配
        #     pattern = re.compile(r'<[^>]+>')
        #     businessHours = data['hours'].replace("</strong><br />",":")
        #
        #     # 使用sub方法替换
        #     cleaned_str = re.sub(pattern, '', businessHours)
        #     web_car_data_item['businessHours'] = cleaned_str
        # except:
        #     web_car_data_item['businessHours'] = "无"


