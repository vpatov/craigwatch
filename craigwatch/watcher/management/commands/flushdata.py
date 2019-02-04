from django.core.management.base import BaseCommand, CommandError
from watcher.models import Listing, ListingURL, ItemHunt

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    

    def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=int)
        pass

    def handle(self, *args, **options):

        Listing.objects.all().delete()
        ListingURL.objects.all().delete()
        ItemHunt.objects.all().delete()
