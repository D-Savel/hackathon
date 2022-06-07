from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from application.models import Object, Object2
from application.serializers import ObjectSerializer, Object2Serializer


class ObjectViewset(ReadOnlyModelViewSet) :

    serializer_class = ObjectSerializer

    def get_queryset(self):
        queryset = Object.objects.all()
        object_active = self.request.GET.get('object_active')
        if object_active :
            queryset = queryset.filter(active = object_active)
        return queryset




class Object2Viewset(ReadOnlyModelViewSet) :

    serializer_class = Object2Serializer

    def get_queryset(self):
        queryset = Object.objects.all()
        object_active = self.request.GET.get('object_active')
        if object_active :
            queryset = queryset.filter(active = object_active)
        return queryset