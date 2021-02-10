import json

from loguru import logger

from .models import Dtp


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
    Dtp.objects.bulk_create(dtps)