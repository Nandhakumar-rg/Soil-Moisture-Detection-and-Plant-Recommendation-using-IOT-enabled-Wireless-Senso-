from django.http import HttpResponse
from django.shortcuts import render
import requests
import time
import json
import csv
import os




url = "https://api.thingspeak.com/channels/2103758/feeds/last.json?api_key=BHC451OAU8L5XJ4H"

def home(request):
    msg = ""
    best_plants = []
    filename = open(os.path.dirname(os.path.realpath(__file__)) + '\Crop_recommendation.csv', "r")
    file = csv.DictReader(filename)

    n = []
    p = []
    k = []
    npk = []
    crops = []

    for col in file:
        n.append(int(col['N']))
        p.append(int(col['P']))
        k.append(int(col['K']))
        crops.append(col['label'])

    for i in range(0, len(k)) :
        npk.append((n[i] + p[i] + k[i]) / 3) 

    response = requests.get(url)
    data = json.loads(response.text)
    # data['field1'] = 12
    msg = 'Sensor value readed at '+data['created_at']+' .'
    i = 0
    h = 5
    if float((data['field1']) == 0):
         best_plants.append("All Leguminous Plants")
    for each in npk :
        if float(data['field1']) > each - 5 and float(data['field1']) < each + 5 :
            if crops[i] not in best_plants :
                best_plants.append(crops[i])
        i = i + 1
    return render(request, 'index.html', {
        'npk' : data['field1'],
        'water' : data['field2'],
        'msg': msg,
        "plant" : best_plants
    })

