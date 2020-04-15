# -*- coding: utf-8 -*-
import scrapy
import logging

import pymongo

class ClubsSpider(scrapy.Spider):
    name = 'clubs'
    allowed_domains = ['strava.com']

    def start_requests(self):
        """ yield a URL for each club """
        # get our options
        start = getattr(self, 'start', 0)
        end = getattr(self, 'end', 1000)
        usemongo = bool(getattr(self, 'usemongo', False))

        if usemongo:
            mongo_uri = self.settings.get('MONGO_URI')
            mongo_db = self.settings.get('MONGO_DB')

            try:
                logging.info("Starting club spider with Mongo query")
                client = pymongo.MongoClient(mongo_uri)
                db = client[mongo_db]
                clubs = db.sitemap.find({"url_category": "clubs"})
                logging.info("Club spider found {} clubs".format(len(clubs)))
                for club in clubs:
                    yield scrapy.Request(
                        url=club['url'],
                        meta = {'dont_redirect': True,
                                'handle_httpstatus_list': [302]},
                        callback=self.parse
                    )
            finally:
                client.close()

        else:
            logging.info("Starting club spider with range {} to {}".format(start, end+1))
            for i in range(start,end+1):
                url = 'https://www.strava.com/clubs/{}'.format(i)
                yield scrapy.Request(
                    url=url,
                    meta = {'dont_redirect': True,
                            'handle_httpstatus_list': [302]},
                    callback=self.parse
                )

    def parse(self, response):
        club_id = response.url.split('/')[-1]
        try:
            club_name = response.css(".club-description h1::text").extract_first().strip()
        except AttributeError:
            club_name = None
        try:
            club_location = response.css(".club-description p.location::text").extract_first().strip()
        except AttributeError:
            club_location = None
        members = []
        for member in response.css("div.avatar a::attr(href)").extract():
            member_num = member.split('/')[-1]
            try:
                member_num = int(member_num)
            except:
                pass
            members.append(member_num)
        try:
            num_members = response.css("div.club-members h3::text").re("(\d+)\ members")[0]
        except IndexError:
            num_members = None
        leaderboard = response.css(".leaderboard .athlete a::attr(href)").extract()
        for athlete in leaderboard:
            members.append(athlete.split('/')[-1])
        members = list(set(members))

        yield {
            "club_id": int(club_id),
            "club_name": club_name,
            "club_location": club_location,
            "club_members": members,
            "club_num_members": int(num_members)
        }
