import requests
import random
import sys
from django.core.management.base import BaseCommand, CommandError
from watcher.models import Listing
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from collections import namedtuple
from watcher.models import ListingURL

with open('user_agents.txt','r') as f:
    user_agents = [line.strip() for line in f.readlines()]


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        params = {
            "postal":11206,
            "search_distance":6,
            "s":0
        }

        base_url = "https://newyork.craigslist.org/search/zip?"

        paramstr = urlencode(params)
        full_url = base_url + paramstr
        r = requests.get(full_url,headers={'User-Agent':random.sample(user_agents,1)[0]})

        if not r.ok:
            raise Exception("Received error code {} from {}\n{}".format(r.status_code,full_url,r.content))

        try:
            soup = BeautifulSoup(r.content,'lxml')
            links_html = soup.find_all('a',{'class':"result-title hdrlnk"})
            listing_urls = [ListingURL(url=link.get('href'),title=link.text,scraped=False) for link in links_html]

            count=0
            already_scraped = set([lurl.url for lurl in ListingURL.objects.all()])
            for listing_url in listing_urls:
                if listing_url.url in already_scraped:
                    continue
                listing_url.save()
                count+=1

            sys.stderr.write("Found {} new URLs.".format(count))
        except Exception as e:
            raise(e)


        # for poll_id in options['poll_id']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))