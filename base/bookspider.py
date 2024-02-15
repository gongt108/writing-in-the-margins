import scrapy


class BookSpider(scrapy.Spider):
    name = "book spooder"
    search_query = "h+mart"
    start_urls = [
        f"https://www.goodreads.com/search?utf8=✓&q={search_query}&search_type=books"
    ]

    def parse(self, response):
        for article in response.css("tr.athing"):
            yield {
                "title": article.css("a.storylink::text").get(),
                "url": article.css("a.storylink::attr(href)").get(),
                "votes": int(article.css("span.score::text").re_first(r"\d+")),
            }
        next_page = response.css("a.morelink::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
