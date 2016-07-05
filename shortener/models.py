from __future__ import unicode_literals

from django.db import models


class UrlList(models.Model):
    original_url = models.URLField()
    shorten_url = models.URLField(null=True)
    date_add = models.DateTimeField()
    date_click = models.DateTimeField(null=True)
    clicks = models.IntegerField(null=True)
