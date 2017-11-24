# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib
from picMore import settings


class PicmorePipeline(object):
    def process_item(self, item, spider):
        #dirPath='%s'%(settings.IMAGES_STORE)
        links=item['link']
        #alt=item['alt'] 
        for link in links:
            
            name=link[link.find("com")+15:]
            path="E:\\pic\\"+name
            urllib.request.urlretrieve(link, path)
        return item