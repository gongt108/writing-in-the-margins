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
