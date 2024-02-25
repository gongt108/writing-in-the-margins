import json
import scrapy
from urllib.parse import urljoin
import re
from base.models import Notification


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

        keyword_list = ["ipad"]
        for notification in notifications:
            keyword = f"{notification.book.title} {notification.book.contributors[0]}"
            amazon_search_url = f"https://www.amazon.com/s?k={keyword}&page=1"
            # TODO yield one search result
            yield scrapy.Request(
                url=amazon_search_url,
                callback=self.discover_product_urls,
                meta={"keyword": keyword, "page": 1},
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
        page = response.meta["page"]
        keyword = response.meta["keyword"]

        ## Discover Product URLs
        search_products = response.css(
            "div.s-result-item[data-component-type=s-search-result]"
        )
        for product in search_products:
            # grabbing portion of url unique to the product
            relative_url = product.css("h2>a::attr(href)").get()
            product_url = urljoin("https://www.amazon.com/", relative_url).split("?")[0]
            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product_data,
                meta={"keyword": keyword, "page": page},
            )

    def parse_product_data(self, response):
        price = response.css('.a-price-whole span[aria-hidden="true"] ::text').get("")
        if not price:
            price = response.css(".a-price .a-offscreen ::text").get("")
        yield {
            "name": response.css("#productTitle::text").get("").strip(),
            "price": price,
        }
