from django import forms


class SearchForm(forms.Form):
    search_term = forms.CharField(label="", max_length=100)
