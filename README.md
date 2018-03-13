# strava-scraper

It scrapes Strava.

To set up:

`virtualenv --python=python3 venv && pip install requirements.txt`

To run:

`source venv/bin/activate && cd tile_scraper && scrapy crawl tile_scraper`

`source venv/bin/activate && cd user_scraper && scrapy crawl user_scraper -o outputfile.jl`

(JL is for [JSON Lines format](http://jsonlines.org/))
