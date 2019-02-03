from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ModelForm


from .models import Listing, ItemHunt



class ItemHuntForm(ModelForm):
    class Meta:
        model = ItemHunt
        fields = ['zipcode','radius','section','minprice','maxprice','listing_age']




def index(request):
    # return HttpResponse("Watcher Home Page.")

    listings = Listing.objects.all()

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


def add_itemhunt(request):


    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    print(request.method)
    if request.method == 'POST':

        form = ItemHuntForm(request.POST)

        if form.is_valid():
            user = get_user_model().objects.get(username=request.user.username)
            # Create, but don't save the new author instance.
            new_itemhunt = form.save(commit=False)
            new_itemhunt.user = user
            new_itemhunt.save()

            return HttpResponseRedirect('watcher/preferences')
    else:
        return HttpResponseForbidden()





    




from django.shortcuts import render


def preferences_page(request):
    # Get User's keywords / scores
    # Get User's zipcode

    if not request.user.is_authenticated:
        return 403


    user = get_user_model().objects.get(username=request.user.username)
    itemhunts = ItemHunt.objects.filter(user=user)

    itemhuntform = ItemHuntForm()

    context = {
        "itemhunts" : itemhunts,
        "itemhuntform": itemhuntform
    }

    return render(request, 'watcher/preferences.html', context)


def settings(request):
    return HttpResponse("<h1>This is the settings page.</h1><p>Coming Soon</p>")
