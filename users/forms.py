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


class ProfilePictureForm(forms.Form):
    profile_picture = forms.ChoiceField(
        choices=[
            (
                "https://i.redd.it/ai-new-characters-v0-r5ati85bf7ua1.jpg?width=1024&format=pjpg&auto=webp&s=39cc0ba21891f5fb4e11b599c970ae9a77557116",
                "Profile Picture 1",
            ),
            (
                "https://as1.ftcdn.net/v2/jpg/05/86/50/06/1000_F_586500663_IOXpv2HouDEiTsmrfjCHQtAd09f3TNkE.jpg",
                "Profile Picture 2",
            ),
            (
                "https://www.metastellar.com/wp-content/uploads/2023/06/Maria_Korolov_illustration_of_a_cute_bot_reading_a_book_02f788e8-bfe0-4834-8f7c-726b82ad0318-Midjourney.png",
                "Profile Picture 3",
            ),
            (
                "https://fiverr-res.cloudinary.com/images/q_auto,f_auto/gigs/344101039/original/f5a6d068a400d1565b529d5f8dabb468bf84d4c6/desing-fantasy-character-books-cover-children-illustration.png",
                "Profile Picture 4",
            ),
            (
                "https://img.freepik.com/premium-photo/illustration-painting-girl-reading-book-big-bulb-generate-ai_868783-918.jpg",
                "Profile Picture 5",
            ),
        ],
        widget=forms.RadioSelect,
    )
