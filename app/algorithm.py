from datetime import datetime
from flask import make_response, render_template
from flask_login import current_user
import requests
# import pdfkit
import requests
from app.models import crop, report
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

# Pdf generator not adapted to UNIX

# def generatePDF(id):
#     reportobject = report.selectreportbyid(id)
#     rendered = render_template('pdfGenerator.html',report=reportobject)
#     path = r'.\executables\pdf\wkhtmltopdf\bin\wkhtmltopdf.exe'
#     config = pdfkit.configuration(wkhtmltopdf=path)
#     pdf = pdfkit.from_string(rendered,False,configuration=config)
    
#     response = make_response(pdf)
#     response.headers['Content-Type'] = 'application/pdf'
#     response.headers['Content-Disposition'] = 'inline; filename=report.pdf'
    
#     return response

# Report generation

def save(gData, pData):
    location = gData['data'][0:2]
    data = report(location,current_user)
    name = gData['data'][2]
    if name != -1:
        data.name = name
    bbox = gData['bbox']
    sides = gData['sides']
    data.bbox = bbox
    data.sides= sides
    data.polygon = (gData['geometry']['coordinates'][0],)
    data.area = round(gData['area'])
    data.params = pData
    #Process the data from nasa
    month = int(datetime.now().strftime("%m"))

    avgtempmonths = getavg(pData['T2M'],month)
    avghumiditymonth = getavg(pData['RH2M'],month)
    avgrainfallmonth =  getavg(pData['PRECTOTCORR'],month)
    avgsoiltempmonth  =  getavg(pData['TS'],month)
    avgsoilmoistmonth   =  getavg(pData['GWETPROF'],month)
    avgwindmonth  =  getavg(pData['WS2M'],month) 
    scores = []
    badges = []
    wns= []
    watercost = []
    profit = []
    periods = []
    for plant in range(1,8):
        monthstogrow = crop.growthrange(plant) 
        sumscores = 0
        badgec = []
        #Calculate data score and badge
        badge,score = analysisA(plant,avgtempmonths,monthstogrow,'T2M')
        sumscores += score
        badgec.append(badge)
        badge,score = analysisA(plant, avghumiditymonth,monthstogrow,'RH2M')
        sumscores += score
        badgec.append(badge)
        badge,score,waterneeded = analysisB(plant, avgrainfallmonth,monthstogrow,data.area)
        sumscores += score
        badgec.append(badge)
        badge,score = analysisA(plant, avgsoiltempmonth,monthstogrow,'TS')
        sumscores += score
        badgec.append(badge)
        badge,score = analysisA(plant, avgsoilmoistmonth,monthstogrow,'GWETPROF')
        sumscores += score
        badgec.append(badge)
        badge,score = analysisC(plant, avgwindmonth,monthstogrow,'WS2M')
        sumscores += score
        badgec.append(badge)        
        
        scores.append(sumscores)    
        badges.append(badgec)
        wns.append(waterneeded)
        
    plantnames = crop.getNames() 
    print(scores)
    
    #Profit calculation section
    watercost = calcwc(wns)
    yieldpresqm = crop.getallyields()
    priceperkg = crop.getallprices()
    profit = calcprof(watercost,round(data.area),yieldpresqm,priceperkg)
    periods= crop.getalllifeperiods()
    
    #Select the best crops for the area selected
    scores, badges, plantnames,profit,watercost,wns,periods = selector(scores, badges,plantnames,profit,watercost,wns,periods)

    #Add all the data to the report
    data.avgMonthlyTemperaturePlants = avgtempmonths
    data.avgMonthlyPrecipitationPlants = avgrainfallmonth
    data.avgMonthlyHumidityPlants = avghumiditymonth
    data.avgMonthlySoilmoisturePlants = avgsoilmoistmonth
    data.avgMonthlySoiltemperaturePlants = avgsoiltempmonth
    data.avgMonthlyWindVelocityPlants = avgwindmonth
    data.watercost = watercost
    data.waterneeded = wns
    data.priceperkg = priceperkg
    data.benefit = profit
    data.plantsScores = scores
    data.plantsBadges = badges  
    data.plantsNames = plantnames
    data.plantsLifePeriod = periods
    data.numberOfPlants = len(plantnames)
    
    
    # Create object with values
    ids = data.insert()
    return ids

