# -*- coding: utf-8 -*-
import re
import logging

import scrapy


class UserSpider(scrapy.Spider):
    name = 'user_scraper'
    allowed_domains = ['strava.com']

    def start_requests(self):
        """ yield a URL for each user """
        max_user = 2000
        for i in range(0,max_user+1):
            url = 'https://www.strava.com/athletes/{}'.format(i)
            yield scrapy.Request(
                url=url,
                meta = {'dont_redirect': True,
                        'handle_httpstatus_list': [302]},
                callback=self.parse
            )

    def parse(self, response):
        user_url = response.url
        user_id = response.url.split('/')[-1]

        title_text = response.css('title::text').re('Strava .+ Profile')
        if len(title_text) < 1:
            # invalid, we probably got a redirect
            return

        full_name = response.css('h1.bottomless::text').extract_first()

        first_name = None
        last_name = None
        try:
            first_name, last_name = full_name.split(' ')
        except ValueError:
            logging.error("Unable to parse name: {}".format(full_name))
        except AttributeError:
            logging.error("Unable to parse name: {}".format(full_name))

        # this regex can extract the user's ID from their strava profile photo
        # (unless they use a facebook/google profile photo)
        id_from_avatar_url = re.compile(r'cloudfront.net\/pictures\/athletes\/(\d+)')

        # number of users they're following
        num_following = response.css('div.social.section :nth-child(1) span::text').extract_first()[2:]
        # names of "following"
        # PROTIP: there are only 6... but which 6 changes on every refresh!
        following = response.css('.social.section ul.grid-inline')[0]
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

        # number of followers
        num_followers = response.css('div.social.section :nth-child(3) span::text').extract_first()[2:]
        # names of "followers"
        followed = response.css('.social.section ul.grid-inline')[1]
        names = followed.css('.avatar::attr(title)').extract()
        avatars = followed.css('.avatar-img::attr(src)').extract()

        followed_by = []
        for name,avatar_url in zip(names, avatars):
            try:
                user_id = id_from_avatar_url.search(avatar_url).group().split('/')[-1]
            except AttributeError:
                # didn't find it
                user_id = None
            followed_by.append({
                'name': name,
                'avatar': avatar_url,
                'user_id': user_id
            })


        yield {
            'user_url': user_url,
            'full_name': full_name,
            'first_name': first_name,
            'last_name': last_name,
            'user_id': user_id,
            'num_following': num_following,
            'num_followers': num_followers,
            'following': follows,
            'followers': followed_by
        }
