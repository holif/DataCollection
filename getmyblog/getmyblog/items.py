# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field


class GetmyblogItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_name = Field() #文章名字  
    public_time = Field()  #发表时间  
    read_num = Field()     #阅读数量  

