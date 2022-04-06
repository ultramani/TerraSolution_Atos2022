import requests

def parse_obj(obj):
    for key in obj:
        if isinstance(obj[key], str):
            obj[key] = obj[key].encode('latin_1').decode('utf-8')
        elif isinstance(obj[key], list):
            obj[key] = list(map(lambda x: x if type(x) != str else x.encode('latin_1').decode('utf-8'), obj[key]))
        pass
    return obj

def getRectangle(geoJson):
    coords = geoJson['geometry']['coordinates'][0]
    long = [item[0] for item in coords]
    lat = [item[1] for item in coords]
    maxLong = max(long)
    maxLat = max(lat)
    minLong = min(long)
    minLat = min(lat)
    return coords

def getSolarData(lat, lon):
    # URL = ("https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=T2M,PS,WS10M&community=AG&longitude=%s&latitude=%s&format=CSV&start=2010&end=2020" %(lat,lon))
    URL = ("https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=T2M,PS,WS10M&community=AG&longitude=%s&latitude=%s&format=JSON" %(lat,lon))
    r = requests.get(URL)
    data = r.json()
    return data
