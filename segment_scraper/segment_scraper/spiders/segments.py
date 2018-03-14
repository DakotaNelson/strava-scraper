# -*- coding: utf-8 -*-
import scrapy


class SegmentSpider(scrapy.Spider):
    name = 'segment_scraper'
    allowed_domains = ['strava.com']

    start_urls = ['http://strava.com/']

    def start_requests(self):
        """ yield a URL for each segment """
        max_segment = 100
        for i in range(0,max_segment+1):
            url = 'https://www.strava.com/segments/{}'.format(i)
            yield scrapy.Request(
                url=url,
                meta = {'dont_redirect': True,
                        'handle_httpstatus_list': [302]},
                callback=self.parse
            )

    def parse(self, response):
        # ID of the location
        location_id = response.url.split('/')[-1]

        # name of the location
        # e.g. "Stanmore Lane Down"
        full_name = response.css('[data-full-name]::text').extract_first()

        # location of the... uh... lcation
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

        yield {
            'id': location_id,
            'full_name': full_name,
            'location': location,
            'people': people,
            'latlng': None # this is set in the pipeline
        }
