from django.contrib import admin

# Register your models here.
from .models import *

for model in [Listing, ListingURL, ItemHunt, KeywordPriorityPair]:
    admin.site.register(model)