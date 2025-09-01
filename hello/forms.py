from django import forms
from .models import Entry

class AddOrEditEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["is_secret", "entry_title", "entry_text", "creation_datetime"]
    entry_title = forms.CharField(label="", max_length=200, initial="Title")
    is_secret = forms.BooleanField(required=False)
    entry_text = forms.CharField(label="", widget=forms.Textarea)