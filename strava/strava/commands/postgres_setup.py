import scrapy
from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from strava.postgresql_utils import *

class SetUpPostgres(ScrapyCommand):
    def short_desc(self):
        return "Create tables in PostgreSQL"

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("--postgres_uri", dest="postgres_uri", metavar="URI",
                help="connection string for PostgreSQL to put Strava data into",
                default="postgresql:///strava")

    def run(self, args, opts):
        """
        NOTE: you already have to have a database created, with PostGIS enabled
        This may look like:

        sudo -u postgres psql -c "CREATE DATABASE strava;"
        sudo -u postgres psql -d strava -c "CREATE EXTENSION postgis;"
        sudo -u postgres psql -d strava -c "CREATE EXTENSION fuzzystrmatch;"
        sudo -u postgres psql -d strava -c "CREATE EXTENSION address_standardizer;"

        But you do you, boo
        """
        engine = sqlalchemy.create_engine(opts.postgres_uri)
        Base.metadata.create_all(engine)
