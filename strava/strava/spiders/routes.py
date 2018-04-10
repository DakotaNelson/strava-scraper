# -*- coding: utf-8 -*-
import re
import logging
import pymongo
import scrapy


class RoutesSpider(scrapy.Spider):
    name = 'routes'
    allowed_domains = ['strava.com']

    def start_requests(self):
        """ yield a URL for each route """
        # get our options
        start = getattr(self, 'start', 0)
        end = getattr(self, 'end', 1000)
        usemongo = bool(getattr(self, 'usemongo', False))

        if usemongo:
            mongo_uri = self.settings.get('MONGO_URI')
            mongo_db = self.settings.get('MONGO_DB')

            try:
                logging.info("Starting route spider with Mongo query")
                client = pymongo.MongoClient(mongo_uri)
                db = client[mongo_db]
                routes = db.sitemap.find({"url_category": "routes"})
                logging.info("Route spider found {} routes".format(len(routes)))
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

        route_name = response.css(".route-name h1::text").extract_first().strip()

        user = json.loads(response.css('*').re("Strava\.Models\.Athlete\((.*)\)")[0])
        route_data = json.loads(response.css('*').re("\.routeData\((.*)\)")[0])

        route = {
            "route_id": route_id,
            "name": route_name,
            "created_by": user,
            "metadata": route_data
        }

        yield route
