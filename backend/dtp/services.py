import json

from django.db.models import Q

from loguru import logger

from .models import Dtp
from .serializers import DtpDetailSerializer


@logger.catch
def get_dtps_by_ids(ids: list):
    q = Q()
    for i in ids:
        q |= Q(pk=i)
    return Dtp.objects.filter(q)


@logger.catch
def fill_db_from_json(file):
    data = json.load(file)['features']
    data = list(filter(lambda x: x['properties']['point']['lat'], data))
    dtps = []
    for i in data:
        dtp = i['properties']
        dtps.append(Dtp(
            datetime=dtp['datetime'], parent_region=dtp['parent_region'], region = dtp['region'],
            address=dtp['address'], lat=dtp['point']['lat'], long=dtp['point']['long'],
            category=dtp['category'], deaths =dtp['dead_count'], injured=dtp['injured_count'],
            light=dtp['light'], weather=dtp['weather'], nearby=dtp['nearby'],
            road_conditions=dtp['road_conditions']))
        logger.info(f'{dtps[-1]} - Created!')
    Dtp.objects.bulk_create(dtps)

def construct_data(params) -> list:
    params = list(params)
    new_params = []
    for claster in params:
        claster = dict(claster)
        detail_point =  DtpDetailSerializer(get_dtps_by_ids(claster.pop('points')), many=True).data
        claster['points'] = [dict(i) for i in detail_point]
        new_params.append(claster)
    return new_params

def get_model_fields() -> list:
    return [i.name for i in Dtp._meta.fields][1:] + ['claster', 'claster_lat', 'claster_long']