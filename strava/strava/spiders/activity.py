# -*- coding: utf-8 -*-
import json

import scrapy


class ActivitySpider(scrapy.Spider):
    name = 'activity'
    allowed_domains = ['strava.com']

    def start_requests(self):
        """ yield a URL for each activity """
        max_activity = 200
        for i in range(0,max_activity+1):
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

        activity_object = {
            'full_name': name,
            'url': response.url,
            'activity_id': activity_id,
            'athlete_id': athlete_id,
            'latlng': None # this is set in the next parser
        }

        geo_url = 'https://www.strava.com/stream/{activity_id}?streams%5B%5D=latlng'.format(activity_id=activity_id)
        yield scrapy.Request(
            url=geo_url,
            callback=self.parse_latlng,
            meta={'activity_object': activity_object}
        )

    def parse_latlng(self, response):
        # provided by the previous parsing function
        activity_object = response.meta['activity_object']

        latlng = json.loads(response.body.decode('utf-8'))["latlng"]

        activity_object["latlng"] = latlng

        yield activity_object
