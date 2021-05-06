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


class SpiderNoticiasDeLaCiencia(scrapy.Spider):
    name = 'noticiasdelaciencia'
    start_urls = [
        'https://noticiasdelaciencia.com'
    ]
    customs_settings = {
        'FEED_URI': 'noticiasdelaciencia.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        links_categories = response.xpath('//ul[@class="topmenu"]/li/a/@href').getall()
        for link in links_categories:
            yield response.follow(link, callback=self.parse_category, 
                                  cb_kwargs= {'url': response.urljoin(link)})

    def parse_category(self, response, **kwargs):
        news_links = response.xpath('//h1[@class="title"]/a/@href').getall()
        for link in news_links:
            yield response.follow(link, callback=self.parse_link, 
                                  cb_kwargs= {'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        items = ScienceNewsItem()
        link = kwargs['url']
        title = response.xpath(
            '//h1[@class="new_title"]/text()'
        ).get()
        tag = response.xpath(
            '//h4[@class="new_pretitle"]/text()'
        ).get()
        author = response.xpath(
            '//span[@class="signature"]/text()'
        ).get()
        image = response.xpath(
            '//img[@class="RichTextAlignCenter"]/@src'
        ).get()
        image_content = response.xpath(
            '//div[@class="new_text "]/p/span/text()'
        ).getall()
        date = response.xpath(
            '//span[@class="date"]/text()'
        ).get()
        content = response.xpath(
            '//div[@class="new_text "]/p/text()'
        ).getall()
        items['url'] = link
        items['tag'] = tag
        items['title'] = title
        items['author'] = author
        items['image'] = image
        items['image_content'] = image_content
        items['date'] = date
        items['content'] = content

        yield items