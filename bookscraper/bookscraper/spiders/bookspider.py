from typing import Iterable
import scrapy
import scrapy.crawler as crawler
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from multiprocessing import Process, Queue
from twisted.internet import reactor

import urllib.parse
from bookscraper.bookscraper.items import BookItem

# from bookscraper.items import BookItem


class BookSpider(scrapy.Spider):
    name = "bookspooder"
    allowed_domains = ["www.goodreads.com"]

    custom_settings = {
        "FEEDS": {"booksdata.json": {"format": "json", "overwrite": True}}
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
        book_item = BookItem()
        books = response.css("table.tableList tr")
        for book in books:
            book_item["book_cover"] = book.css(
                "img.bookCover::attr(src)"
            ).extract_first()
            book_item["title"] = book.css("a.bookTitle span::text").get()
            book_item["author"] = book.css("a.authorName span::text").get()
            book_item["other_details"] = (
                book.xpath("td[2]/div[1]/span").xpath("normalize-space()").getall()[0]
            )
            parsed_url = urllib.parse.urlparse(
                book.css("a.bookTitle::attr(href)").extract_first()
            )
            book_item["book_id"] = parsed_url.path.split("/")[-1]

            # Put the book item in the result queue
            yield book_item


# def scrape_books(search_query, result_queue):
#     # Create a CrawlerProcess
#     process = CrawlerProcess(get_project_settings())
#     # Pass the search query and result queue to the spider
#     process.crawl(BookSpider, search_query=search_query, result_queue=result_queue)
#     # Start the crawling process
#     process.start()


# if __name__ == "__main__":
#     # Create a queue to communicate between the main process and spawned processes
#     result_queue = Queue()
#     # Start separate processes for each search query
#     processes = []
#     search_queries = ["query1", "query2", "query3"]  # Example search queries
#     for query in search_queries:
#         p = Process(target=scrape_books, args=(query, result_queue))
#         p.start()
#         processes.append(p)
#     # Wait for all processes to finish
#     for p in processes:
#         p.join()
#     # Collect results from the queue
#     while not result_queue.empty():
#         result = result_queue.get()
#         print(result)
