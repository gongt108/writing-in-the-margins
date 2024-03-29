# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ResultItem(scrapy.Item):
    book_cover = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    other_details = scrapy.Field()
    book_id = scrapy.Field()


class BookItem(scrapy.Item):
    book_cover = scrapy.Field()
    title = scrapy.Field()
    contributors = scrapy.Field()
    avg_rating = scrapy.Field()
    num_rating = scrapy.Field()
    description = scrapy.Field()
    genres = scrapy.Field()
    page_num = scrapy.Field()
    publication_date = scrapy.Field()
    book_id = scrapy.Field()


class AmazonItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    email = scrapy.Field()
