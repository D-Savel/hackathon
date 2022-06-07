from rest_framework.serializers import ModelSerializer

from application.models import Object, Object2






class ObjectSerializer(ModelSerializer):

    class Meta:
        model = Object
        fields = ['id', 'name', 'date_created', 'date_updated']


class Object2Serializer(ModelSerializer):

    class Meta:
        model = Object2
        fields = ['id', 'name', 'date_created', 'date_updated']