# -*- coding: utf-8 -*-
import math

import scrapy

class TileSpider(scrapy.Spider):
    name = 'tile_scraper'

    allowed_domains = [
            'heatmap-external-a.strava.com',
            'heatmap-external-b.strava.com',
            'heatmap-external-c.strava.com'
    ]

    def start_requests(self):
        """ calculate out all the tiles we need to get, then yield each tile's
        URL for the spider to grab """
        max_zoom = 1
        for zoom in range(0,max_zoom+1):
            tile_extent = 2 ** zoom
            for x in range(tile_extent):
                for y in range(tile_extent):
                    url = 'http://heatmap-external-a.strava.com/tiles/all/hot/{zoom}/{x}/{y}.png'.format(
                            zoom=zoom,
                            x=x,
                            y=y
                    )
                    yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # take the ".png" off,
        # then split by "/",
        # then take only the last 3 elements
        zoom, x, y = response.url[:-4].split("/")[-3:]
        filename = "{zoom}.{x}.{y}.png".format(
                zoom=zoom,
                x=x,
                y=y
        )
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log("Saved {}".format(filename))
