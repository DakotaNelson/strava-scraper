import scrapy

from twisted.internet import reactor, defer
from scrapy.commands import ScrapyCommand
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from strava.spiders.sitemap import SitemapSpider
from strava.spiders.segments import SegmentSpider
from strava.spiders.tiles import TileSpider
from strava.spiders.users import UserSpider
from strava.spiders.activity import ActivitySpider
from strava.spiders.clubs import ClubsSpider
from strava.spiders.routes import RoutesSpider

class CrawlAllCommand(ScrapyCommand):
    def run(self, args, opts):
        runner = CrawlerRunner(get_project_settings())

        @defer.inlineCallbacks
        def crawl():
            # the sitemap populates a list of URLs in mongo
            yield runner.crawl(SitemapSpider)
            # spiders with usemongo=True pull a list of URLs to crawl
            # from mongo and thus must be run after the sitemap spider
            yield runner.crawl(UserSpider, usemongo=True)
            yield runner.crawl(ClubsSpider, usemongo=True)
            yield runner.crawl(RoutesSpider, usemongo=True)
            yield runner.crawl(SegmentSpider, end=1000000)
            yield runner.crawl(ActivitySpider, end=1000000)
            yield runner.crawl(TileSpider)
            reactor.stop()

        crawl()
        reactor.run()

