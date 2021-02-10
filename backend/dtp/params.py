from .models import Dtp


LIGHT = []
WEATHER = []
NEARBY = []
ROAD_CONDITIONS = []
CATEGORIES = []
REGIONS = []

Dtps = Dtp.objects.all()
for dtp in Dtps:
    try:
        LIGHT.append(dtp.light)
        WEATHER.extend(dtp.weather)
        NEARBY.extend(dtp.nearby)
        ROAD_CONDITIONS.extend(dtp.road_conditions)
        REGIONS.append(dtp.region)
        CATEGORIES.append(dtp.category)
    except Exception:
        pass

    LIGHT = list(set(LIGHT))
    WEATHER = list(set(WEATHER))
    NEARBY = list(set(NEARBY))
    ROAD_CONDITIONS = list(set(ROAD_CONDITIONS))
    REGIONS = list(set(REGIONS))
    CATEGORIES = list(set(CATEGORIES))