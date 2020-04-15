# -*- coding: utf-8 -*-
import re
import json
import logging
import pymongo
import scrapy


class RoutesSpider(scrapy.Spider):
    name = 'routes'
    allowed_domains = ['strava.com']

    def start_requests(self):
        """ yield a URL for each route """
        # get our options
        start = int(getattr(self, 'start', 0))
        end = int(getattr(self, 'end', 1000))
        usemongo = bool(getattr(self, 'usemongo', False))

        if usemongo:
            mongo_uri = self.settings.get('MONGO_URI')
            mongo_db = self.settings.get('MONGO_DB')

            try:
                logging.info("Starting route spider with Mongo query")
                client = pymongo.MongoClient(mongo_uri)
                db = client[mongo_db]
                routes = db.sitemap.find({"url_category": "routes"})
                for route in routes:
                    yield scrapy.Request(
                        url=route['url'],
                        meta = {'dont_redirect': True,
                                'handle_httpstatus_list': [302]},
                        callback=self.parse
                    )
            finally:
                self.client.close()

        else:
            logging.info("Starting route spider with range {} to {}".format(start, end+1))
            for i in range(start,end+1):
                url = 'https://www.strava.com/routes/{}'.format(i)
                yield scrapy.Request(
                    url=url,
                    meta = {'dont_redirect': True,
                            'handle_httpstatus_list': [302]},
                    callback=self.parse
                )

    def parse(self, response):
        route_id = response.url.split('/')[-1]

        try:
            route_name = response.css(".route-name h1::text").extract_first().strip()
        except:
            route_name = None

        try:
            user = json.loads(response.css('*').re("Strava\.Models\.Athlete\((.*)\)")[0])
        except IndexError:
            user = None

        try:
            route_data = json.loads(response.css('*').re("\.routeData\((.*)\)")[0])
        except IndexError:
            route_data = None

        route = {
            "route_id": int(route_id),
            "name": route_name,
            "created_by": user,
            "metadata": route_data
        }

        yield route
