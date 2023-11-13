# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PttEducationItem(scrapy.Item):
    日期 = scrapy.Field()
    作者 = scrapy.Field()
    標題 = scrapy.Field()
    網址 = scrapy.Field()
