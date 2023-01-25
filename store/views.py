from django.http import HttpResponse
from django.core import serializers

from django_cache import settings
from django.core.cache import cache
from store.models import Product
from django.core.cache.backends.base import DEFAULT_TIMEOUT


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def products_view(request):
    objs = Product.objects.all()
    data = serializers.serialize('json', objs)
    return HttpResponse(data, content_type="application/json")


def products_cached_view(request):
    if 'product' in cache:
        data = cache.get('product')
        return HttpResponse(data, content_type="application/json")
    else:
        objs = Product.objects.all()
        data = serializers.serialize('json', objs)
        # store data in cache
        cache.set('product', data, timeout=CACHE_TTL)
        return HttpResponse(data, content_type="application/json")

