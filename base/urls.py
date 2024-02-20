from django.urls import path
from . import views

app_name = "base"

urlpatterns = [
    path("", views.home, name="home"),
    path("book-club/", views.bookclub_view, name="book-club"),
    path("book/", views.book_view, name="book-view"),
    path(
        "book/chapter-discussion/",
        views.chapterdiscussion_view,
        name="chapter-discussion",
    ),
    path(
        "book/forum/",
        views.forum_view,
        name="other-discussion",
    ),
    path("search/", views.searchresults_view, name="search-view"),
]