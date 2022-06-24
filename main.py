import time

from twisted.internet import defer # reactor,
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from jewellery_scrapy.spiders.proxies_scrapper import ProxySpider
from jewellery_scrapy.spiders.brosway import BroswaySpider
from jewellery_scrapy.spiders.tedora import TedoraSpider
from jewellery_scrapy.spiders.breuning import BreuningSpider
from jewellery_scrapy.spiders.boccadamo import BoccadamoSpider
from jewellery_scrapy.spiders.gioiapura import GioiapuraSpider

from scrapy.utils.reactor import install_reactor

if __name__ == "__main__":

    # configure_logging()
    # settings = get_project_settings()
    # runner = CrawlerRunner(settings=settings)
    # runner.crawl(ProxySpider)
    # runner.crawl(BroswaySpider)
    # d = runner.join()
    # d.addBoth(lambda _: reactor.stop())
    #
    # reactor.run()  # the script will block here until all crawling jobs are



    configure_logging()
    settings = get_project_settings()
    # runner = CrawlerRunner(settings)
    #
    # @defer.inlineCallbacks
    # def crawl():
    #     yield runner.crawl(ProxySpider)
    #     #yield runner.crawl(BroswaySpider)
    #     #yield runner.crawl(TedoraSpider)
    #     #yield runner.crawl(BreuningSpider)
    #     yield runner.crawl(BoccadamoSpider)
    #     reactor.stop()
    #
    # crawl()
    # reactor.run()




    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    process = CrawlerProcess(settings=settings)
    process.crawl(GioiapuraSpider)
    process.start()