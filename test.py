from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import requests 
from bs4 import BeautifulSoup
#from selenium import webdriver
import time
import xlsxwriter

from .tasks import get_data 

# Create your views here.
def index(request):
    return render(request, "core/index.htm")

def process_data(request):
    if request.method == "POST":
        f = request.FILES.get("file")
        bill = request.POST.get("bill")
        d_type = request.POST.get("type")
        xls = pd.ExcelFile(f)
        df1 = pd.read_excel(xls)
        end = df1.index
        get_data.delay(bill, d_type, end ,df1)
        return JsonResponse({
            "data": "working"
        })