import scrapy 
from ..items import ScienceNewsItem
# Xpath

# categories links = //ul[@class="topmenu"]/li/a/@href
# news links = //h1[@class="title"]/a/@href
# tags = '//h4[@class="new_pretitle"]/text()'
# title = '//h1[@class="new_title"]/text()'
# autor = '//span[@class="signature"]/text()'
# image = '//img[@class="RichTextAlignCenter"]/@src'
# image content = '//div[@class="new_text "]/p/span/text()'
# date = '//span[@class="date"]/text()'
# content = '//div[@class="new_text "]/p/span[notow]/text()'


class MuyInteresante(scrapy.Spider):
    name = 'muyinteresante'
    start_urls = [
        'https://www.muyinteresante.es'
    ]
    customs_settings = {
        'FEED_URI': 'muyinteresant.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        links_categories = response.xpath('//li[@class="dropdown "]/a/@href').getall()
        for link in links_categories:
            yield response.follow(link, callback=self.parse_category,
                                    cb_kwargs= {'url': response.urljoin(link)})

    def parse_category(self, response, **kwargs):
        news_links = response.xpath('//div[@class="box--text--container"]/h2/a/@href').getall()
        for link in news_links:
            yield response.follow(link, callback=self.parse_link,
                                    cb_kwargs= {'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        items = ScienceNewsItem()
        link = kwargs['url']
        title = response.xpath(
            '//h1[contains(@class, "title")]/text()'
        ).get()
        tag = response.xpath(
            '//h3[contains(@class, "tags")]//a/text()'
        ).getall()
        tags = []
        for i in tag:
            tags.append(i.strip('#'))
        author = response.xpath(
            '//div[contains(@class, "author")]//h3/text()'
        ).get()
        image = response.xpath(
            '//figure[@class]/img/@src'
        ).get()
        image_content = response.xpath(
            '//div[@class="paragraph--image--caption"]/text()'
        ).get()
        image_sumary = ''
        image_sumary = response.xpath(
            '//div[@class="paragraph--image--caption"]/text()'
        ).get()
        imagecontent = image_sumary + " " + image_content
        date = response.xpath(
           '//time[@class]/text()'
        ).get()
        content = response.xpath(
            '//div[@class="paragraph--text"]/*//text()'
        ).getall()
        content_complete = ""
        for cont in content:
            if cont != '\xa0':
                content_complete += cont
        items['url'] = link
        items['tag'] = tags
        items['title'] = title
        items['author'] = author
        items['image'] = image
        items['image_content'] = imagecontent
        items['date'] = date
        items['content'] = content_complete

        yield items