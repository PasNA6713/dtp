from datetime import datetime

from django.db import models
from django.contrib.postgres.fields import ArrayField


class Dtp(models.Model):
    datetime = models.DateTimeField('datetime', default=datetime.now())

    parent_region = models.CharField('parent_region', max_length=150)
    region = models.CharField('region', max_length=150)
    address = models.CharField('region', max_length=150, blank=True, null=True)
    lat = models.FloatField('latitude')
    long = models.FloatField('longitude')
   
    category = models.CharField('category', max_length=150, blank=True, null=True)
    deaths = models.IntegerField('deaths', default=0)
    injured = models.IntegerField('injured', default=0)

    light = models.CharField('light', max_length=150, blank=True, null=True)
    weather = ArrayField(models.CharField('weather', max_length=1000), blank=True, null=True)
    nearby = ArrayField(models.CharField('nearby', max_length=1000), blank=True, null=True)
    road_conditions = ArrayField(models.CharField('road_conditions', max_length=1000), blank=True, null=True)

    def __repr__(self):
        return '{}/{}'.format(self.datetime, self.region)

    def __str__(self):
        return '{}/{}'.format(self.datetime, self.region)
