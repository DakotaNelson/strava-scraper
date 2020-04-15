# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.spidermiddlewares.httperror import HttpError


class ActivitySpider(scrapy.Spider):
    name = 'activity'
    allowed_domains = ['strava.com']

    def start_requests(self):
        """ yield a URL for each activity """
        start = int(getattr(self, 'start', 0))
        end = int(getattr(self, 'end', 1000))

        for i in range(start,end+1):
            url = 'https://www.strava.com/activities/{}'.format(i)
            yield scrapy.Request(
                url=url,
                meta = {'dont_redirect': True,
                        'handle_httpstatus_list': [302]},
                callback=self.parse
            )

    def parse(self, response):
        name = response.css('div.description > h2 > a::text').extract_first()

        if name is None:
            return # not a valid page

        activity_id = response.url.split('/')[-1]

        athlete_id = response.css('div.description > h2 > a::attr(href)').extract_first().split('/')[-1]

        geo_url = 'https://www.strava.com/stream/{activity_id}?streams%5B%5D=latlng'.format(activity_id=activity_id)
        activity_object = {
            'full_name': name,
            #'url': response.url,
            'activity_id': int(activity_id),
            'athlete_id': int(athlete_id),
            #'latlng_url': geo_url,
            'path': None # this is set in the next parser
        }

        yield scrapy.Request(
            url=geo_url,
            callback=self.parse_latlng,
            meta={'activity_object': activity_object,
                  'handle_httpstatus_list': [429]},
        )

    def parse_latlng(self, response):
        # provided by the previous parsing function
        activity_object = response.meta['activity_object']

        if response.status == 429:
            # we got blocked
            logging.warning("Activity spider got a rate-limit error 429")
            pass
        else:
            # we're good, yay!
            latlng = json.loads(response.body.decode('utf-8'))["latlng"]
            if len(latlng) > 1:
                activity_object["path"] = {
                        "type": "LineString",
                        "coordinates": [[y,x] for x,y in latlng]
                    }
            elif len(latlng) == 1:
                activity_object["path"] = {
                        "type": "LineString",
                        # need len(coordinates) > 1 so we just add two
                        # identical points /shrug
                        "coordinates": [[y,x] for x,y in latlng + latlng]
                    }
            else: # length zero or some weird case
                activity_object["path"] = None


        yield activity_object
