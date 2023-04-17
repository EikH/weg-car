import scrapy

from ..items import WebcarDataItem

class DongfengbentianSpider(scrapy.Spider):
    name = "dongfengbentian"
    allowed_domains = ["www.dongfeng-honda.com"]
    start_urls = ["https://www.dongfeng-honda.com/dot_query.shtml"]

    def parse(self, response):
        url = "https://www.dongfeng-honda.com/index/get_city_bypid/{}"

        # 获取城市和城市id  xpath列表
        provinces_id = response.xpath('//*[@id="province"]/option/@province_id')
        provinces = response.xpath('//*[@id="province"]/option/text()')[1:]

        body = {
            "dealer_type": "dot_query",
            "ajax": "true"
        }

        for index, value in zip(provinces_id, provinces):
            # 获取城市和城市id数据
            province_id = index.get()
            province = value.get()

            yield scrapy.FormRequest(url=url.format(province_id), formdata=body, callback=self.city_parse, meta={
                "province": province
            })

    def city_parse(self, response):

        url = 'https://www.dongfeng-honda.com/dot_query.shtml?province={}&city={}'

        # 省份和城市
        citys = response.xpath('//option/text()')[1:]
        province = response.meta["province"]

        for value in citys:
            city = value.get()

            yield scrapy.Request(url=url.format(province,city), callback=self.data_parse, meta={
                "province": province,
                "city": city
            })

    def data_parse(self, response):
        # 经销商列表xpath
        dealerNames = response.xpath('//*[@id="pagetop"]/div/div/div/section/div[1]/section/ul/li/h4/text()')[2:]
        # 地址列表xpath
        addresss = response.xpath('//*[@id="pagetop"]/div/div/div/section/div[1]/section/ul/li/p[1]/text()')
        # 销售电话列表xpath
        salesTels = response.xpath('//*[@id="pagetop"]/div/div/div/section/div[1]/section/ul/li/p[2]/text()')
        # 售后电话列表xpath
        afterSalesTels = response.xpath('//*[@id="pagetop"]/div/div/div/section/div[1]/section/ul/li/p[3]/text()')

        provinces = response.meta['province']
        city = response.meta['city']

        for dealerName,address,salesTel,afterSalesTel in zip(dealerNames,addresss,salesTels,afterSalesTels):
            web_car_data_item = WebcarDataItem()
            # 省
            web_car_data_item['provinces'] = provinces
            # 城市
            web_car_data_item['city'] = city
            # 经销商名称
            web_car_data_item['dealerName'] = dealerName.get()
            # 地址
            web_car_data_item['address'] = address.get()
            # 销售电话
            web_car_data_item['salesTel'] = salesTel.get().split('：')[1]
            # 售后电话
            web_car_data_item['afterSalesTel'] = afterSalesTel.get().split('：')[1]

            print(web_car_data_item)
            yield web_car_data_item
