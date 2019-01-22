from django.db import models
from datetime import datetime

# Create your models here.

class ListingURL(models.Model):
    title = models.CharField(max_length=200)
    url = models.TextField(unique=True)
    scraped = models.BooleanField(default=False)


class Listing(models.Model):
    title = models.CharField(max_length=160)
    description = models.TextField(null=True)
    listingurl = models.ForeignKey(ListingURL, on_delete=models.CASCADE, null=True)
    html = models.TextField(null=True)
    location = models.TextField()
    time_posted = models.DateTimeField(default=datetime.now, blank=True)
    predicted_score = models.FloatField(null=True)
    user_score = models.FloatField(null=True)
    dismissed = models.BooleanField(default=False)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
