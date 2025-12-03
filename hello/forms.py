from django import forms
from .models import Entry

SORTING_METHODS = {
    "creation_datetime": "Creation Date",
    "last_edit_datetime": "Last Edited",
    "entry_text_wordcount": "Word Count",
}

SORTING_DIRECTIONS = {
    "desc": "Descending",
    "asc": "Ascending",
}

class AddOrEditEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["is_secret", "entry_title", "entry_text", "creation_datetime"]
    entry_title = forms.CharField(label="", max_length=200, initial="Title")
    is_secret = forms.BooleanField(required=False)
    entry_text = forms.CharField(label="", widget=forms.Textarea)


class EntrySearchForm(forms.Form):
    query_text = forms.CharField(label="Search...", required=False)
    sort_by = forms.ChoiceField(label="Sort by", choices=SORTING_METHODS, initial=SORTING_METHODS["creation_datetime"], required=False)
    sort_dir = forms.ChoiceField(label="Direction", choices=SORTING_DIRECTIONS, initial=SORTING_DIRECTIONS, required=False)