import requests
import random
import sys
import os
import re
import geopy.distance 
import logging
import logging.config
import pdb
import json
import traceback


from django.core.management.base import BaseCommand, CommandError
from watcher.models import Listing
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from dateutil import parser
from collections import namedtuple
from watcher.models import ListingURL

my_coordinates = (40.694861, -73.948087)

dirname = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dirname,'user_agents.txt'),'r') as f:
    user_agents = [line.strip() for line in f.readlines()]

LOGGING_CONFIG = None
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        }
    },
    'loggers': {
    # root logger
        '': {
            'level': 'INFO',
            'handlers': ['console'],
        },
    },
})





class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    

    def add_arguments(self, parser):
        parser.add_argument('--url',
                        dest='debugurl',
                        action='store',
                        type=str
        )
        pass

    def handle(self, *args, **options):

        debugurl = options.get('debugurl')

        if debugurl is None:

            lurl = ListingURL.objects.filter(scraped=False).first()
            if lurl is None:
                logging.info("No unscraped urls.")
                return

            listing_url = lurl.url
        else:
            listing_url = debugurl

        r = requests.get(listing_url,headers={'User-Agent': random.sample(user_agents,1)[0]})

        if not r.ok:
            raise Exception("Received error code {} from {}\n{}".format(r.status_code,full_url,r.content))

            

        soup = BeautifulSoup(r.content,'lxml')

        ## Perhaps replace these ugly try-catches with something else?
        if self.is_removed(soup):
            logging.info("Listing {} was removed by its author.".format(listing_url))
            lurl.scraped = True
            lurl.save()
            return

        listing = Listing()


        ## this should be made less ugly 
        try:
            listing.latitude, listing.longitude = self.get_coordinates(soup)
        except:
            logging.info("Couldn't get coordinates from {}.".format(url))

        try:
            listing.description = self.get_description(soup).strip()
            logging.info("Description:\n{}".format(listing.description))
        except:
            logging.info("Couldn't get description from {}.".format(url))

        try:
            listing.timestamp = self.get_timestamp(soup)
            logging.info("Post Timestamp: {}".format(listing.timestamp))

        except:
            logging.info("Couldn't get timestamp from {}.".format(url))

        try:
            image_urls = self.get_image_urls(soup)
            listing.image_urls = '\n'.join(image_urls)
            logging.info("Got {} images.".format(len(image_urls)))
        except Exception as e:
            pdb.set_trace()
            traceback.print_exc()
            logging.info("Couldn't get images.")

        if debugurl:
            return


        listing.html = r.content
        listing.title = lurl.title
        listing.listingurl = lurl
        listing.save()

        lurl.scraped = True
        lurl.save()


        logging.info("Title:{}".format(listing.title,))
        logging.info("URL:{}".format(listing.listingurl.url))



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

    def get_image_urls_from_script(self,script):
        """
<script type="text/javascript"><!--
var imgList = [{"shortid":"71pliC1bfyo","url":"https://images.craigslist.org/00v0v_71pliC1bfyo_600x450.jpg","thumb":"https://images.craigslist.org/00v0v_71pliC1bfyo_50x50c.jpg","imgid":"1:00v0v_71pliC1bfyo"},{"shortid":"crvBC0l6mzu","url":"https://images.craigslist.org/01212_crvBC0l6mzu_600x450.jpg","thumb":"https://images.craigslist.org/01212_crvBC0l6mzu_50x50c.jpg","imgid":"1:01212_crvBC0l6mzu"},{"shortid":"cLjMIEXU844","url":"https://images.craigslist.org/01717_cLjMIEXU844_600x450.jpg","thumb":"https://images.craigslist.org/01717_cLjMIEXU844_50x50c.jpg","imgid":"1:01717_cLjMIEXU844"},{"shortid":"jQ3JxHTRn5D","url":"https://images.craigslist.org/01414_jQ3JxHTRn5D_600x450.jpg","thumb":"https://images.craigslist.org/01414_jQ3JxHTRn5D_50x50c.jpg","imgid":"1:01414_jQ3JxHTRn5D"}];
--></script>
        """

        pat = re.compile(r'\[.*\]')
        source = script.text

        try:
            obj = json.loads(pat.search(source)[0])
            return [image["url"] for image in obj]

        except Exception as e:
            traceback.print_exc()
            return []



    def get_image_urls(self, soup: BeautifulSoup):


        figure = soup.find('figure',{'class':['iw','multiimage']})
        script = figure.find('script')
        if script is not None:
            script_img_urls = self.get_image_urls_from_script(script)
            if script_img_urls:
                return script_img_urls


        gallery = soup.find('div',{'class':'gallery'})
        if gallery is None:
            return []
        image_urls = []
        for element in gallery.findAll('img'):

            ## I'm in 3.7 
            src = element.get('src')
            if src is not None and src != "":
                image_urls.append(src)


            ## In Python 3.8 you should be able to do this
            # if src_url := element.get('src_url') is not None:
            #     images_urls.append(src_url)


        return image_urls