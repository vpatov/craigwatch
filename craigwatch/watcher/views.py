from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ModelForm


from .models import Listing, ItemHunt



class ItemHuntForm(ModelForm):
    class Meta:
        model = ItemHunt
        fields = ['name', 'zipcode','radius','section','minprice','maxprice','listing_age']




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


def edit_itemhunt(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden(request)


    user = get_user_model().objects.get(username=request.user.username)

    if request.path == '/watcher/edit_itemhunt/new':
        itemhuntform = ItemHuntForm()
        itemhuntform.user = user


    else:
        ihname = request.GET.get('ihname',None)
        if ihname is None:
            return HttpResponseBadRequest(request)
        itemhunt = ItemHunt.objects.get(user=user,name=ihname)
        itemhuntform = ItemHuntForm(instance=itemhunt)


    context = {
        "itemhuntform": itemhuntform
    }

    return render(request, 'watcher/edit_itemhunt.html',context)

    


def process_itemhunt(request):


    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    import pdb
    pdb.set_trace()

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
        return HttpResponseForbidden()

    context = {}
        
    return render(request, 'watcher/preferences.html', context)
    

def manage_itemhunts(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    user = get_user_model().objects.get(username=request.user.username)
    itemhunts = ItemHunt.objects.filter(user=user)

    context = {
        'itemhunts':itemhunts
    }



    return render(request, 'watcher/manage_itemhunts.html', context)

def settings(request):
    return HttpResponse("<h1>This is the settings page.</h1><p>Coming Soon</p>")
