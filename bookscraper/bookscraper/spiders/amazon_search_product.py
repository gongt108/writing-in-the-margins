import json
import scrapy
import urllib.parse

# from urllib.parse import urljoin
import re
import psycopg2

# from bookscraper.bookscraper.items import AmazonItem

from bookscraper.items import AmazonItem


class AmazonSearchProductSpider(scrapy.Spider):
    name = "amazon_search_product"

    custom_settings = {
        "FEEDS": {
            "data/%(name)s_%(time)s.csv": {
                "format": "csv",
            }
        },
        "ITEM_PIPELINES": {
            "bookscraper.pipelines.AmazonscraperPipeline": 400,
        },
    }


def start_requests(self):
    print("starting spider")
    # Call the function and print the notifications
    notifications = [
        (
            "Harry Potter and the Sorcerer’s Stone",
            "J.K. Rowling, Olly Moss",
            29,
            "tiffanygong@yahoo.com",
        )
    ]
    # notifications = get_notifications()
    # print("notifications", notifications)

    if len(notifications) == 0:
        return

    for notification in notifications:
        title = notification[0]
        contributors = notification[1].split(",")
        price = notification[2]
        email = notification[3]
        keyword = f"{title} by {contributors[0]}"
        parsed_keyword = urllib.parse.quote_plus(keyword)

        amazon_search_url = f"https://www.amazon.com/s?k={parsed_keyword}"

        # TODO yield one search result
        # yield scrapy.Request(
        #     url=amazon_search_url,
        #     callback=self.discover_product_urls,
        #     meta={
        #         "keyword": parsed_keyword,
        #         "target_price": notification.price,
        #         "email": notification.email,
        #     },
        # )


def discover_product_urls(self, response):
    keyword = response.meta["keyword"]

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
            meta={
                "keyword": keyword,
                "target_price": response.meta["target_price"],
                "email": response.meta["email"],
            },
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
