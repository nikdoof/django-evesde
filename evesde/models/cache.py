from django.db import models


class EVEAPICache(models.Model):

    key = models.CharField('Cache Key', blank=False, max_length=40)
    cache_until = models.DateTimeField('Cached Until', blank=False)
    document = models.TextField('Document')

    class Meta:
            app_label = 'evesde'

    def __unicode__(self):
        return '%(key)s - %(cache_until)s' % self.__dict__