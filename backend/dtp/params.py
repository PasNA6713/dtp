from .models import Dtp


LIGHT = []
WEATHER = []
NEARBY = []
ROAD_CONDITIONS = []
CATEGORY = []
REGION = []

try:
    Dtps = Dtp.objects.all()
    for dtp in Dtps:
        LIGHT.append(dtp.light)
        WEATHER.extend(dtp.weather)
        NEARBY.extend(dtp.nearby)
        ROAD_CONDITIONS.extend(dtp.road_conditions)
        REGION.append(dtp.region)
        CATEGORY.append(dtp.category)

        LIGHT = list(set(LIGHT))
        WEATHER = list(set(WEATHER))
        NEARBY = list(set(NEARBY))
        ROAD_CONDITIONS = list(set(ROAD_CONDITIONS))
        REGION = list(set(REGION))
        CATEGORY = list(set(CATEGORY))
except Exception:
    pass

    