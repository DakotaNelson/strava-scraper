# exit if any commands fail
set -e

# this has huuuuuge pages and puts a lot of load on mongo, so it's throttled
scrapy crawl -L INFO -s DOWNLOAD_DELAY=1 -s CONCURRENT_REQUESTS_PER_DOMAIN=1 -s JOBDIR=crawls/sitemap sitemap

scrapy crawl -a usemongo=True -L INFO -s DOWNLOAD_DELAY=0 -s CONCURRENT_REQUESTS_PER_DOMAIN=40 -s JOBDIR=crawls/clubs clubs

scrapy crawl -a usemongo=True -L INFO -s DOWNLOAD_DELAY=0 -s CONCURRENT_REQUESTS_PER_DOMAIN=40 -s JOBDIR=crawls/users users

crapy crawl -a usemongo=True -L INFO -s DOWNLOAD_DELAY=0 -s CONCURRENT_REQUESTS_PER_DOMAIN=40 -s JOBDIR=crawls/routes routes

scrapy crawl -L INFO -s CONCURRENT_REQUESTS_PER_DOMAIN=10 -s JOBDIR=crawls/tiles tiles

# set up our proxies
export https_proxy="http://us-ca.proxymesh.com:31280"
export http_proxy="http://us-ca.proxymesh.com:31280"

# activity gets blocked pretty aggressively; as far as I can tell it's the only thing that is
scrapy crawl -a start=0 -a end=10000000 -s CONCURRENT_REQUESTS_PER_DOMAIN=10 -s DOWNLOAD_DELAY=3 -s JOBDIR=crawls/activity activity

scrapy crawl -a start=0 -a end=10000000 -s JOBDIR=crawls/segments segments
