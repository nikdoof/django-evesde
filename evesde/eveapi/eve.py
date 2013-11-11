from django.db import transaction

from evesde.models.locations import Station
from evesde.eveapi import get_api_connection


def import_conquerable_stations():
    """Import all conquerable stations and outposts from the EVE API"""
    api = get_api_connection()
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
        obj.x = 0
        obj.y = 0
        obj.z = 0
        objs.append(obj)

    with transaction.atomic():
        for obj in objs:
            obj.save()