
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.shortcuts import get_list_or_404
from .models import Property
from .utils import get_all_properties

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    properties = get_all_properties()  # Fetch from Redis or DB
    return JsonResponse({
        "data": list(properties)
    })