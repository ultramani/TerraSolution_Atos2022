<<<<<<< HEAD

import requests, json, urllib.parse
import urllib.request as ur
from xml.dom import minidom 
from datetime import datetime, timezone, date, timedelta
from io import BytesIO
from PIL import Image
import ssl # quitar esto en produccion
=======
from turtle import pd
from flask import make_response, render_template
from flask_login import current_user
import requests, json
import pdfkit
>>>>>>> master
from .databaseManager import db
from app.models import report, mundiImg
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

<<<<<<< HEAD
# SENTINEL 2 #
# Algoritmo para seleccionar la fecha más reciente con el menor porcentaje de nubes 
# para una determinada zona.
# FALTA VER COMO OBTENER LAS COORDENADAS PARA ESTA FUNCION

#Parsea las coordenadas para formato URL
def parse_bbox(bbox):
  return str(bbox[0][0]) + ',' + str(bbox[0][1]) + ',' + str(bbox[1][0]) + ',' + str(bbox[1][1])

#Resta fechas con el formato adecuado
def subtract_date(main_date,days_difference=5):
  timeSubtract = main_date - timedelta(days=days_difference) # Resta la diferencia de días
  timeStart = timeSubtract.strftime("%Y-%m-%dT%H:%M:%SZ")
  return timeStart

#Abre la URL 
def open_url(coordinates, timeStart, timeEnd, cloudCover): # devuelve la url parseada en xml
  url = 'https://mundiwebservices.com/acdc/catalog/proxy/search/Sentinel2/opensearch?bbox=' + coordinates + '&timeStart=' + timeStart +'&timeEnd=' + timeEnd + '&cloudCover=[0,' + cloudCover + ']'
  try:
    f = ur.urlopen(url, context=ssl._create_unverified_context()) # Quitar context ssl en producción 
    s = f.read().decode()
    f.close()
  except Exception as e:
    print(e)
    s = '<error></error>'
  s = minidom.parseString(s)
  return s

#Comprueba que haya imágenes para el intervalo de fechas indicados en la url
def check_for_entries(doc): 
  entries = doc.getElementsByTagName('entry')
  if entries.length > 0:
    return True
  else:
    return False

#Comprueba que existan imágenes para los parámetros que se quieren encontrar; por ej. CloudCover
def parameters_exist(coordinates,timeStart,timeEnd,cloudCover=['25','50','75']):
  selected_cloudCover = '100'
  for coverage in cloudCover:
    doc = open_url(coordinates,timeStart,timeEnd,coverage)
    isentry = check_for_entries(doc)
    if isentry is True:
      selected_cloudCover = coverage
      break
  return isentry, coverage

#Selecciona la fecha más reciente de un intervalor de fechas especificado
def select_recent_date(coordenadas,timeStart,timeEnd,cloudCover):
  doc = open_url(coordenadas,timeStart,timeEnd,cloudCover)
  tagname = doc.getElementsByTagName('entry')
  dates = []
  for tag in tagname:
    cloud_coverage = tag.getElementsByTagName('eo:cloudCover')[0].firstChild.data
    date = tag.getElementsByTagName('dc:date')[0].firstChild.data
    if cloud_coverage < cloudCover:
      dates.append(date)
  return max(dates)

#Genera la url necesaria para obtener la imagen del Index Vegetation adecuada
def url_mundiLayer_Date(bbox, days_difference=5):
  hasFoundDate = False
  coordinates = bbox
  date_gap = 5
  time_now = datetime.now() # Día actual
  timeEnd = time_now.strftime("%Y-%m-%dT%H:%M:%SZ") # Coge el día actual con el formato que se necesita para la petición
  timeStart = subtract_date(time_now, days_difference) # Inicio del intervalo de fechas 
  while hasFoundDate is False and days_difference < 90: # Como mucho tres meses atrás de búsqueda
    hasFoundDate, cloudCover = parameters_exist(coordinates, timeStart, timeEnd)
    days_difference += date_gap #Aumenta la diferencia de dias
    timeStart = subtract_date(time_now, days_difference)  
  recent_date = select_recent_date(coordinates, timeStart, timeEnd, cloudCover)
  return recent_date

#Obtiene los colores y las veces que se repite en formato hexadecimal
def img_analyzer(img, maxcolors=256):
  colors = img.getcolors(maxcolors)
  count = []
  pixelColorHex = []
  for color in colors:
    count.append(color[0])
    pixelColorHex.append('#{:02x}{:02x}{:02x}'.format(color[1][0],color[1][1],color[1][2]))
  return count, pixelColorHex

#Transforma la información necesaria para analizar la imagen en JSON, para que se pueda trabajar desde el frontend
def img_to_dict(count,color,url):
  json_dict = {
      "img_url" : url,
      "img_color_count" : count,
      "img_color" : color
  }
  return json_dict

