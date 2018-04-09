# -*- coding: utf-8 -*-
import re
import logging

import scrapy


class SitemapSpider(scrapy.Spider):
    name = 'sitemap'
    allowed_domains = ['strava.com', 'cloudfront.net']
    start_urls = ['https://www.strava.com/robots.txt']

    def parse(self, response):
        # this url tells us where the root XML file defining all the sitemaps is
        main_url = response.css('body').re('http.*sitemap.xml')[0]
        yield scrapy.Request(main_url, callback=self.parse_sitemap_root)

    def parse_sitemap_root(self, response):
        response.selector.register_namespace('xmlns', "http://www.sitemaps.org/schemas/sitemap/0.9")
        # this gets a list of URLs, each of which leads to an actual sitemap
        sitemap_urls = response.xpath("./xmlns:sitemap/xmlns:loc/text()").re('http.*sitemap\d{1,3}.xml')
        for url in sitemap_urls:
            yield scrapy.Request(url, callback=self.parse_sitemap)

    def parse_sitemap(self, response):
        # parse an actual sitemap here
        response.selector.register_namespace('xmlns', "http://www.sitemaps.org/schemas/sitemap/0.9")
        all_urls = response.selector.xpath('//xmlns:url/xmlns:loc/text()').extract()
        for url in all_urls:
            yield {'url': url, 'url_category': url.split('/')[3]}
