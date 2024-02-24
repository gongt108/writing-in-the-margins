from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field


class SearchForm(forms.Form):
    search_query = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search for books...",
                "class": "w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500",
                "required": True,
            }
        ),
    )


class ResponseForm(forms.Form):
    content = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(ResponseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

        self.fields["content"].label = ""


class NewDiscussionForm(forms.Form):
    DISCUSSION_TYPES = [
        ("bookclub", "Book-club"),
        ("general", "General"),
    ]

    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea(attrs={"style": "resize: none;"}))
    type = forms.ChoiceField(
        choices=DISCUSSION_TYPES, widget=forms.Select(attrs={"class": "form-control"})
    )


class AddToListForm(forms.Form):
    OPTIONS = (
        ("read_list", "Read"),
        ("reading_list", "Currently Reading"),
        ("tbr_list", "TBR"),
    )
    shelf = forms.ChoiceField(choices=OPTIONS, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        # bookshelf = kwargs.pop("bookshelf", None)  # Get the value of bookshelf
        super(AddToListForm, self).__init__(*args, **kwargs)

        # print("Initial value of shelf field:", self.fields["shelf"].initial)

        # if bookshelf is not None:  # Set the initial value if bookshelf is provided
        #     self.fields["shelf"].initial = bookshelf
        #     print("Initial value of shelf field 2:", self.fields["shelf"].initial)

        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
        self.fields["shelf"].label = ""
