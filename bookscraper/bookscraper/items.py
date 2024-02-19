# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BookItem(scrapy.Item):
    book_cover = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    other_details = scrapy.Field()
    book_id = scrapy.Field()
    # num_rating = scrapy.Field()
    # publication_year = scrapy.Field()
