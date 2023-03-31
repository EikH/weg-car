# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 数据对象
class WebcarDataItem(scrapy.Item):
    # define the fields for your item here like:
    # 经销商名称
    dealerName = scrapy.Field()
    # 省
    provinces = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 销售瘦电话
    salesTel = scrapy.Field()
    # 地区
    districtName = scrapy.Field()
    # 售后电话
    afterSalesTel = scrapy.Field()
    # 营业时间
    businessHours = scrapy.Field()
    # 公司全称
    companyName = scrapy.Field()




