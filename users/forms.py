from django import forms
from django.db import models
from django.db.models import fields
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username", "password"]


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ["email", "first_name", "last_name"]
