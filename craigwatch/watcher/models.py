from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model


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
    image_urls = models.TextField(default="")
    time_posted = models.DateTimeField(default=datetime.now, blank=True)
    predicted_score = models.FloatField(null=True)
    user_score = models.FloatField(null=True)
    dismissed = models.BooleanField(default=False)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def split_image_urls(self):
        return self.image_urls.split('\n')



class ListingRating(models.Model):
    pass

class KeywordPriorityPair(models.Model):
   keyword = models.CharField(max_length=220)
   priority = models.IntegerField(null=False)
   itemhunt = models.ForeignKey(
        'ItemHunt',
        on_delete=models.CASCADE,
    )

class ItemHunt(models.Model):
    zipcode     = models.CharField(max_length=5)
    radius      = models.IntegerField(null=True)
    section     = models.CharField(default="free",max_length=160)
    minprice    = models.FloatField(default=0.0)
    maxprice    = models.FloatField(default=float("inf"))
    listing_age = models.FloatField(null=False)
    user        = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True
    )

