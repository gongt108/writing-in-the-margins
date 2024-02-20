from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import os
import sys
import subprocess
from .models import Book

# Add the directory containing the Scrapy project to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bookscraper"))
from .forms import SearchForm
from bookscraper.bookscraper.spiders.resultspider import ResultSpider
from bookscraper.bookscraper.spiders.bookspider import BookSpider


# Create your views here.
def home(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        return handle_search_form(request, form)

        # if form.is_valid():
        #     search_query = form.cleaned_data["search_query"]
        #     subprocess.run(["python", "manage.py", "start_scraping", search_query])

        #     return HttpResponseRedirect(
        #         f"/search?search_query={search_query}/"
        #     )  # Redirect after form submission
    else:
        form = SearchForm()
    return render(request, "home.html", {"form": form})


def start_scraping(search_query):
    process = CrawlerProcess(
        settings={
            "FEEDS": {"booksdata.json": {"format": "json", "overwrite": True}},
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        }
    )
    # Pass search_query as argument to the spider
    process.crawl(ResultSpider, search_query=search_query)
    process.start()


def handle_search_form(request, form):
    if form.is_valid():
        search_query = form.cleaned_data["search_query"]
        subprocess.run(["python", "manage.py", "start_scraping", search_query])

        return HttpResponseRedirect(
            f"/search?search_query={search_query}/"
        )  # Redirect after form submission


def searchform_template(request):
    form = SearchForm()
    return render(request, "forms/search_form.html", {"form": form})


def searchresults_view(request):
    with open("booksdata.json") as book_search_data:
        search_results = json.load(book_search_data)

    search_query = request.GET.get("search_query", "")
    print("searchquery", search_query)
    form = SearchForm()

    if request.method == "POST":
        form = SearchForm(request.POST)
        return handle_search_form(request, form)
    else:
        form = SearchForm()
    return render(
        request,
        "book_search.html",
        {"search_query": search_query, "search_results": search_results, "form": form},
    )


def bookclub_view(request):
    return render(request, "book_club.html")


def book_view(request):
    book_id = request.GET.get("book_id")
    found_book = Book.objects.filter(book_id=book_id)
    if not found_book:
        subprocess.run(["python", "manage.py", "start_book_scraping", book_id])
    else:
        print(found_book)
    return render(request, "book_sample.html")


def start_book_scraping(book_id):
    process = CrawlerProcess(
        settings={
            "FEEDS": {"bookdata.json": {"format": "json", "overwrite": True}},
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        }
    )
    # Pass search_query as argument to the spider
    process.crawl(BookSpider, book_id=book_id)
    process.start()


def chapterdiscussion_view(request):
    return render(request, "chapter_discussion.html")


def forum_view(request):
    return render(request, "forum.html")
