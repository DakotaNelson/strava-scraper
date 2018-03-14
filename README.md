# strava-scraper

It scrapes Strava.

To set up:

`virtualenv --python=python3 venv && source venv/bin/activate && pip install requirements.txt`

To run:

`source venv/bin/activate && cd tile_scraper && scrapy crawl tile_scraper`

`source venv/bin/activate && cd user_scraper && scrapy crawl user_scraper -o outputfile.jl`

You can use the previous two run examples to run any of the scrapers.

(JL is for [JSON Lines format](http://jsonlines.org/))
