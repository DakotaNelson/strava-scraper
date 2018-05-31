# -*- coding: utf-8 -*-
import json

import scrapy


class SegmentSpider(scrapy.Spider):
    name = 'segments'
    allowed_domains = ['strava.com']

    def start_requests(self):
        """ yield a URL for each segment """
        start = int(getattr(self, 'start', 0))
        end = int(getattr(self, 'end', 1000))

        for i in range(start,end+1):
            url = 'https://www.strava.com/segments/{}'.format(i)
            yield scrapy.Request(
                url=url,
                meta = {'dont_redirect': True,
                        'handle_httpstatus_list': [302]},
                callback=self.parse
            )

    def parse(self, response):
        # ID of the location
        segment_id = response.url.split('/')[-1]

        # name of the location
        # e.g. "Stanmore Lane Down"
        full_name = response.css('[data-full-name]::text').extract_first()

        # location of the... uh... location
        # e.g. "Winchester, Hampshire, United Kingdom"
        try:
            location = response.css('.location').extract_first().split('\n')[-2]
        except AttributeError:
            return # we probably got a redirect

        leaderboard_rows = response.css('tbody tr')

        def parse_row(row):
            name = row.css('td:nth-child(2)::text').extract_first()
            activity_id = row.css('td a::attr(href)').extract_first().split('/')[-1]
            return {
                'full_name': name,
                'activity_id': activity_id
            }

        people = []
        for row in leaderboard_rows:
            people.append(parse_row(row))

        segment_object = {
            'segment_id': segment_id,
            'full_name': full_name,
            'location': location,
            'people': people,
            'latlng': None # this is set in the next parser
        }

        geo_url = 'https://www.strava.com/stream/segments/{location_id}?streams%5B%5D=latlng'.format(location_id=segment_id)
        yield scrapy.Request(
            url=geo_url,
            callback=self.parse_latlng,
            meta={'segment_object': segment_object}
        )

    def parse_latlng(self, response):
        # provided by the previous parsing function
        segment_object = response.meta['segment_object']

        latlng = json.loads(response.body.decode('utf-8'))["latlng"]

        segment_object["latlng"] = latlng

        yield segment_object
