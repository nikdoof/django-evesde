from django.test import TestCase
from evesde.models.locations import Station
from evesde.eveapi.eve import import_conquerable_stations


class TestConquerableStationsImport(TestCase):
    """Tests the import_conquerable_stations function"""

    def setUp(self):
        Station.objects.all().delete()

    def test_import_stations(self):
        import_conquerable_stations()
        self.assertGreater(Station.objects.count(), 0)

