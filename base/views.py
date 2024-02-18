from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json

from .forms import SearchForm


# Create your views here.
def home(request):
    if request.method == "POST":
        pass
    return render(request, "home.html")


def searchresults_view(request):
    with open("./bookscraper/booksdata.json") as book_search_data:
        search_results = json.load(book_search_data)

    search_query = request.GET.get("search", "")

    if request.method == "POST":
        print("search_query")
    #     form = SearchForm(request.POST)
    #     if form.is_valid():
    #         return HttpResponseRedirect("/search")
    # else:
    # form = SearchForm()
    return render(
        request,
        "book_search.html",
        {"search_query": search_query, "search_results": search_results},
    )


def bookclub_view(request):
    return render(request, "book_club.html")


def book_view(request):
    return render(request, "book_sample.html")


def chapterdiscussion_view(request):
    return render(request, "chapter_discussion.html")


def forum_view(request):
    return render(request, "forum.html")
