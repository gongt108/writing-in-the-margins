import datetime
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
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
    link_id = models.CharField(max_length=255, unique=True)
    book_id = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    next_meeting_date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        # Generate the link_id using the primary key (pk) and name
        if not self.pk:
            # Save the instance to get a primary key (pk)
            super().save(*args, **kwargs)

            self.link_id = f"{self.pk}-{slugify(self.name)}"
        super().save(*args, **kwargs)


class Member(models.Model):
    is_admin = models.BooleanField(default=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_club = models.ForeignKey(BookClub, on_delete=models.SET_NULL, null=True)


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
    last_update = models.DateTimeField(default=timezone.now)
    num_posts = models.PositiveIntegerField(default=0)
    date_created = models.DateTimeField(default=timezone.now)


class Post(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField("date published", auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.IntegerField()
    email = models.CharField(default="")
