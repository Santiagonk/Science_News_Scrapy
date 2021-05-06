# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# scraper data -> Item Containers -> Json/csv files
# Scraper data -> Item containers -> Pipeline -> Database
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScienceNewsPipeline:
    def process_item(self, item, spider):
        
        print('Pipeline: ' + item['title'])
        return item
