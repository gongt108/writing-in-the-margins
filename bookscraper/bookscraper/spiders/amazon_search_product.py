import json
import scrapy
import urllib.parse

# from urllib.parse import urljoin
import re
from base.models import Notification

# from bookscraper.bookscraper.items import AmazonItem

from bookscraper.items import AmazonItem


class AmazonSearchProductSpider(scrapy.Spider):
    name = "amazon_search_product"

    custom_settings = {
        "FEEDS": {
            "data/%(name)s_%(time)s.csv": {
                "format": "csv",
            }
        }
    }

    def start_requests(self):
        notifications = Notification.objects.all()
        if len(notifications) == 0:
            return
        # keyword_list = ["ipad"]
        for notification in notifications:
            keyword = (
                f"{notification.book.title} by {notification.book.contributors[0]}"
            )
            parsed_keyword = urllib.parse.quote_plus(keyword)
            amazon_search_url = f"https://www.amazon.com/s?k={parsed_keyword}&page=1"
            # TODO yield one search result
            yield scrapy.Request(
                url=amazon_search_url,
                callback=self.discover_product_urls,
                meta={
                    "keyword": parsed_keyword,
                    "target_price": notification.price,
                    "email": notification.email,
                },
            )

        # keyword_list = ["ipad"]
        # for keyword in keyword_list:
        #     amazon_search_url = f"https://www.amazon.com/s?k={keyword}&page=1"
        #     yield scrapy.Request(
        #         url=amazon_search_url,
        #         callback=self.discover_product_urls,
        #         meta={"keyword": keyword, "page": 1},
        #     )

    def discover_product_urls(self, response):
        keyword = response.meta["page"]
        target_price = response.meta["target_price"]
        email = response.meta["email"]

        ## Discover Product URLs
        search_products = response.css(
            "div.s-result-item[data-component-type=s-search-result]"
        )[1]
        for product in search_products:
            # grabbing portion of url unique to the product
            relative_url = product.css("h2>a::attr(href)").get()
            product_url = urllib.parse.urljoin(
                "https://www.amazon.com/", relative_url
            ).split("?")[0]
            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product_data,
                meta={"keyword": keyword, "target_price": target_price, "email": email},
            )

    def parse_product_data(self, response):
        amazon_item = AmazonItem()
        price = response.css('.a-price-whole span[aria-hidden="true"] ::text').get("")
        target_price = response.meta["target_price"]

        if not price:
            price = response.css(".a-price .a-offscreen ::text").get("")

        if price is not None and price < target_price:
            amazon_item["name"] = response.css("#productTitle::text").get("").xstrip()
            amazon_item["price"] = price
            amazon_item["email"] = response.meta["email"]
            yield amazon_item