#Funcion devuelve un json con las capas especificadas en la variable layers y sus url, colores y  conteo
def layers(bbox, best_recent_date, width, height):
  layers = ['5_VEGETATION_INDEX', '6_MOISTURE_INDEX'] # Añadir aquí las capas
  mundiLayers_dict = {}
  maxcolors = height * width
  for layer in layers:
    url = 'http://shservices.mundiwebservices.com/ogc/wms/d275ef59-3f26-4466-9a60-ff837e572144?SERVICE=WMS&REQUEST=GetMap&TRANSPARENT=true&LAYERS=' + layer + '&VERSION=1.1.1&FORMAT=image%2Fpng&STYLES=&showLogo=false&time='+ best_recent_date +'&SRS=EPSG%3A4326&WIDTH='+ str(width) +'&HEIGHT=' + str(height) + '&BBOX=' + bbox
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img_color_count, img_color = img_analyzer(img, maxcolors)
    img_dict = img_to_dict(img_color_count,img_color,url)
    mundiLayers_dict[layer] = img_dict # Añade la capa al diccionario
  return mundiLayers_dict

#Coordina la selección de la mejor imagen para el análisis, y retorna dicho análisis en formato JSON
#Devuelve la url de la image y los colores y cuanto se repiten en listas diferentes.
def mundiLayer(bbox, width=682, height=373):
  bbox = parse_bbox(bbox)
  best_recent_date = url_mundiLayer_Date(bbox)
  best_recent_date = urllib.parse.quote(str(best_recent_date),safe="")
  bbox = urllib.parse.quote(str(bbox),safe="")
  mundiLayers_json = layers(bbox, best_recent_date, width, height)
  return mundiLayers_json

def saveMundi(gData):
  bbox = gData['bbox']
  sides = gData['sides']
  width = int(sides[0] * 1000) # To meters
  height = int(sides[1] * 1000) # To meters
  mundiInfo = mundiLayer(bbox,width,height)
  report_id, = report.query.with_entities(report.id).order_by(report.id.desc()).first() # Gets the last Report ID generated
  print(report_id)
  for layer in mundiInfo:
    layer_dict = mundiInfo[layer]
    mundi = mundiImg()
    mundi.report_id = report_id 
    mundi.layerName = layer
    mundi.url = layer_dict['img_url']
    mundi.colorCount = ((layer_dict['img_color_count'],))
    mundi.pixelColor = ((layer_dict['img_color'],))
    mundi.insert()
  print("Mundi values added correctly")
  
=======
# Pdf generator

def generatePDF():
    reportobject = report.selectfirst()
    rendered = render_template('pdfGenerator.html',report=reportobject)
    path = r'C:\Users\ultra\Desktop\pdf\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path)
    pdf = pdfkit.from_string(rendered,False,configuration=config)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=report.pdf'
    
    return response

>>>>>>> master
def save(gData, pData):
    location = gData['data'][0:2]
    data = report((location,),current_user)
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


# Las funciones agrupan colores para obtener el estado de la vegetacion en funcion de la imagen: 
# https://images.ctfassets.net/qfhr9fiom9gi/7JaDAufyzx0KwgnduSNFWX/c9d251df8e13516c57ca85ec71ee2288/image4.jpg
def pruebaJoinColors(test):
  """legend = {
    '#000000': -1.0,
    '#ff0000': -0.2,
    '#9a0000': -0.1,
    '#660000': 0.0,
    '#ffff33': 0.1,
    '#cccc33': 0.2,
    '#666600': 0.3,
    '#33ffff': 0.4,
    '#33cccc': 0.5,
    '#006666': 0.6,
    '#33ff33': 0.7,
    '#33cc33': 0.8,
    '#006600': 0.9 }"""

  color_groups = ['Dead Vegetation','Unhealthy Vegetation','Moderately Healthy Vegetation', 'Very Healthy Vegetation', 'Unknown status']
  color_count_groups = [0,0,0,0,0]
  for i in range(len(test["pixelColor"])):
    color = test["pixelColor"][i]
    if color in ['#000000','#ff0000','#9a0000','#660000']: #Estos valores se sacan de la leyenda
      color_count_groups[0] += test["colorCount"][i]
    elif color in ['#ffff33','#cccc33','#666600']:
      color_count_groups[1] += test["colorCount"][i]
    elif color in ['#33ffff','#33cccc','#006666']:
      color_count_groups[2] += test["colorCount"][i]
    elif color in ['#33ff33','#33cc33','#006600']:
      color_count_groups[3] += test["colorCount"][i]
    else:
      color_count_groups[4] += test["colorCount"][i]
  return {
    'url' : test["url"],
    'colorCount': color_groups,
    'pixelColor': color_count_groups
  }


def pruebaMundi():
  mundi = mundiImg.query.all()
  test = mundi[-2].getJson()
  a = pruebaJoinColors(test)
  return a
