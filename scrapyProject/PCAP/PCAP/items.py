# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PcapItem(scrapy.Item):
    # define the fields for your item here like:
    price = scrapy.Field()
    url = scrapy.Field()
    shopId = scrapy.Field()
    competitorId = scrapy.Field()
    productId = scrapy.Field()
