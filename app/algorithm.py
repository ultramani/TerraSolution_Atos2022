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
    # URL = ("https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py?&request=execute&tempAverage=CLIMATOLOGY&identifier=SinglePoint&parameters=SI_EF_TILTED_SURFACE&userCommunity=SB&lon=%s&lat=%s&outputList=CSV&user=DOCUMENTATION" %(longitud,latitud))
    URL = ("https://power.larc.nasa.gov/api/temporal/climatology/regional?latitude-min=50&latitude-max=55&longitude-min=50&longitude-max=55&parameters=T2M&community=SB&format=JSON&start=2010&end=2020")
    r = requests.get(URL)
    data = r.json()
    # with open('data.json','w') as json_file:
    #     json.dump(data,json_file)
    #csv = data['outputs']['csv'] #url del csv
    #wget.download(csv, './prueba.csv') # para descargar el csv
    # parameters = data['features'][0]['properties']['parameter'] #valores medios mensual y anual por parametro
    # parametersInfo = data['parameterInformation'] #nombre completo y unidades de parametros
    # for para in parameters:
    #     parameters[para].insert(0,parametersInfo[para]['longname'] + "("+ parametersInfo[para]['units'] + ')')
    # aux = []
    # for para in parameters:
    #     aux.append(parameters[para])
    return data