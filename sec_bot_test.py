import unittest
import json

from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, task

from sec_bot import SecSpider

ciks = ['18532','1367024', '780507', '0001512693', '0001196871']

items={}
def add_item(item, spider):
    items[spider.cik] = item

def setup_crawler(spider_class, **kwargs):
    spider = spider_class(**kwargs)
    _cik = kwargs['cik']
    settings = get_project_settings()
    crawler = Crawler(spider_class, settings)
    crawler.crawl(**kwargs)
    crawler.signals.connect(add_item, signals.item_scraped)
    return spider

for cik in ciks:
    setup_crawler(
        spider_class=SecSpider,
        cik=cik
    )

task.deferLater(reactor, 1, reactor.stop)
reactor.run()

class SpidersTests(unittest.TestCase):
  def test_spider(self):
      for cik in ciks:
          with open("outputs/{}.json".format(cik)) as file:
              self.assertEqual(items[cik], json.load(file))
