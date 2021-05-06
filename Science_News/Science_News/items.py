# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# Extracted data -> Temporary containers (items) -> Storing in database

import scrapy


class ScienceNewsItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    tag = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    image = scrapy.Field()
    image_content = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
