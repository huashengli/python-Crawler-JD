# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sort_url=scrapy.Field()
    sort_name = scrapy.Field()
    num=scrapy.Field()
    product_id=scrapy.Field()
    #product_color=scrapy.Field()
    #product_img = scrapy.Field()
    product_brand=scrapy.Field()
    shop_name=scrapy.Field()
    discription_detail=scrapy.Field()
    standard= scrapy.Field()
    product_price = scrapy.Field()
    product_href = scrapy.Field()
    content = scrapy.Field()