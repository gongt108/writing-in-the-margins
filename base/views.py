from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import os
import sys
import subprocess
from .forms import (
    SearchForm,
    ResponseForm,
    NewDiscussionForm,
    AddToListForm,
    CreateOrEditNotificationForm,
)
from .models import Book, BookClub, Post, Discussion, Notification
from users.models import Profile

# Add the directory containing the Scrapy project to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bookscraper"))
from bookscraper.bookscraper.spiders.resultspider import ResultSpider
from bookscraper.bookscraper.spiders.bookspider import BookSpider


# Create your views here.
def home(request):
    print(request.user.profile.tbr_list.all())
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
    book_club = request.user.profile.book_club
    if book_club is None:
        bookclubs = BookClub.objects.all()
        if request.method == "POST":
            book_club_to_join_id = request.POST.get("book_club_to_join")
            book_club_to_join = BookClub.objects.get(id=book_club_to_join_id)
            # Update the user's profile with the new book club
            request.user.profile.book_club = book_club_to_join
            request.user.profile.save()

            return HttpResponseRedirect(reverse("base:book-club"))

        return render(request, "bookclub_join.html", {"bookclubs": bookclubs})

    if book_club:
        # bookclub = BookClub.objects.get(id=bookclub.id)
        discussions = Discussion.objects.filter(
            Q(type="bookclub") | Q(type="general"), object_id=book_club.id
        ).order_by("-last_update")
        members = Profile.objects.filter(book_club=book_club)
        admins = members.filter(bookclub_admin=True)
        if request.method == "POST":
            next_meeting_date = request.POST["datepicker"]
            next_meeting_date = datetime.strptime(next_meeting_date, "%m/%d/%Y")
            print(next_meeting_date)
            book_club.next_meeting_date = next_meeting_date
            book_club.save()

        print(book_club.next_meeting_date)
        print(timezone.now())

        if (
            book_club.next_meeting_date is not None
            and book_club.next_meeting_date < timezone.now()
        ):
            book_club.next_meeting_date = None
            book_club.save()

        return render(
            request,
            "book_club.html",
            {"bookclub": book_club, "discussions": discussions, "members": members},
        )


def book_view(request, book_id):
    # book_id = request.GET.get("book_id")
    found_book = Book.objects.filter(book_id=book_id).first()
    if not found_book:
        subprocess.run(["python", "manage.py", "start_book_scraping", book_id])
        found_book = Book.objects.filter(book_id=book_id).first()

    bookshelf = get_list_containing_book(request, found_book)
    print(found_book)

    book_description = found_book.description
    if book_description is not None:
        book_description = book_description.split("/n/n")
    genre_list = found_book.genres.split(", ")

    atl_form = AddToListForm(initial={"shelf": bookshelf})
    coen_form = CreateOrEditNotificationForm()
    existing_notification = Notification.objects.filter(
        user=request.user, book=found_book
    ).first()

    if request.method == "POST":
        if "save_book_list" in request.POST:

            atl_form = AddToListForm(request.POST)
            handle_book_list(request, atl_form, found_book, bookshelf)
        elif "save_notification_button" in request.POST:
            coen_form = CreateOrEditNotificationForm(request.POST)
            handle_notification_list(request, coen_form, found_book)

        return HttpResponseRedirect(reverse("base:book-view", args=(book_id,)))

    return render(
        request,
        "book_sample.html",
        {
            "book": found_book,
            "book_description": book_description,
            "genre_list": genre_list,
            "bookshelf": bookshelf,
            "atl_form": atl_form,
            "coen_form": coen_form,
            "existing_notification": existing_notification,
        },
    )


def handle_book_list(request, form, book, bookshelf):
    if form.is_valid():
        if bookshelf is not None:
            getattr(request.user.profile, bookshelf).remove(book)
        new_shelf = form.cleaned_data["shelf"]
        getattr(request.user.profile, new_shelf).add(book)

        request.user.profile.save()


def handle_notification_list(request, form, book):
    user = request.user
    price = request.POST["price"]
    email = request.POST["email"]

    existing_notification = Notification.objects.filter(user=user, book=book).first()

    if form.is_valid():
        if existing_notification:
            existing_notification.price = price
            existing_notification.email = email
            existing_notification.save()
        else:
            new_notification = Notification.objects.create(
                user=user, price=price, email=email, book=book
            )
            request.user.profile.notifications_list.add(new_notification)
            request.user.profile.save()
    else:
        print(form.errors)


def get_list_containing_book(request, book):
    profile = get_object_or_404(Profile, user=request.user)
    # book = get_object_or_404(Book, book_id=book_id)
    # Check if the book is in any of the lists
    if book in profile.read_list.all():
        return "read_list"
    elif book in profile.reading_list.all():
        return "reading_list"
    elif book in profile.tbr_list.all():
        return "tbr_list"
    else:
        return None


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


def chapterdiscussion_view(request, book_id):
    # book_id = request.GET.get("book_id")
    found_book = Book.objects.filter(book_id=book_id).first()
    discussions = Discussion.objects.filter(type="chapter", object_id=1).order_by(
        "-last_update"
    )
    for discussion in discussions:
        discussion.chapter_title = discussion.title.split(" - ")[1]
        discussion.title = discussion.title.split(" - ")[0]
    return render(
        request,
        "chapter_discussion.html",
        {"book": found_book, "discussions": discussions},
    )


def forum_view(request):
    book_id = request.GET.get("book_id")
    found_book = Book.objects.filter(book_id=book_id).first()
    return render(request, "forum.html", {"book": found_book})


def discussion_view(request, discussion_id):
    user = request.user
    form = ResponseForm()

    # Retrieve the discussion object based on the discussion_id from the URL
    # discussion = get_object_or_404(Discussion, pk=discussion_id)
    discussion = Discussion.objects.get(id=discussion_id)
    posts = Post.objects.filter(discussion=discussion)
    discussion.num_posts = len(posts)
    if posts:
        discussion.last_update = posts.order_by("-pub_date")[0].pub_date
    discussion.save()

    if request.method == "POST":
        if not user.is_authenticated:
            print("You must login first.")
        else:
            if "delete_post_button" in request.POST:
                post_id_to_delete = request.POST["post_id_to_delete"]
                post_to_delete = Post.objects.get(id=post_id_to_delete)
                post_to_delete.delete()

            elif "create_post_button" in request.POST and user.is_authenticated:
                form = ResponseForm(request.POST)
                if form.is_valid():
                    content = form.cleaned_data["content"]
                    Post.objects.create(
                        discussion=discussion, user=user, content=content
                    )

            return HttpResponseRedirect(
                reverse("base:discussion-view", args=(discussion_id,))
            )

    return render(
        request,
        "discussions/discussion.html",
        {"form": form, "discussion": discussion, "posts": posts},
    )


def new_discussion_view(request):
    form = NewDiscussionForm()
    # Discussion.objects.create()
    if request.method == "POST":
        form = NewDiscussionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            type = form.cleaned_data["type"]
            # created_by = request.user
            content_type = BookClub if request.GET.get("type") == "bookclub" else Book
            content_type = ContentType.objects.get_for_model(content_type)
            object_id = request.GET.get("object_id")

            Discussion.objects.create(
                title=title,
                created_by=request.user,
                content=content,
                type=type,
                content_type=content_type,
                object_id=object_id,
            )

            return HttpResponseRedirect(
                reverse(
                    "base:book-club",
                    # args=(discussion_id,)
                )
            )

    return render(request, "forms/new_discussion_form.html", {"form": form})


def get_posts_for_discussion(discussion_id):
    posts = Post.objects.filter(discussion=discussion_id)
    return posts
