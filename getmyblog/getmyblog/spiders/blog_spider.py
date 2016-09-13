# -*- coding: utf-8 -*-  
from scrapy.selector import HtmlXPathSelector  
from scrapy.contrib.spiders import CrawlSpider,Rule  
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor  
from getmyblog.items import GetmyblogItem  
  
class MoiveSpider(CrawlSpider):  
    name="getmyblog"  
    allowed_domains=["blog.csdn.net"]  
    start_urls=["http://blog.csdn.net/baalhuo/article/list/1"]  
  
    rules=[  
        Rule(SgmlLinkExtractor(allow=(r'http://blog.csdn.net/baalhuo/article/list/\d+'))),  
        Rule(SgmlLinkExtractor(allow=(r'http://blog.csdn.net/baalhuo/article/details/\d+')),callback="parse_item"),        
    ]  
  
    def parse_item(self,response):
		filename = response.url.split("/")[-1] + '.html'
		with open(filename, 'wb') as f:
			f.write(response.body)
			f.close()
		
        #sel=HtmlXPathSelector(response)
        #item=GetmyblogItem()  
        #item['article_name']=sel.select('//*[@class="link_title"]/a/text()').extract()  
        #item['public_time']=sel.select('//*[@class="link_postdate"]/text()').extract()  
        #item['read_num']=sel.select('//*[@class="link_view"]/text()').extract()  

        #return item	