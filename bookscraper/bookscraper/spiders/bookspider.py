from typing import Iterable
import scrapy
from bookscraper.items import BookItem


class BookSpider(scrapy.Spider):
    name = "bookspooder"
    allowed_domains = ["www.goodreads.com"]
    start_urls = [
        "https://www.goodreads.com/search?utf8=%E2%9C%93&q=h+mart&search_type=books"
    ]

    custom_settings = {
        "FEEDS": {"booksdata.json": {"format": "json", "overwrite": True}}
    }

    # def start_requests(self):
    #     search_query = "h+mart"
    #     url = f"https://www.goodreads.com/search?utf8=✓&q={search_query}&search_type=books"
    #     yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
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
            # book_item["avg_rating"] = other_details[0].strip()
            # book_item["num_rating"] = other_details[1].strip()
            # book_item["publication_year"] = other_details[2].strip()

            yield book_item
