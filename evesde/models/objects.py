from django.db import models

from evesde.app_defines import *
from .types import Type
from .locations import System, Moon


class InSpaceObject(models.Model):
    """Represents a object in space"""
    id = models.BigIntegerField('Object ID', primary_key=True)
    type = models.ForeignKey(Type, related_name='assets')
    system = models.ForeignKey(System, related_name='assets')
    x = models.BigIntegerField('X Location', null=True)
    y = models.BigIntegerField('Y Location', null=True)
    z = models.BigIntegerField('Z Location', null=True)

    class Meta:
            app_label = 'evesde'

    def __unicode__(self):
        return '%s (%s)' % (self.type.name, self.system.name)
