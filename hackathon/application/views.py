from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from application.models import Object, Object2
import requests
import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()


# Create your views here.

def object_list (request) :
    objects = Object.objects.all()
    return render (request, 'application/object_list.html', {'objects': objects})

def object_details(request, id):
    object = Object.objects.get(id=id)
    return render (request, 'application/object_details.html', {'object' : object})



def object2_list (request) :
    objects = Object2.objects.all()
    return render (request, 'application/object2_list.html', {'objects': objects})

def object2_details(request, id):
    object = Object2.objects.get(id=id)
    return render (request, 'application/object2_details.html', {'object' : object})

def geoapi(request):

    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
    # use api with your ip Address for retrieve geodata
    response = requests.get('http://ip-api.com/json/%s' % ip_address)
    geodata = response.json()
    lat = geodata['lat']
    lon = geodata['lon']
    API_KEY = env("API_KEY")
    # prepare url for display a map with api
    # API use api-key given by locationiq
    # API_KEY must be save in .env file at the root of the project (same as settings.py)
    # API_KEY=<YOUR_API_KEY> (without '')
    url = f"""https://maps.locationiq.com/v3/staticmap?key={API_KEY}&center=43.66,3.9726&size=800x800&zoom=13&markers=size:small|color:red|{lat},{lon}"""

    return render(request, 'application/geoapi.html', {
        'ip': geodata['query'],
        'country': geodata['country'],
        'latitude': geodata['lat'],
        'longitude': geodata['lon'],
        'city': geodata['city'],
        'url': url
    })

