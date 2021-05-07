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


class SpiderNature(scrapy.Spider):
    name = 'nature'
    start_urls = [
        'https://www.nature.com'
    ]
    customs_settings = {
        'FEED_URI': 'nature.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        news_links = response.xpath('//h3[@itemprop="name headline"]/a/@href').getall()
        for link in news_links:
            yield response.follow(link, callback=self.parse_link,
                                    cb_kwargs= {'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        items = ScienceNewsItem()
        link = kwargs['url']
        title = response.xpath(
            '//h1[@class="header-default__title___2wL7r"]/text()'
        ).get()
        tag = response.xpath(
            '//li[@class="subject"]/a/text()'
        ).getall()
        author = response.xpath(
            '//li[@class="c-author-list__item"]/a/text()'
        ).get()
        image = response.xpath(
            '//figure[@class="figure"]//img/@data-src'
        ).get()
        image_content = response.xpath(
            '//figure[@class="figure"]//p//text()'
        ).getall()
        imagecontent = []
        for con in image_content:
            imagecontent.append(con)
        date = response.xpath(
            '//time[@itemprop="datePublished"]/text()'
        ).get()
        content = response.xpath(
            '//div[@class="article__body cleared"]/*//text()'
        ).getall()
        content_complete = ""
        for cont in content:
            if cont not in image_content:
                content_complete += cont.strip('\n').strip() + " "
        items['url'] = link
        items['tag'] = tag
        items['title'] = title
        items['author'] = author
        items['image'] = image
        items['image_content'] = image_content
        items['date'] = date
        items['content'] = content_complete

        yield items