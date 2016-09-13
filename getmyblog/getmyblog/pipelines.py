# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')  
from scrapy.exceptions import DropItem  
from scrapy.conf import settings  
from scrapy import log  

class GetmyblogPipeline(object):
    def __init__(self):  
        print 'GetmyblogPipeline'  
  
    def process_item(self, item, spider):  
        #Remove invalid data  
        #valid = True  
        #for data in item:  
          #if not data:  
            #valid = False  
            #raise DropItem("Missing %s of blogpost from %s" %(data, item['url']))  
            #print 'crawl no data.....\n'  
        #if valid:  
        #Insert data into txt  
        input = open('data.txt', 'a')
        input.write('article_name:'+item['article_name'][0]+'   ');  
        input.write('public_time:'+item['public_time'][0]+'   ');  
        input.write('read_num:'+item['read_num'][0]+'   ');  
        input.close()  
  
        return item 
