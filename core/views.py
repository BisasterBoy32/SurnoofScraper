from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import requests 
from bs4 import BeautifulSoup
#from selenium import webdriver
import time
import xlsxwriter
from webScraper.settings import pusher_client

from .tasks import get_data 

# Create your views here.
def index(request):
    return render(request, "core/index.htm")

def process_data(request):
    if request.method == "POST":
        f = request.FILES.get("file")
        bill = request.POST.get("bill")
        d_type = request.POST.get("type")
        data = []
        xls = pd.ExcelFile(f)
        df1 = pd.read_excel(xls)
        end = df1.index.stop
        urls = []
        for index in range(0 , int(end)):
            try:
                lat = df1.iloc[index]["lat"]
                lon = df1.iloc[index]["long"]
                f = d_type
                url = f"https://www.google.com/get/sunroof/building/{lat}/{lon}/#?f={f}&b={bill}"
                urls.append(url)

            except Exception as e:
                print(e)
                print("This URL doesn't conain any data")

        pusher_client.trigger('webScraper', 'scrape-finished', {'message': "before running celery ^^"})
        item = get_data.delay(urls, end ,bill,d_type )
        return JsonResponse({
            "data": data
        })