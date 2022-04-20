from .databaseManager import db
import requests
from app.models import report
from math import sin, cos, sqrt, atan2, radians

def parse_obj(obj):
    for key in obj:
        if isinstance(obj[key], str):
            obj[key] = obj[key].encode('latin_1').decode('utf-8')
        elif isinstance(obj[key], list):
            obj[key] = list(map(lambda x: x if type(x) != str else x.encode('latin_1').decode('utf-8'), obj[key]))
        pass
    return obj

def sides(bbox):
    p1, p2, p3 = bbox[0], bbox[1], [bbox[1][0], bbox[0][1]]
    return [lineLen(p3,p1),lineLen(p3,p2)]

def lineLen(p1, p2):
    R = 6373.0

    lat1, lon1, lat2, lon2 = radians(p1[0]), radians(p1[1]), radians(p2[0]), radians(p2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def getRectangle(geoJson):
    coords = geoJson['geometry']['coordinates'][0]
    long = [item[0] for item in coords]
    lat = [item[1] for item in coords]
    maxLong, maxLat, minLong, minLat = max(long), max(lat),min(long), min(lat)
    bbox = [[minLong,minLat],[maxLong,maxLat]]
    geoJson['bbox'] = bbox
    geoJson['sides'] = sides(bbox)
    return geoJson

def getSolarData(lat, lon, params):
    paraStr = ""
    for para in params:
        paraStr += str(para) + ","
    URL = ("https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=%s&community=AG&longitude=%s&latitude=%s&format=JSON" %(paraStr[:-1],lat,lon))
    r = requests.get(URL)
    data = r.json()
    parsed_data = {}
    for para in data['parameters']:
        parsed_data[para]={
            'longname': data['parameters'][para]['longname'],
            'units': data['parameters'][para]['units'],
            'values' : list(data['properties']['parameter'][para].values())[0:13]
            }
    return parsed_data

def save(gData, pData):
    location = gData['data'][0:2]
    data = report((location,))
    name = gData['data'][2]
    if name != -1:
        data.name = name
    bbox = gData['bbox']
    sides = gData['sides']
    data.bbox = ((bbox,))
    data.sides= ((sides,))
    data.polygon = (gData['geometry']['coordinates'][0],)
    data.area = gData['area']
    data.params = pData
    # Create object with values
    data.insert()
    message = f"The data for report {location} and {bbox} has been submitted."
    return message

def prueba():
    reports = report.query.all()
    test = reports[-1].getJson()
    params = test['params']
    print(test)
    print(params)
    for e in params:
        # print(e)
        print("longname = {}, units = {}, values = {}".format(params[e]['longname'],params[e]['units'],params[e]['values']))
    pass