# main/tasks.py
from bs4 import BeautifulSoup
from .celery import app
import requests
from .helpers import  scrape_data
from webScraper.settings import pusher_client
import json 

# celery worker -A core --loglevel=debug

@app.task()
def get_data(urls ,end, bill, d_type):
    print("working on background .....")
    i = 1
    data = []
    for index in range(0 , end):
        try:
            item = scrape_data(urls[index], bill, d_type)
            if item:
                data.append(item)
                i += 1

        except Exception as e:
            print(e)
            print("This URL doesn't conain any data")
    
    result = {
        "data" : data,
        "message" : "success all pages has been scraped succefully",
        "type" : "success"
    }
    data = json.dumps(result)
    pusher_client.trigger('webScraper', 'scrape-finished', {'message': data})
    return "success"

   