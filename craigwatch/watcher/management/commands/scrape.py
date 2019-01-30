import requests
import random
import sys
import os
import geopy.distance 

from django.core.management.base import BaseCommand, CommandError
from watcher.models import Listing
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from dateutil import parser
from collections import namedtuple
from watcher.models import ListingURL

my_coordinates = (40.694861, -73.948087)

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(SITE_ROOT,'user_agents.txt'),'r') as f:
    user_agents = [line.strip() for line in f.readlines()]


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):

        lurl = ListingURL.objects.filter(scraped=False).first()
        title, url = lurl.title, lurl.url

        r = requests.get(url,headers={'User-Agent': random.sample(user_agents,1)[0]})

        if not r.ok:
            raise Exception("Received error code {} from {}\n{}".format(r.status_code,full_url,r.content))


        try:
            soup = BeautifulSoup(r.content,'lxml')

        except Exception as e:
            raise(e)

        finally:
            lurl.scraped = True
            lurl.save()



        ## Perhaps replace these ugly try-catches with something else?
        if self.is_removed(soup):
            sys.stderr.write("Listing {} was removed by its author.".format(url))
            return

        listing = Listing()

        try:
            listing.latitude, listing.longitude = self.get_coordinates(soup)
        except:
            sys.stderr.write("Couldn't get coordinates from {}.".format(url))

        try:
            listing.description = self.get_description(soup).strip()
            sys.stderr.write("description:{}".format(listing.description))
        except:
            sys.stderr.write("Couldn't get description from {}.".format(url))

        try:
            listing.timestamp = self.get_timestamp(soup)
        except:
            sys.stderr.write("Couldn't get timestamp from {}.".format(url))

        listing.html = r.content
        listing.title = title
        listing.listingurl = lurl
        listing.save()

        sys.stderr.write("Just saved Title:{}\nURL:{}\n".format(listing.title, listing.listingurl.url))



    def is_removed(self,soup: BeautifulSoup):
        removed_div = soup.find('div',{'class':'removed'})
        if removed_div is not None:
            return True


    def get_timestamp(self,soup: BeautifulSoup):
        timetag = soup.find('time',{'class':['date','timeago']})
        datestr = timetag.get('datetime')
        timestamp = parser.parse(datestr)
        return timestamp


    def get_coordinates(self,soup: BeautifulSoup):

        map_leaflet = soup.find('div',{"class":["viewposting","leaflet-container"]})
        latitude = map_leaflet.get('data-latitude')
        longitude = map_leaflet.get('data-longitude')

        coords = (latitude, longitude)

        return coords

    def get_description(self,soup: BeautifulSoup):

        section = soup.find('section',{'id':'postingbody'})
        section.find('p',{'class':'print-qrcode-label'}).decompose()   
        return section.text

