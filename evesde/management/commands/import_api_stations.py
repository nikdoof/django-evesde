from django.core.management.base import BaseCommand
from django.db import transaction
from evesde.models.locations import Station
from eveapi import EVEAPIConnection


class Command(BaseCommand):
    help = 'Imports outposts from the EVE API.'

    def handle(self, *args, **options):
        api = EVEAPIConnection()
        stations = Station.objects.all()

        objs = []
        for station in api.eve.ConquerableStationList().outposts:
            print "Importing %s" % station.stationName
            try:
                obj = stations.get(pk=station.stationID)
            except Station.DoesNotExist:
                obj = Station(pk=station.stationID)
            obj.name = station.stationName
            obj.system_id = station.solarSystemID
            objs.append(obj)

        with transaction.atomic():
            for obj in objs:
                obj.save()
