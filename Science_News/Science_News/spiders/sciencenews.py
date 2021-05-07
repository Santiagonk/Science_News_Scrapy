import scrapy
from ..items import ScienceNewsItem
# Xpath

# categories links = '//a[@data-text]/@href'
# sub categories links = '//div[@data-track-gtm="Topics to Explore"]/div/div/a/@href'
# news links = '//div[@class="mb-4"]/div[@data-track-gtm !="Topics to Explore"]//a/@href'
# tags = '//div[@itemprop]/a/span/text()'
# title = '//div[contains(@class,"page-title")]/h1/text()'
# autor = '//span[@class="signature"]/text()'
# image = '//img[@class="RichTextAlignCenter"]/@src'
# image content = '//div[@class="new_text "]/p/span/text()'
# date = '//span[@class="date"]/text()'
# content = '//div[@class="new_text "]/p/span[notow]/text()'


class SpiderScienceNews(scrapy.Spider):
    name = 'sciencenews'
    start_urls = [
        'https://www.sciencenews.org'
    ]
    customs_settings = {
        'FEED_URI': 'howstuffworks.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        links_categories = response.xpath(
            '//a[contains(@class, "topics-megamenu")]/@href'
            ).getall()
        for link in links_categories:
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response, **kwargs):
        links_subcategories = response.xpath(
            '//a[contains(@class, "term-feature-header")]/@href'
            ).getall()
        for link in links_subcategories:
            yield response.follow(link, callback=self.parse_notice)

    def parse_notice(self, response, **kwargs):
        news_links = response.xpath(
            '//h3[contains(@class, "title")]/a/@href'
            ).getall()
        for link in news_links:
            yield response.follow(link, callback=self.parse_link,
                                    cb_kwargs= {'url': link})

    def parse_link(self, response, **kwargs):
        items = ScienceNewsItem()
        link = kwargs['url']
        title = response.xpath(
            '//h1[@class="header-default__title___2wL7r"]/text()'
        ).get()
        tag = response.xpath(
            '//span[@class="header-default__eyebrow___b3lhS"]/a/text()'
        ).getall()
        tags = []
        for i in tag:
            tags.append(i.strip('\n').strip('\t'))
        author = response.xpath(
            '//span[@class="byline author vcard"]/a/text()'
        ).get()
        image = response.xpath(
            '//figure[@class="header-default__figure___1N2fo"]/div/img/@src'
        ).getall()
        image_author = response.xpath(
            '//span[@class="header-default__credit___34nDz"]/p/text()'
        ).getall()
        try:
            image_author = image_author[0]
        except:
            image_author = ""
        imagen_content = response.xpath(
            '//span[@class="header-default__caption___1B6mW"]/p/text()'
        ).getall()
        try:
            imagen_content = imagen_content[0]
        except:
            imagen_content = ""
        imagecontent = imagen_content + ' ' + image_author
        date = response.xpath(
            '//p[@class="byline__published___3GjAo"]/time[@class]/text()'
        ).get()
        content = response.xpath(
            '//div[@class="single__content___Cm2ty"]/div/p/descendant-or-self::text()'
        ).getall()
        content_complete = ""
        for cont in content:
            content_complete += cont + " "
        items['url'] = link
        items['tag'] = tags
        items['title'] = title
        items['author'] = author
        items['image'] = image
        items['image_content'] = imagecontent
        items['date'] = date
        items['content'] = content_complete.strip('Advertisement')

        yield items