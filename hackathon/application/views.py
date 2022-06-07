from django.shortcuts import render
from application.models import Object, Object2

# Create your views here.

def object_list (request) :
    objects = Object.objects.all()
    return render (request, 'application/object_list.html', {'objects': objects})


def object2_list (request) :
    objects = Object2.objects.all()
    return render (request, 'application/object2_list.html', {'objects': objects})


