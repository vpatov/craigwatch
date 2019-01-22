from django.shortcuts import render
from django.http import HttpResponse

from .models import Listing

def index(request):
    # return HttpResponse("Watcher Home Page.")

    listings = Listing.objects.all()[:10]

    context = {
        'title': 'Hottest Listings',
        'listings': listings    
    }

    return render(request, 'watcher/index.html', context)


def listing_page(request, id):
    listing = Listing.objects.get(id=id)


    context = {
        'listing': listing
    }

    return render(request, 'watcher/listing.html', context)


def settings(request):
    return HttpResponse("<h1>This is the settings page.</h1><p>Coming Soon</p>")
