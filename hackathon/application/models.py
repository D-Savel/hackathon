from django.db import models


# Create your models here.


class Object(models.Model):

    name = models.fields.CharField(max_length=100)

    description = models.fields.CharField(max_length=500)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Object2(models.Model):

    name = models.fields.CharField(max_length=100)

    description = models.fields.CharField(max_length=500)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name