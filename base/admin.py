from django import forms
from django.contrib import admin
from .models import Book, BookClub, Discussion, Post, Notification


# Register your models here.
class BookClubAdminForm(forms.ModelForm):
    class Meta:
        model = BookClub
        fields = "__all__"  # Include all fields of the BookClub model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark fields as optional
        self.fields["link_id"].required = False
        self.fields["book_id"].required = False
        self.fields["next_meeting_date"].required = False


class BookClubAdmin(admin.ModelAdmin):
    form = BookClubAdminForm


admin.site.register(BookClub, BookClubAdmin)


# class MemberAdminForm(forms.ModelForm):
#     class Meta:
#         model = Member
#         fields = "__all__"

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Mark fields as optional
#         self.fields["book_club"].required = False


# class MemberAdmin(admin.ModelAdmin):
#     form = MemberAdminForm


# admin.site.register(Member, MemberAdmin)

admin.site.register(Discussion)
admin.site.register(Post)
admin.site.register(Book)
admin.site.register(Notification)
