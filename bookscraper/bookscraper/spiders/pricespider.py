import json
import scrapy
import urllib.parse
from django.utils import timezone

# from urllib.parse import urljoin
import re
import psycopg2

from bookscraper.bookscraper.items import AmazonItem

# from bookscraper.items import AmazonItem


class AmazonSearchProductSpider(scrapy.Spider):
    name = "price_spider"
    date = str(timezone.now().date())

    custom_settings = {
        "FEEDS": {
            f"data/%(name)s_{date}.json": {
                "format": "json",
            }
        },
        "ITEM_PIPELINES": {
            "bookscraper.bookscraper.pipelines.AmazonscraperPipeline": 300,
            # "bookscraper.pipelines.EmailUserPipeline": 400,
        },
    }

    def __init__(self):
        self.connection = psycopg2.connect(
            host="localhost", user="tiffanygong", password="testpass", dbname="project4"
        )

        self.cur = self.connection.cursor()
        # Execute the query
        self.cur.execute(
            "SELECT title, contributors, price, email FROM base_book JOIN base_notification ON base_book.id = base_notification.book_id"
        )

        # Fetch all rows from the result set
        notifications = self.cur.fetchall()

        # Close the cursor and the connection
        self.cur.close()
        self.connection.close()

        # Return the fetched notifications
        self.notifications = notifications

    def start_requests(self):
        notifications = self.notifications
        # keyword_list = ["ipad"]
        for notification in notifications:
            title = notification[0]
            contributors = notification[1].split(",")
            target_price = notification[2]
            email = notification[3]
            keyword = f"{title} by {contributors[0]}"
            parsed_keyword = urllib.parse.quote_plus(keyword)

            amazon_search_url = f"https://www.amazon.com/s?k={parsed_keyword}"

            # amazon_search_url = f"https://www.amazon.com/s?k={keyword}&page=1"
            yield scrapy.Request(
                url=amazon_search_url,
                callback=self.discover_product_urls,
                meta={
                    "keyword": keyword,
                    "target_price": target_price,
                    "email": email,
                },
            )

    def discover_product_urls(self, response):
        amazon_item = AmazonItem()
        target_price = response.meta["target_price"]

        ## Discover Product URLs
        product = response.css(
            "div.s-result-item[data-component-type=s-search-result]"
        )[1]

        dollar = product.css("span.a-price-whole::text").get("")
        cent = product.css("span.a-price-fraction::text").get("")

        if dollar and dollar.isdigit() and int(dollar) < target_price:
            amazon_item["name"] = (
                product.css("h2.a-size-mini span.a-size-medium::text").get("").strip()
            )
            amazon_item["price"] = f"{dollar}.{cent}"
            amazon_item["email"] = response.meta["email"]

            yield amazon_item

        # relative_url = product.css("h2>a::attr(href)").get()
        # product_url = urllib.parse.urljoin(
        #     "https://www.amazon.com/", relative_url
        # ).split("?")[0]
        # yield scrapy.Request(
        #     url=product_url,
        #     callback=self.parse_product_data,
        #     meta={"keyword": keyword, "page": page},
        # )

        ## Get All Pages

    # def parse_product_data(self, response):

    # price = response.css('.a-price-whole span[aria-hidden="true"] ::text').get("")
    # price = response.css(".a-price .a-offscreen::text").get()
    # if not price:
    # price = response.css(".a-price .a-offscreen ::text").get("")
    # if price is not None and price < target_price:

    #     yield {
    #         "name": response.css("#productTitle::text").get("").strip(),
    #         "price": price,
    #     }
    # yield {
    #     "name": response.css("#productTitle::text").get("").strip(),
    #     "price": price,
    # }
