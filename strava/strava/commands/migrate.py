import scrapy
from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError

import pymongo
import sqlalchemy

from shapely.geometry import shape
from geoalchemy2.shape import from_shape
#from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from sqlalchemy.exc import IntegrityError

from strava.postgresql_utils import User, Activity

class MigrateFromMongo(ScrapyCommand):
    def short_desc(self):
        return "Migrate strava data from MongoDB to PostgreSQL"

    def syntax(self):
        return "[options] <table: {users,routes,clubs,activity}>"

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("--mongo_uri", dest="mongo_uri", metavar="URI",
                help="connection string for MongoDB containing Strava data",
                default="mongodb://localhost:27017/strava")
        parser.add_option("--postgres_uri", dest="postgres_uri", metavar="URI",
                help="connection string for PostgreSQL to put Strava data into",
                default="postgresql:///strava")

    def run(self, args, opts):
        if len(args) != 1 or args[0] not in ["users", "routes", "clubs", "activity"]:
            raise UsageError()

        # open a session with MongoDB
        mongo = pymongo.MongoClient(opts.mongo_uri)['strava']

        # open a session with PostgreSQL
        engine = sqlalchemy.create_engine(opts.postgres_uri)
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        psql = Session()

        # move EEEEEEEEEEEVERYTHING from Mongo to Postgres
        collectionSize = mongo[args[0]].estimated_document_count()
        processed = 0
        batchSize = 10000
        print(f"Now migrating {collectionSize} documents from MongoDB...")
        cursor = mongo[args[0]].find(batch_size=batchSize, no_cursor_timeout=True)
        for item in cursor:
            processed += 1
            try:
                toAdd = mongoToPostgres(item, args[0])
                psql.add(toAdd)
                psql.commit()
            except IntegrityError:
                if args[0] == "activity":
                    psql.rollback()
                    # user was not present in db; add an empty row for them
                    userid = toAdd.user_id
                    psql.add(User(id=userid))
                    psql.add(toAdd)
                    psql.commit()
            if processed % 10000 == 0:
                if processed % 100000 == 0:
                    percent = processed / collectionSize
                    print(f"Migrated {processed}/{collectionSize} ({percent:.1%}) documents...")

        print("Performing final commit...")
        psql.commit()
        print("Closing cursors...")
        cursor.close()
        print("Done!")


def mongoToPostgres(item, table):
    """ Given an item from MongoDb, and a string representing what type of item
    it is, return the item reformatted for insertion into Postgres """
    if table == "users":
        return User(
                id = item["user_id"],
                full_name = item["full_name"],
                first_name = item["first_name"],
                last_name = item["last_name"],
                avatar = item["avatar"],
                location = item["location"],
                num_following = item["num_following"],
                num_followers = item["num_followers"]
                )
    elif table == "routes":
        raise NotImplementedError
    elif table == "clubs":
        raise NotImplementedError
    elif table == "activity":
        try:
            raw_path = {
                "type": item["path"]["type"],
                "coordinates": [tuple(x) for x in item["path"]["coordinates"]]
            }
            path = shape(raw_path)
            # NOTE this will fail out the whole process; is not caught
            assert path.geom_type == "LineString"
            path = from_shape(path)
        except TypeError:
            path = None
        return Activity(
                id = item["activity_id"],
                user_id = item["athlete_id"],
                name = item["activity_name"],
                path = path
                )
    else:
        raise ValueError('table name not recognized')
