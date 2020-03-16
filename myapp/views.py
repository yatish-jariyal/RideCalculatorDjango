from django.shortcuts import render
# Create your views here.
from bs4 import BeautifulSoup
from .models import FuelPrices

import requests

def fetchPetrolPrices():
    URL = 'https://www.bankbazaar.com/fuel/petrol-price-india.html'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find("div", {"class": "gold-rate-table"})
    print(results.prettify())

    data = []
    prices = dict()
    table = soup.find('table', attrs={'class':'table table-curved tabdetails heightcontroltable'})
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        prices[cols[0]] = cols[1]
        data.append([ele for ele in cols if ele]) # Get rid


    print(prices)

    return prices


def updateCurrentFuelPrices():
    #petrol
    prices = fetchPetrolPrices()
    # import these petrol prices in FuelPrices table -> type petrol
    for key in prices.keys():
        cityname = key
        fuelprice = prices[key]

        fp = FuelPrices(city=cityname, price=fuelprice, type='Petrol')
        fp.save()
