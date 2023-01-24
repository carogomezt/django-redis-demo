from django.http import HttpResponse
from django.core import serializers

from store.models import Product


# Create your views here.

def products_view(request):
    objs = Product.objects.all()
    data = serializers.serialize('json', objs)
    return HttpResponse(data, content_type="application/json")
