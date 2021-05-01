import scrapy
from scrapy_lab1.pipelines import HotelsXMLPipeline


def string_not_empty(str):
    return len(str) > 0


class HotelsSpider(scrapy.Spider):
    name = "uahotels"

    custom_settings = {
        'ITEM_PIPELINES': {
            HotelsXMLPipeline: 300,
        },
        'CLOSESPIDER_PAGECOUNT': 0,
        'CLOSESPIDER_ITEMCOUNT': 20,
    }

    fields = {
        'img': '//img/@src',
        'text': '//*[not(self::script)]/text()',
        'link': '//a/@href'
    }

    start_urls = [
        'https://uahotels.info'
    ]
    allowed_domains = [
        'uahotels.info'
    ]

    # parses uahotels website
    def parse(self, response):
        # get text elements
        text = filter(string_not_empty,
            map(lambda str: str.strip(),
                [text.extract() for text in response.xpath(self.fields["text"])]))


        # get image elements
        images = map(lambda url: ((response.url + url) if url.startswith('/') else url),
            [img_url.extract() for img_url in response.xpath(self.fields["img"])])

        yield {
            'text': text,
            'images': images,
            'url': response.url
        }

        # follow next link
        for link_url in response.xpath(self.fields['link']):
            yield response.follow(link_url.extract(), callback=self.parse)
