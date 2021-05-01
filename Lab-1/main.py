from lxml import etree
from scrapy.crawler import CrawlerProcess
from scrapy_lab1.spiders.HotelsSpider import HotelsSpider

process = CrawlerProcess({})
# start crawler
process.crawl(HotelsSpider)

process.start()

root = None

# write parsed info to uahotels.xml
with open('results/uahotels.xml', 'r') as file:
    root = etree.parse(file)

# task 2 console output
pagesCount = root.xpath('count(//page)')
textFragmentsCount = root.xpath('count(//fragment[@type="text"])')
print('Total text fragments count %f' % textFragmentsCount)
print('Average count of text fragments per page %f' % (textFragmentsCount / pagesCount))