# scraper.py
import sys
import os
from celery import shared_task
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bookscraper"))
from bookscraper.bookscraper.spiders.bookspider import BookSpider


@shared_task
def run_spider(search_query):
    process = CrawlerProcess(get_project_settings())
    process.crawl(BookSpider, search_query=search_query)
    process.start()
