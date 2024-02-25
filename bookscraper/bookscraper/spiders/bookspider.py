# from typing import Iterable
# import scrapy
# import scrapy.crawler as crawler
# from scrapy.utils.log import configure_logging
# from scrapy.utils.project import get_project_settings
# from multiprocessing import Process, Queue
# from bs4 import BeautifulSoup
# import urllib.parse


# from bookscraper.bookscraper.items import ResultItem, BookItem

# # from bookscraper.items import BookItem


# class BookSpider(scrapy.Spider):
#     name = "bookspooder"
#     allowed_domains = ["www.goodreads.com"]

#     custom_settings = {
#         "FEEDS": {"bookdata.json": {"format": "json", "overwrite": True}},
#         "ITEM_PIPELINES": {
#             "bookscraper.bookscraper.pipelines.BookscraperPipeline": 300,
#             "bookscraper.bookscraper.pipelines.SaveToPostgresPipeline": 400,
#         },
#     }

#     def __init__(self, book_id=None):
#         self.book_id = book_id

#     def start_requests(self):
#         if self.book_id:
#             url = f"https://www.goodreads.com/book/show/{self.book_id}"
#             yield scrapy.Request(url, callback=self.parse_search_results)

#     def parse_search_results(self, response):
#         book_item = BookItem()
#         book = response.css("div.BookPage__gridContainer")
#         book_item["book_cover"] = book.css(
#             "img.ResponsiveImage::attr(src)"
#         ).extract_first()
#         book_item["title"] = book.css("div.BookPageTitleSection__title h1::text").get()
#         book_item["contributors"] = response.css(
#             "div.ContributorLinksList span.ContributorLink__name::text"
#         ).getall()
#         book_item["avg_rating"] = book.css("div.RatingStatistics__rating::text").get()
#         book_item["num_rating"] = book.css(
#             "div.RatingStatistics__meta span.u-dot-before::text"
#         ).get()
#         book_item["description"] = book.css(
#             "div.BookPageMetadataSection__description div.DetailsLayoutRightParagraph__widthConstrained span.Formatted::text"
#         ).getall()
#         book_item["genres"] = book.css(
#             "ul.CollapsableList span.Button__labelItem::text"
#         ).getall()[:5]
#         book_item["page_num"] = book.css("div.FeaturedDetails p::text").getall()[0]
#         book_item["publication_date"] = book.css(
#             "div.FeaturedDetails p::text"
#         ).getall()[1]
#         book_item["book_id"] = (
#             response.xpath('//head/link[@rel="canonical"]/@href').get().split("/")[-1]
#         )

#         yield book_item
