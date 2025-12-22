from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Entry(models.Model):
    entry_title = models.CharField(default="Untitled")
    entry_text = models.CharField()
    entry_text_wordcount = models.PositiveIntegerField(default=1)
    tags = models.CharField(null=True, blank=True)  # A comma-separated list of tags
                                                    # TODO: Actually implement this
    creation_datetime = models.DateTimeField()
    last_edit_datetime = models.DateTimeField(null=True, blank=True)
    is_secret = models.BooleanField(default=False)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)