def calcprof(watercost,area,yieldpresqm,priceperkg):
    profs = []
    for i in range(len(watercost)):
        total = area * yieldpresqm[i] * priceperkg[i]
        total -= watercost[i]
        if total < 0:
            total == 0
        profs.append(round(total * 0.8))
    return profs

def calcwc(wns):
    costs = []
    for item in wns:
       costs.append(item * 0.64) 
    return costs

    
def selector(scores, badges,plantnames,profit,watercost,wns,periods):
    aux = scores.copy()
    aux1 = badges.copy()
    aux2 = plantnames.copy()
    aux3 = profit.copy()
    aux4 = watercost.copy()
    aux5 = wns.copy()
    aux6 = periods.copy()
    print(aux)
    for score in scores:
        if score < 35:
            index = aux.index(score)
            del aux [index]
            del aux1 [index]
            del aux2 [index]
            del aux3 [index]
            del aux4 [index]
            del aux5 [index]
            del aux6 [index]
    return aux, aux1,aux2,aux3,aux4,aux5,aux6
            
def getavg(data,month):
    avgmonths= []
    for j in range(2,7):
        auxavg = 0
        for i in range(j):
            auxavg += data['values'][i + month]
        auxavg = round(auxavg / j, 2)
        avgmonths.append(auxavg)
    return avgmonths

def analysisA(id,avgmonths,monthstogrow,param):
    
    rangex = crop.getrange(id  ,param)
    aux = avgmonths[monthstogrow - 2] 
    #For further versions the score will be calculated more precisly
    if (rangex[0] <= aux < rangex[1]) or (rangex[3] < aux <= rangex[4]):
        return ['Almost ideal',''],5
    elif rangex[1] <= aux <= rangex[3]:
        return ['Ideal',''],10
    else:
        if  aux < rangex[0]: 
            return ['Not ideal','low'] ,-3    
        else:   
            return ['Not ideal','high'] ,-3


def analysisB(id,avgmonths,monthstogrow,area):
    water_data = crop.getwaterneed(id)
    aux = avgmonths[monthstogrow - 2]
    #The total water needed for all the area in a span of time of a week
    water_needed_period = water_data[0] * area
    water_obtained_rainfall =  aux * 7
    water_add_needed = water_needed_period - water_obtained_rainfall
    if (water_needed_period * 0.75) >= water_add_needed >= 0:
        return ['Very ideal',''],  6 , water_add_needed
    elif (water_needed_period * 0.75) <= water_add_needed:
        return ['Almost ideal',''], 3 , water_add_needed
    elif -28 <= water_add_needed < 0:
        return ['Ideal',''], 10, 0
    elif  water_add_needed < -28:
        return ['Not ideal',''], 0 , water_add_needed
    
def analysisC(id,avgmonths,monthstogrow,param):
    
    rangex = crop.getrange(id  ,param)
    aux = avgmonths[monthstogrow - 2] 
    #For further versions the score will be calculated more precisly
    if (rangex[1] <= aux < rangex[4] - 5):
        return ['Almost ideal',''],5
    elif rangex[0] <= aux <= rangex[1]:
        return ['ideal',''],10
    else:
        if  aux < rangex[0]: 
            return ['Not ideal','low'] ,0    
        else:   
            return ['Not ideal','high'] , -5


# def prueba():
#     reports = report.query.all()
#     test = reports[-1].getJson()
#     params = test['params']
#     print(test)
#     print(params)
#     for e in params:
#         # print(e)
#         print("longname = {}, units = {}, values = {}".format(params[e]['longname'],params[e]['units'],params[e]['values']))
#     pass
