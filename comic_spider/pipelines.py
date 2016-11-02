# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from .mailer import RemindMailer

class ComicSpiderPipeline(object):

    collection_name = 'onepiece'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, spider):
        return cls(
            mongo_uri=spider.settings.get('MONGO_URI'),
            mongo_db=spider.settings.get('MONGO_DATABASE', 'onepiece')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if not self.db[self.collection_name].find_one(dict(item)):
            #self.db[self.collection_name].insert(dict(item))
            remind_mailer = RemindMailer.config_for(spider.settings)
            remind_mailer.async_send(spider)
        return item
