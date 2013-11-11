import imp
from datetime import timedelta
from django.utils.timezone import now
from django.utils.module_loading import import_by_path
from django.conf import settings
from eveapi import EVEAPIConnection

from evesde.models.cache import EVEAPICache


class EVEAPICache(object):

    def hash(self, data):
        from hashlib import sha1
        return sha1('-'.join(data)).hexdigest()

    def store(self, host, path, params, doc, obj):
        key = self.hash((host, path, str(params.items())))
        cached = now() + timedelta(seconds=obj.cachedUntil - obj.currentTime)

        try:
            obj = EVEAPICache.objects.get(key=key)
        except EVEAPICache.DoesNotExist:
            EVEAPICache.objects.create(key=key, cache_until=cached, document=doc)
        else:
            obj.cache_until = cached
            obj.document = doc
            obj.save()

    def retrieve(self, host, path, params):
        key = self.hash((host, path, str(params.items())))
        try:
            obj = EVEAPICache.objects.get(key=key)
        except EVEAPICache.DoesNotExist:
            pass
        else:
            if obj.cache_until >= now():
                return obj.document
        return None


def get_api_connection():
    cache_handler = getattr(settings, 'EVE_SDE_CACHE_HANDLER', 'evesde.eveapi.EVEAPICache')
    cache_obj = import_by_path(cache_handler)
    return EVEAPIConnection(cacheHandler=cache_obj)