import scrapy

from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError

import sqlalchemy
from sqlalchemy import func

from strava.postgresql_utils import User, Activity

class CrawlFromMax(ScrapyCommand):
    def short_desc(self):
        return "Start crawling from max(id) in database"

    def syntax(self):
        return "[options] <table: {users,routes,clubs,activity}>"

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        parser.add_option("--postgres_uri", dest="postgres_uri", metavar="URI",
                help="connection string for PostgreSQL to put data into",
                default="postgresql:///strava")
        parser.add_option("-a", dest="spargs", action="append", default=[],
                metavar="NAME=VALUE",
                help="set spider argument (may be repeated)")

    def run(self, args, opts):
        if len(args) != 1 or \
                args[0] not in ["users", "routes", "clubs", "activity"]:
            raise UsageError()

        # open a session with PostgreSQL
        engine = sqlalchemy.create_engine(opts.postgres_uri)
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        psql = Session()

        # TODO get max(id) for chosen table
        # these will probably return bad numbers /shrug
        dbMax = 0
        if args[0] == "users":
            dbMax = psql.query(func.count(User.id))
        elif args[0] == "activity":
            dbMax = psql.query(func.count(Activity.id))
        elif args[0] == "routes":
            raise NotImplementedError
        elif args[0] == "clubs":
            raise NotImplementedError

        # TODO re-add **opts.spargs to allow passing spider args
        crawl_defer = self.crawler_process.crawl(args[0], start=dbMax)
                #**opts.spargs)
        if getattr(crawl_defer, 'result', None) is not None and \
                issubclass(crawl_defer.result.type, Exception):
            self.exitcode = 1
        else:
            self.crawler_process.start()

            if self.crawler_process.bootstrap_failed or \
                    (hasattr(self.crawler_process, 'has_exception') and \
                    self.crawler_process.has_exception):
                self.exitcode = 1
