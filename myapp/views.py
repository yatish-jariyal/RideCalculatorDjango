import json
from django.shortcuts import render
# Create your views here.
from bs4 import BeautifulSoup
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from .models import FuelPrices
from django.http import HttpResponse
import requests
from django.core import serializers

@never_cache
@csrf_exempt
def updateCurrentFuelPrices(request):

    req = request.POST
    city = req["city"]
    price = float(req["price"])
    type = req["fuel_type"]

    if type == "Petrol":
        fuel_type = 1
    elif type == "Diesel":
        fuel_type = 2
    else:
        fuel_type = 3

    if FuelPrices.objects.filter(city=city, fuel_type = fuel_type).exists():
        #update
        FuelPrices.objects.filter(city=city, fuel_type=fuel_type).update(price=price)
    else:
        fp = FuelPrices(city=city, price=price, fuel_type=fuel_type)
        fp.save()

    response = dict()
    response['data'] = 'ok'
    return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
@never_cache
def fetchFuelPrice(request):
    req = request.POST
    city = req['city']
    fuel_type = req['fuel_type']

    print("fueltype = ",fuel_type)
    if fuel_type == 'Petrol':
        type = 1
    elif fuel_type == 'Diesel':
        type = 2
    elif fuel_type == "CNG":
        type = 3

    query_set = FuelPrices.objects.filter(city=city, fuel_type=type)
    json_data = serializers.serialize('json',query_set)
    data = json.loads(json_data)

    print('data = ',data)
    data = data[0]
    mydata = dict()
    mydata['id'] = data['pk']
    fields = data['fields']
    mydata['city'] = fields['city']
    mydata['price'] = fields['price']
    fuel_type = fields['fuel_type']
    if fuel_type == 1:
        mydata['fuel_type'] = 'Petrol'
    elif fuel_type == 2:
        mydata['fuel_type'] = 'Diesel'
    else:
        mydata['fuel_type'] = 'CNG'

    return HttpResponse(json.dumps(mydata), content_type='application/json')







