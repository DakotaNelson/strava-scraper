# strava-scraper

It scrapes Strava.

To set up:

`virtualenv --python=python3 venv && source venv/bin/activate && pip install requirements.txt`

If you want to put the data in mongodb, make sure mongo is running (locally or otherwise):

`sudo mongod --dbpath ./db/`

Then, go to `strava-scraper/strava/strava/settings.py` and set `MONGO_URI` and `MONGO_DATABASE`.


### To run:

#### Run everything using:

`source venv/bin/activate && cd strava && scrapy crawlall`

#### Run a specific crawler using:

`source venv/bin/activate && cd strava && scrapy crawl tiles`

Instead of `tiles`, you could run `users`, `activity`, etc. - if you look in the folder `strava/strava/spiders/` you'll find all the available things to crawl. If you want output, you can add `-o FILE` and `-t FORMAT` to save down the data to a file. You'll also probably want to specify some options for the crawlers, though they have sensible defaults if you're just testing (but you won't get much data). You can look in `strava/commands/crawlall.py` to see what the defaults are for a comprehensive data dump from Strava and go from there.
