# -*- coding: utf-8 -*-
import re
import logging
import pymongo
import scrapy


class UserSpider(scrapy.Spider):
    name = 'users'
    allowed_domains = ['strava.com']

    def start_requests(self):
        """ yield a URL for each user """
        # get our options
        start = getattr(self, 'start', 0)
        end = getattr(self, 'end', 1000)
        usemongo = bool(getattr(self, 'usemongo', False))

        if usemongo:
            mongo_uri = self.settings.get('MONGO_URI')
            mongo_db = self.settings.get('MONGO_DB')

            try:
                logging.info("Starting user spider with Mongo query")
                client = pymongo.MongoClient(mongo_uri)
                db = client[mongo_db]
                athletes = db.sitemap.find({"url_category": "athletes"})
                for athlete in athletes:
                    yield scrapy.Request(
                        url=athlete['url'],
                        meta = {'dont_redirect': True,
                                'handle_httpstatus_list': [302, 503]},
                        callback=self.parse
                    )
            finally:
                client.close()

        else:
            logging.info("Starting user spider with range {} to {}".format(start, end+1))
            for i in range(start,end+1):
                url = 'https://www.strava.com/athletes/{}'.format(i)
                yield scrapy.Request(
                    url=url,
                    meta = {'dont_redirect': True,
                            'handle_httpstatus_list': [302, 503]},
                    callback=self.parse
                )


    def parse(self, response):
        user_url = response.url
        user_id = response.url.split('/')[-1]

        title_text = response.css('title::text').re('Strava .+ Profile')
        if len(title_text) < 1:
            # invalid, we probably got a redirect/rate limit/etc.
            return

        full_name = response.css('h1.bottomless::text').extract_first()

        first_name = None
        last_name = None
        try:
            tokens = full_name.split(' ')
            first_name, last_name = tokens[0], tokens[-1]
        except ValueError:
            logging.error("Unable to parse name: {}".format(full_name))
        except AttributeError:
            logging.error("Unable to parse name: {}".format(full_name))

        # the user's self-reported location
        location = response.css('div.location::text').extract_first()

        # recently uploaded images
        uploaded_images = response.css('.photostream img::attr(src)').extract()

        # the user's avatar
        avatar = response.css('.athlete-hero .avatar-img::attr(src)').extract_first()

        # this regex can extract the user's ID from their strava profile photo
        # (unless they use a facebook/google profile photo)
        id_from_avatar_url = re.compile(r'cloudfront.net\/pictures\/athletes\/(\d+)')

        def process_follows(following):
            """ given a CSS selection of users that this user is following or
            being followed by, return a list of dict objects representing
            those users """
            names = following.css('.avatar::attr(title)').extract()
            avatars = following.css('.avatar-img::attr(src)').extract()
            follows = []
            for name,avatar_url in zip(names, avatars):
                try:
                    user_id = id_from_avatar_url.search(avatar_url).group().split('/')[-1]
                except AttributeError:
                    # didn't find it
                    user_id = None
                follows.append({
                    'name': name,
                    'avatar': avatar_url,
                    'user_id': user_id
                })
            return follows

        # number of users they're following
        num_following = response.css('div.social.section :nth-child(1) span::text').extract_first()[2:]
        # names of "following"
        # PROTIP: there are only 6... but which 6 changes on every refresh!
        following = response.css('.social.section ul.grid-inline')[0]
        follows = process_follows(following)

        # number of followers
        num_followers = response.css('div.social.section :nth-child(3) span::text').extract_first()[2:]
        # names of "followers"
        # PROTIP: there are only 6... but which 6 changes on every refresh!
        followed = response.css('.social.section ul.grid-inline')[1]
        followed_by = process_follows(followed)

        yield {
            'user_url': user_url,
            'full_name': full_name,
            'avatar': avatar,
            'first_name': first_name,
            'last_name': last_name,
            'user_id': user_id,
            'location': location,
            'uploaded_images': uploaded_images,
            'num_following': num_following,
            'num_followers': num_followers,
            'following': follows,
            'followers': followed_by
        }
