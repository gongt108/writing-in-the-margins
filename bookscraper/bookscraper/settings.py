# Scrapy settings for bookscraper project
BOT_NAME = "bookscraper"

import os
from dotenv import load_dotenv

load_dotenv()

# SCRAPEOPS_API_KEY = os.getenv("SCRAPEOPS_API_KEY ")
# print("SCRAPEOPS_API_KEY", SCRAPEOPS_API_KEY)
SCRAPEOPS_API_KEY = "84624c6b-0aa5-475a-91d2-116ba96de156"
SCRAPEOPS_PROXY_ENABLED = True
# SCRAPEOPS_NUM_RESULTS = 5

SPIDER_MODULES = ["bookscraper.spiders"]
NEWSPIDER_MODULE = "bookscraper.spiders"

# allows you to use scrapy crawl bookspider without specifying file name
FEEDS = {"booksdata.json": {"format": "json"}}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "bookscraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "bookscraper.middlewares.BookscraperSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #    "bookscraper.middlewares.BookscraperDownloaderMiddleware": 543,
    # "bookscraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware": 400,
    "scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk": 725,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     "bookscraper.pipelines.BookscraperPipeline": 300,
#     "bookscraper.pipelines.SaveToMySQLPipeline": 400,  # number represents order in pipeline. lower number first
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Configure SMTP settings
MAIL_FROM = "gongt108@gmail.com"
MAIL_HOST = "smtp.gmail.com"
MAIL_PORT = 587  # or 25, 465 (SSL)
MAIL_USERNAME = "gongt108"
MAIL_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
MAIL_TLS = True  # Set to False if you're using SSL
