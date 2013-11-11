from math import sqrt
from django.db import models
from evesde.utils import euclidean_distance
from evesde.app_defines import DISTANCE_LIGHT_YEAR
from evesde.models.utils import InheritanceQuerySet


class LocationManager(models.Manager):

    def all_subclassed(self):
        return InheritanceQuerySet(model=self.model).select_subclasses()


class Location(models.Model):
    """
    Parent model for Locations
    """
    id = models.BigIntegerField('Location ID', primary_key=True)
    name = models.CharField('Name', max_length=255)
    x = models.DecimalField('X', max_digits=22, decimal_places=0)
    y = models.DecimalField('Y', max_digits=22, decimal_places=0)
    z = models.DecimalField('Z', max_digits=22, decimal_places=0)

    objects = LocationManager()

    def __unicode__(self):
        return u"%(name)s" % self.__dict__

    class Meta:
        app_label = 'evesde'
        ordering = ['name']


class Region(Location):
    """
    Represents a EVE region
    """

    @property
    def systems(self):
        return System.objects.filter(constellation__in=self.constellations.all())

    @property
    def planets(self):
        return Planet.objects.filter(system__constellation__in=self.constellations.all())

    @property
    def moons(self):
        return Moon.objects.filter(planet__system__constellation__in=self.constellations.all())

    class Meta:
        app_label = 'evesde'
        ordering = ['name']


class Constellation(Location):
    """
    Represents a Constellation
    """
    region = models.ForeignKey(Region, related_name='constellations')

    @property
    def planets(self):
        return Planet.objects.filter(system__in=self.systems.all())

    @property
    def moons(self):
        return Moon.objects.filter(planet__system__in=self.systems.all())

    class Meta:
        app_label = 'evesde'
        ordering = ['name']


class System(Location):
    """
    Represents a System
    """

    SYSTEM_SECURITY_CLASS_HIGHSEC = 1
    SYSTEM_SECURITY_CLASS_LOWSEC = 2
    SYSTEM_SECURITY_CLASS_NULLSEC = 3

    SYSTEM_SECURITY_CLASS_CHOICES = (
        (SYSTEM_SECURITY_CLASS_HIGHSEC, 'Highsec'),
        (SYSTEM_SECURITY_CLASS_LOWSEC, 'Lowsec'),
        (SYSTEM_SECURITY_CLASS_NULLSEC, 'Nullsec'),
    )

    # http://blog.evepanel.net/eve-online/igb/colors-of-the-security-status.html
    SYSTEM_SECURITY_CLASS_COLORS = dict([
        (1.0, '#2FEFEF'),
        (0.9, '#48F0C0'),
        (0.8, '#00EF47'),
        (0.7, '#00F000'),
        (0.6, '#8FEF2F'),
        (0.5, '#EFEF00'),
        (0.4, '#D77700'),
        (0.3, '#F06000'),
        (0.2, '#F04800'),
        (0.1, '#D73000'),
        (0.0, '#F00000'),
    ])

    constellation = models.ForeignKey(Constellation, related_name='systems')
    jumps = models.ManyToManyField('self', through='SystemJump', symmetrical=False, related_name='+')
    security = models.DecimalField('Security', max_digits=2, decimal_places=1)

    @property
    def security_class(self):
        if self.security <= 0:
            return self.SYSTEM_SECURITY_CLASS_NULLSEC
        elif self.security <= 0.4:
            return self.SYSTEM_SECURITY_CLASS_LOWSEC
        return self.SYSTEM_SECURITY_CLASS_HIGHSEC

    def get_security_class_display(self):
        sec = self.security_class
        for val, name in self.SYSTEM_SECURITY_CLASS_CHOICES:
            if val == sec:
                return name
        return "Unknown"

    def get_system_color(self):
        if self.security < 0:
            return self.SYSTEM_SECURITY_CLASS_COLORS[0.0]
        else:
            return self.SYSTEM_SECURITY_CLASS_COLORS[float(self.security)]

    @property
    def region(self):
        return self.constellation.region

    @property
    def moons(self):
        return Moon.objects.filter(planet__in=self.planets.all())

    def distance_to(self, destination):
        """Calculates the ly distance between the two systems"""
        if not isinstance(destination, System):
            raise ValueError('Provided destination is not a System.')
        origin = (self.x, self.y, self.z)
        destination = (destination.x, destination.y, destination.z)
        return euclidean_distance(origin, destination) / DISTANCE_LIGHT_YEAR

    class Meta:
        app_label = 'evesde'
        ordering = ['name']


class Planet(Location):
    system = models.ForeignKey(System, related_name='planets')

    class Meta:
        app_label = 'evesde'


class Moon(Location):
    planet = models.ForeignKey(Planet, related_name='moons')

    class Meta:
        app_label = 'evesde'


class SystemJump(models.Model):
    from_system = models.ForeignKey(System, related_name='+')
    to_system = models.ForeignKey(System, related_name='+')

    def __unicode__(self):
        return u"%s to %s" % (self.from_system, self.to_system)

    class Meta:
        app_label = 'evesde'


class Station(Location):
    system = models.ForeignKey(System, related_name='stations')

    class Meta:
        app_label = 'evesde'