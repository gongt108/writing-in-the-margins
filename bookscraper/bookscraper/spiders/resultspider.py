from typing import Iterable
import scrapy
import scrapy.crawler as crawler
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from multiprocessing import Process, Queue

import urllib.parse

# from bookscraper.bookscraper.items import ResultItem, BookItem

from bookscraper.items import ResultItem, BookItem


class ResultSpider(scrapy.Spider):
    name = "resultspider"
    allowed_domains = ["www.goodreads.com"]

    custom_settings = {
        "FEEDS": {"booksdata.json": {"format": "json", "overwrite": True}},
    }

    def __init__(self, search_query=None, result_queue=None):
        self.search_query = search_query
        self.result_queue = result_queue

    def start_requests(self):
        # def f(q):
        #     try:
        #         runner = crawler.CrawlerRunner()
        #         deferred =
        if self.search_query:
            search_query = urllib.parse.quote_plus(self.search_query)
            url = f"https://www.goodreads.com/search?utf8=✓&q={search_query}"
            yield scrapy.Request(url, callback=self.parse_search_results)

    def parse_search_results(self, response):
        result_item = ResultItem()
        books = response.css("table.tableList tr")
        for book in books:
            result_item["book_cover"] = book.css(
                "img.bookCover::attr(src)"
            ).extract_first()
            result_item["title"] = book.css("a.bookTitle span::text").get()
            result_item["author"] = book.css("a.authorName span::text").get()
            result_item["other_details"] = (
                book.xpath("td[2]/div[1]/span").xpath("normalize-space()").getall()[0]
            )
            parsed_url = urllib.parse.urlparse(
                book.css("a.bookTitle::attr(href)").extract_first()
            )
            result_item["book_id"] = parsed_url.path.split("/")[-1]

            # Put the book item in the result queue
            yield result_item
