from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import SearchForm


# Create your views here.
def home(request):
    return render(request, "home.html")


def searchresults_view(request):
    search_query = request.GET.get("search", "")

    if request.method == "POST":
        print("search_query")
    #     form = SearchForm(request.POST)
    #     if form.is_valid():
    #         return HttpResponseRedirect("/search")
    # else:
    # form = SearchForm()
    return render(request, "book_search.html", {"search_query": search_query})


def bookclub_view(request):
    return render(request, "book_club.html")


def book_view(request):
    return render(request, "book_sample.html")


def chapterdiscussion_view(request):
    return render(request, "book_sample.html")
