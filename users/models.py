from django.db import models
from django.contrib.auth.models import User
from base.models import BookClub, Book, Notification


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(default="default.jpg", upload_to="profile_pic")
    email = models.EmailField(default="")
    first_name = models.CharField(max_length=100, default="John")
    last_name = models.CharField(max_length=100, default="Doe")
    bookclub_admin = models.BooleanField(default=False, null=True)
    book_club = models.ForeignKey(BookClub, on_delete=models.SET_NULL, null=True)
    read_list = models.ManyToManyField(Book, blank=True, related_name="read_list")
    reading_list = models.ManyToManyField(Book, blank=True, related_name="reading_list")
    tbr_list = models.ManyToManyField(Book, blank=True, related_name="tbr_list")
    notifications_list = models.ManyToManyField(
        Notification,
        blank=True,
    )


# Intermediary models


# class ReadList(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

#     class Meta:
#         unique_together = ("profile", "book")


# class ReadingList(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

#     class Meta:
#         unique_together = ("profile", "book")


# class TBRList(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

#     class Meta:
#         unique_together = ("profile", "book")
