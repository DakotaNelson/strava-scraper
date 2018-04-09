# strava-scraper

It scrapes Strava.

To set up:

`virtualenv --python=python3 venv && source venv/bin/activate && pip install requirements.txt`

To run:

`source venv/bin/activate && cd strava && scrapy crawl tiles`

Instead of `tiles`, you could run `users`, `activity`, etc. - if you look in the folder `strava/strava/spiders/` you'll find all the available things to crawl. If you want output, you can add `-o FILE` and `-t FORMAT` to save down the data to a file.


(JL is for [JSON Lines format](http://jsonlines.org/))
