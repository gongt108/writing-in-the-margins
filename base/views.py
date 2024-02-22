from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import os
import sys
import subprocess
from .forms import SearchForm, ResponseForm
from .models import Book, Post, Discussion

# Add the directory containing the Scrapy project to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bookscraper"))
from bookscraper.bookscraper.spiders.resultspider import ResultSpider
from bookscraper.bookscraper.spiders.bookspider import BookSpider


# Create your views here.
def home(request):
    if request.user:
        print(request.user.is_authenticated)
    if request.method == "POST":
        form = SearchForm(request.POST)
        return handle_search_form(request, form)
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
    discussions = Discussion.objects.filter(
        Q(type="bookclub") | Q(type="general"), object_id=2
    )
    return render(request, "book_club.html", {"discussions": discussions})


def book_view(request):
    book_id = request.GET.get("book_id")
    found_book = Book.objects.filter(book_id=book_id).first()
    if not found_book:
        subprocess.run(["python", "manage.py", "start_book_scraping", book_id])
        found_book = Book.objects.filter(book_id=book_id).first()

    return render(request, "book_sample.html", {"found_book": found_book})


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


def discussion_view(request, discussion_id):
    user = request.user
    form = ResponseForm()

    # Retrieve the discussion object based on the discussion_id from the URL
    # discussion = get_object_or_404(Discussion, pk=discussion_id)
    discussion = Discussion.objects.get(id=discussion_id)
    posts = Post.objects.filter(discussion=discussion)

    if request.method == "POST":
        if "delete_post_button" in request.POST:
            post_id_to_delete = request.POST["post_id_to_delete"]
            post_to_delete = Post.objects.get(id=post_id_to_delete)
            post_to_delete.delete()
        if not user.is_authenticated:
            print("You must login first.")
        elif "create_post_button" in request.POST and user.is_authenticated:
            form = ResponseForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data["content"]
                Post.objects.create(discussion=discussion, user=user, content=content)
                print("post created")
                return HttpResponseRedirect(
                    reverse("base:discussion-view", args=(discussion_id,))
                )
            else:
                print("error posting")
                for field, errors in form.errors.items():
                    for error in errors:
                        print(f"Error in {field}: {error}")

    return render(
        request,
        "discussions/discussion.html",
        {"form": form, "discussion": discussion, "posts": posts},
    )


def get_posts_for_discussion(discussion_id):
    posts = Post.objects.filter(discussion=discussion_id)
    return posts
