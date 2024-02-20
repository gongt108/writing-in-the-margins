import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin


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
