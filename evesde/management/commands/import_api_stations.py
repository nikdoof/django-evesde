from django.core.management.base import BaseCommand
from evesde.eveapi.eve import import_conquerable_stations

class Command(BaseCommand):
    help = 'Imports outposts from the EVE API.'

    def handle(self, *args, **options):
        import_conquerable_stations()