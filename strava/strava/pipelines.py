# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlalchemy
from shapely.geometry import shape
from geoalchemy2.shape import from_shape

from strava.postgresql_utils import User, Activity

class PostgresPipeline(object):
    def __init__(self, postgres_uri):
        # TODO get from settings
        self.postgres_uri = postgres_uri
        # TODO initialize tables and whatnot

    def open_spider(self, spider):
        # open a session with PostgreSQL
        engine = sqlalchemy.create_engine(opts.postgres_uri)
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        self.psql = Session()

    def close_spider(self, spider):
        self.psql.commit()
        self.psql.close()

    def process_item(self, item, spider):
        if spider.name == "users":
            self.psql.add(User(
                    id = item["user_id"],
                    full_name = item["full_name"],
                    first_name = item["first_name"],
                    last_name = item["last_name"],
                    avatar = item["avatar"],
                    location = item["location"],
                    num_following = item["num_following"],
                    num_followers = item["num_followers"]
                    ))
        elif spider.name == "routes":
            raise NotImplementedError
        elif spider.name == "clubs":
            raise NotImplementedError
        elif spider.name == "activity":
            try:
                path = shape(item["path"])
                # NOTE this will fail out the whole process; is not caught
                assert path.geom_type == "LineString"
                path = from_shape(path)
            except TypeError:
                path = None
            self.psql.add(Activity(
                    id = item["activity_id"],
                    user_id = item["athlete_id"],
                    name = item["full_name"],
                    path = path
                    ))
        else:
            raise ValueError('spider name not recognized')

        return item
