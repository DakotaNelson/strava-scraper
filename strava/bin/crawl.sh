export https_proxy="http://us-ca.proxymesh.com:31280"
export http_proxy="http://us-ca.proxymesh.com:31280"

scrapy crawl -L INFO -s DOWNLOAD_DELAY=0 -s CONCURRENT_REQUESTS_PER_DOMAIN=40 sitemap

scrapy crawl -a usemongo=True -L INFO -s DOWNLOAD_DELAY=0 -s CONCURRENT_REQUESTS_PER_DOMAIN=40 clubs

scrapy crawl -a usemongo=True -L INFO -s DOWNLOAD_DELAY=0 -s CONCURRENT_REQUESTS_PER_DOMAIN=40 users

crapy crawl -a usemongo=True -L INFO -s DOWNLOAD_DELAY=0 -s CONCURRENT_REQUESTS_PER_DOMAIN=32 routes

# activity gets blocked pretty aggressively; as far as I can tell it's the only thing that is
scrapy crawl -a start=0 -a end=10000000 -s CONCURRENT_REQUESTS_PER_DOMAIN=10 -s DOWNLOAD_DELAY=3 activity

scrapy crawl -a start=0 -a end=10000000 segments

scrapy crawl -L INFO -s CONCURRENT_REQUESTS_PER_DOMAIN=10 tiles
