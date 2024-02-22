from django import forms
from django.contrib import admin
from .models import BookClub, Discussion, Post


# Register your models here.
class BookClubAdminForm(forms.ModelForm):
    class Meta:
        model = BookClub
        fields = "__all__"  # Include all fields of the BookClub model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark fields as optional
        self.fields["book_id"].required = False
        self.fields["member_list"].required = False
        self.fields["next_meeting_date"].required = False
        self.fields["discussion_list_id"].required = False


class BookClubAdmin(admin.ModelAdmin):
    form = BookClubAdminForm


admin.site.register(BookClub, BookClubAdmin)

admin.site.register(Discussion)
admin.site.register(Post)
