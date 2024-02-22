import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Book(models.Model):
    book_cover = models.CharField()
    title = models.CharField()
    contributors = models.CharField()
    avg_rating = models.CharField()
    num_rating = models.CharField()
    description = models.TextField()
    genres = models.CharField()
    page_num = models.CharField()
    publication_date = models.CharField()
    book_id = models.CharField()


class BookClub(models.Model):
    name = models.CharField(max_length=100)
    book_id = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    member_list = models.ForeignKey(
        "MemberList", on_delete=models.CASCADE, related_name="book_club", null=True
    )
    next_meeting_date = models.DateTimeField(null=True)
    discussion_list_id = models.IntegerField(null=True)


class MemberList(models.Model):
    is_admin = models.BooleanField(default=False, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Discussion(models.Model):
    DISCUSSION_TYPES = [
        ("general", "General"),
        ("bookclub", "Book-club"),
        ("chapter", "Chapter-specific"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(default="")
    type = models.CharField(max_length=20, choices=DISCUSSION_TYPES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    last_update = models.DateTimeField()
    num_posts = models.PositiveIntegerField()
    date_created = models.DateTimeField(default=timezone.now)


class Post(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField("date published", auto_now_add=True)
