from django.contrib import admin
from django import forms
from .models import Profile


# Register your models here.
class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"  # Include all fields of the BookClub model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark fields as optional
        self.fields["bookclub_admin"].required = False
        self.fields["book_club"].required = False


class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm


admin.site.register(Profile, ProfileAdmin)
# admin.site.register(Profile)
