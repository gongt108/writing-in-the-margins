from django.db import models
from django.contrib.auth.models import User
from base.models import BookClub


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(default="default.jpg", upload_to="profile_pic")
    email = models.EmailField(default="")
    first_name = models.CharField(max_length=100, default="John")
    last_name = models.CharField(max_length=100, default="Doe")
    bookclub_admin = models.BooleanField(default=False, null=True)
    book_club = models.ForeignKey(BookClub, on_delete=models.SET_NULL, null=True)
