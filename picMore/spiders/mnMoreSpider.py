# -*- coding: utf-8 -*-
import scrapy
import operator
from scrapy.http import Request, FormRequest
import urllib
import os
import time
from picMore.items import PicmoreItem
from scrapy.selector import Selector
from scrapy.http import HtmlResponse,Request


class MnmorespiderSpider(scrapy.Spider):
    name = 'mnMoreSpider'
    allowed_domains = ['']
    start_urls = ['http://pornpics.com/']

    def parse(self, response):
        #doc=response.xpath('//ul/li/a/img')
        #selector = scrapy.Selector(response)
        a_href=response.xpath('//ul[@id="tiles"]/li[@class="thumbwook"]/a/@href').extract()
        for href in a_href :
            #当结尾不是jpg且连接中不包含http，从http开始截取作为新的页面（非图片）链接
            if operator.eq(href[-3:],"jpg")==False and "http" in href :
                link="https"+href.split('https')[1:][0]
                yield scrapy.Request(link, callback=self.parse_item,dont_filter = True)
                response = scrapy.Request(link, callback = self.parse,dont_filter = True)
                yield response
            #当结尾是jpg时，href即为所需图片链接
            elif operator.eq(href[-3:],"jpg")==True:
                #items=[]
                item=PicmoreItem()
                item['link']=response.xpath('//ul[@id="tiles"]/li[@class="thumbwook"]/a/img/@href').extract()
                #items.append(item)
                yield item
                #request = scrapy.Request(href, callback=self.parse_item)
                #paths = response.xpath('//ul/li/a[@class="rel-link"]/@href').extract()
                #for path in paths:
                #    #link='https://www.pornpics.com'+path
                #    request = scrapy.Request(path, callback=self.parse_item)
                #    yield request
            #其他情况时，需要拼接链接地址，作为新的页面链接 
            else :
                #paths = response.xpath('//ul/li/a[@class="rel-link"]/@href').extract()
                link='https://www.pornpics.com'+href
                yield scrapy.Request(link, callback=self.parse_item,dont_filter = True)
                response = scrapy.Request(link, callback=self.parse,dont_filter = True)
                #request = scrapy.Request(link, callback=self.parse_item)
                yield response
                #for path in paths:
                #    #link='https://www.pornpics.com'+path
                #    request = scrapy.Request(path, callback=self.parse_item)
                #    yield request
                
        
    def parse_item(self, response):
        #items=[]
        item=PicmoreItem()
        a_href=response.xpath('//ul[@id="tiles"]/li[@class="thumbwook"]/a/@href').extract()
        for href in a_href:
            #当结尾不是jpg且连接中不包含http，从http开始截取作为新的页面（非图片）链接
            if operator.eq(href[-3:],"jpg")==False and "http" in href :
                item['link']=response.xpath('//ul[@id="tiles"]/li[@class="thumbwook"]/a/img/@src').extract()
                yield item
            #当结尾是jpg时，href即为所需图片链接
            elif operator.eq(href[-3:],"jpg")==True:
                item['link']=response.xpath('//ul[@id="tiles"]/li[@class="thumbwook"]/a/@href').extract()
                yield item
            #其他情况时，需要拼接链接地址，作为新的页面链接 
            else :
                item['link']=response.xpath('//ul[@id="tiles"]/li[@class="thumbwook"]/a/img/@src').extract()
                #items.append(item)
                yield item
