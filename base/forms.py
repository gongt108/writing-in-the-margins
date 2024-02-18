from django import forms


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
