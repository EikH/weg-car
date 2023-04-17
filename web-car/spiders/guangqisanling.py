import scrapy

from ..items import WebcarDataItem


class GuangqisanlingSpider(scrapy.Spider):
    name = "guangqisanling"

    # 允许处理的响应码
    handle_httpstatus_list = [304,301,302]

    # 允许访问的域
    allowed_domains = ["www.gmmc.com.cn", "gmmc.com.cn"]

    start_urls = ["https://www.gmmc.com.cn/AppBuildFile/library/hq/jsonresources/all/provinces.txt"]

    city_url = "https://www.gmmc.com.cn/AppBuildFile/library/hq/jsonresources/all/{}city.txt"
    data_url = "https://www.gmmc.com.cn/AppBuildFile/library/hq/jsonresources/all/{}dealer.json"

    def parse(self, response):
        data = response.json()
        for i in data:
            province_id = i['PROVINCE_ID']
            yield scrapy.Request(url=self.city_url.format(province_id), callback=self.parse_city_page,dont_filter=True)

    def parse_city_page(self, response):
        data = response.json()
        for i in data:
            city_id = i['CITY_ID']
            yield scrapy.Request(url=self.data_url.format(city_id), callback=self.parse_data_page,dont_filter=True)

    def parse_data_page(self, response):
        datas = response.json()
        for i in datas:
            web_car_data_item = WebcarDataItem()
            # 省
            web_car_data_item['provinces'] = i['PROVINCE_NAME'].strip()
            # 城市
            web_car_data_item['city'] = i['CITY_NAME'].strip()
            # 经销商名称
            web_car_data_item['dealerName'] = i['DEALER_NAME']
            # 销售电话
            web_car_data_item['salesTel'] = i['SALES_PHONE']
            # 地址
            web_car_data_item['address'] = i['ADDRESS']
            # 营业时间
            web_car_data_item['afterSalesTel'] = i['AFTER_SALES_PHONE']
            yield web_car_data_item
