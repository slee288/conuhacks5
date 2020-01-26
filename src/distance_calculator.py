from math import sin, cos, sqrt, atan2, radians


def get_distance(a1, o1, a2, o2):
    R = 6373.0 # approximate radius of earth in km

    lat1 = radians(a1)
    lon1 = radians(o1)
    lat2 = radians(a2)
    lon2 = radians(o2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c