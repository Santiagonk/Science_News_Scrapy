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


class SpiderHowStuffworks(scrapy.Spider):
    name = 'howstuffworks'
    start_urls = [
        'https://www.howstuffworks.com'
    ]
    customs_settings = {
        'FEED_URI': 'howstuffworks.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        links_categories = response.xpath(
            '//a[@data-text]/@href'
            ).getall()
        for link in links_categories:
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response, **kwargs):
        links_subcategories = response.xpath(
            '//div[@data-track-gtm="Topics to Explore"]/div/div/a/@href'
            ).getall()
        for link in links_subcategories:
            yield response.follow(link, callback=self.parse_notice)
    def parse_notice(self, response, **kwargs):
        news_links = response.xpath(
            '//div[@class="mb-4"]/div[@data-track-gtm !="Topics to Explore"]//a/@href'
            ).getall()
        for link in news_links:
            yield response.follow(link, callback=self.parse_link,
                                    cb_kwargs= {'url': link})

    def parse_link(self, response, **kwargs):
        items = ScienceNewsItem()
        link = kwargs['url']
        title = response.xpath(
            '//div[contains(@class,"page-title")]/h1/text()'
        ).get()
        if title != None:
            title = title.strip('\n').strip('\t')
        tag = response.xpath(
            '//div[@itemprop]/a/span/text()'
        ).getall()
        author = response.xpath(
            '//p[@class="mb-4"]/a/text()'
        ).get()
        image = response.xpath(
            '//div[@class="media-hero-wrap"]//img/@src'
        ).getall()
        if image != []:
            image = image[1]
        imagen_content = response.xpath(
            '//div[@class="media-body"]/text()'
        ).getall()
        imagecontent = []
        for con in imagen_content:
            imagecontent.append(con.replace('\n','').replace('\t',''))
        date = response.xpath(
            '//p[@class="mb-4"]/span/text()'
        ).get()
        content = response.xpath(
            '//div[@class = "page-content"]//p/descendant-or-self::text()'
        ).getall()
        content_complete = ""
        for cont in content:
            content_complete += cont
        items['url'] = link
        items['tag'] = tag[1:]
        items['title'] = title
        items['author'] = author
        items['image'] = image
        items['image_content'] = imagecontent
        items['date'] = date
        items['content'] = content_complete.strip('Advertisement')

        yield items