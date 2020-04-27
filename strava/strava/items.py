# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Activity(scrapy.Item):
    full_name = scrapy.Field(serializer=str)
    activity_id = scrapy.Field(serializer=int)
    athlete_id = scrapy.Field(serializer=int)
    path = scrapy.Field(serializer=dict)

# not yet used, untested
class Club(scrapy.Item):
    club_id = scrapy.Field(serializer=int)
    club_name = scrapy.Field(serializer=str)
    club_location = scrapy.Field(serializer=str)
    club_members = scrapy.Field(serializer=list)
    club_num_members = scrapy.Field(serializer=int)

# not yet used, untested
class Route(scrapy.Item):
    route_id = scrapy.Field(serializer=int)
    name = scrapy.Field(serializer=str)
    created_by = scrapy.Field(serializer=int)
    metadata = scrapy.Field(serializer=str)

# not yet used, untested
class Segment(scrapy.Item):
    segment_id = scrapy.Field(serializer=int)
    full_name = scrapy.Field(serializer=str)
    location = scrapy.Field(serializer=str)
    people = scrapy.Field()
    path = scrapy.Field(serializer=dict)

class User(scrapy.Item):
    full_name = scrapy.Field(serializer=str)
    avatar = scrapy.Field(serializer=str)
    first_name = scrapy.Field(serializer=str)
    last_name = scrapy.Field(serializer=str)
    user_id = scrapy.Field(serializer=int)
    location = scrapy.Field(serializer=str)
    uploaded_images = scrapy.Field(serializer=list)
    num_following = scrapy.Field(serializer=int)
    num_followers = scrapy.Field(serializer=int)
    following = scrapy.Field(serializer=list)
    followers = scrapy.Field(serializer=list)
