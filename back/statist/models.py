from django.db import models

from django_pandas.managers import DataFrameManager


COUNTER = 0

class Dtp(models.Model):
    date = models.TextField('date')
    Time = models.CharField('Time', max_length=150)
    District = models.CharField('District', max_length=150)
    DTP_V = models.CharField('DTP_V', max_length=150)
    POG = models.IntegerField('POG')
    RAN = models.IntegerField('RAN')
    K_UCH = models.IntegerField('K_UCH')
    n_p = models.CharField('n_p', max_length=150)
    street = models.CharField('street', max_length=150)
    house = models.CharField('house', null=True, max_length=150)
    dor = models.CharField('dor', max_length=150, null=True)
    factor = models.CharField('factor', max_length=150)
    s_pog = models.CharField('s_pog', max_length=150)
    s_pch = models.CharField('s_pch', max_length=150)
    osv = models.CharField('osv', max_length=150)
    latitude = models.FloatField('latitude')
    longitude = models.FloatField('longitude')
    OBJ_DTP = models.CharField('OBJ_DTP', max_length=150)
    change_org_motion = models.CharField('change_org_motion', max_length=150)
    time_group = models.IntegerField('time_group', default=0)

    objects = DataFrameManager()

    def __iter__(self):
        global COUNTER
        yield from {
            "type": "Feature",
            "id": COUNTER,
            "geometry": {
                "type": "Point",
                "coordinates": [self.latitude, self.longitude]
            }
        }.items()
        COUNTER += 1

    def str(self):
        return '{}/{}'.format(self.date, self.District)


class Dtp_outside(models.Model):
    date = models.TextField('date')
    Time = models.CharField('Time', max_length=150)
    District = models.CharField('District', max_length=150)
    DTP_V = models.CharField('DTP_V', max_length=150)
    POG = models.IntegerField('POG')
    RAN = models.IntegerField('RAN')
    K_UCH = models.IntegerField('K_UCH')
    n_p = models.CharField('n_p', max_length=150)
    street = models.CharField('street', null=True, max_length=150)
    house = models.CharField('house', null=True, max_length=150)
    dor = models.CharField('dor', max_length=150, null=True)
    factor = models.CharField('factor', max_length=150)
    s_pog = models.CharField('s_pog', max_length=150)
    s_pch = models.CharField('s_pch', max_length=150)
    osv = models.CharField('osv', max_length=150)
    latitude = models.FloatField('latitude')
    longitude = models.FloatField('longitude')
    OBJ_DTP = models.CharField('OBJ_DTP', max_length=150)
    change_org_motion = models.CharField('change_org_motion', max_length=150)
    time_group = models.IntegerField('time_group', default=0)

    objects = DataFrameManager()

    def __iter__(self):
        global COUNTER
        yield from {
            "type": "Feature",
            "id": COUNTER,
            "geometry": {
                "type": "Point",
                "coordinates": [self.latitude, self.longitude]
            }
        }.items()
        COUNTER += 1


class PiterDtp(models.Model):
    date = models.TextField('date')
    Time = models.CharField('Time', max_length=150)
    District = models.CharField('District', max_length=150)
    DTP_V = models.CharField('DTP_V', max_length=150)
    POG = models.IntegerField('POG')
    RAN = models.IntegerField('RAN')
    K_UCH = models.IntegerField('K_UCH')
    n_p = models.CharField('n_p', max_length=150)
    street = models.CharField('street', null=True, max_length=150)
    house = models.CharField('house', null=True, max_length=150)
    dor = models.CharField('dor', max_length=150, null=True)
    factor = models.CharField('factor', max_length=150)
    s_pog = models.CharField('s_pog', max_length=150)
    s_pch = models.CharField('s_pch', max_length=150)
    osv = models.CharField('osv', max_length=150)
    latitude = models.FloatField('latitude')
    longitude = models.FloatField('longitude')
    OBJ_DTP = models.CharField('OBJ_DTP', max_length=150)
    change_org_motion = models.CharField('change_org_motion', max_length=150)
    time_group = models.IntegerField('time_group', default=0)

    objects = DataFrameManager()

    def __iter__(self):
        global COUNTER
        yield from {
            "type": "Feature",
            "id": COUNTER,
            "geometry": {
                "type": "Point",
                "coordinates": [self.latitude, self.longitude]
            }
        }.items()
        COUNTER += 1