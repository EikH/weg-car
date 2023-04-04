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
        # 判断数据是否为空
        if isinstance(data,list):
            print("数据异常")
            return

        # # 判断数据是否为体验店的数据
        # if len(data["location_type"]) < 2:
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
        # # 营业时间
        # try:
        #     web_car_data_item['businessHours'] = data['hours'].replace('<p><strong>','').replace("</strong><br />",":").replace(
        #         "</p>", ",")
        # except:
        #     web_car_data_item['businessHours'] = "无"
        # 地址
        web_car_data_item['address'] = data['address'].strip()

        yield web_car_data_item


