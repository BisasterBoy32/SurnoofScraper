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
    i = 1
    data = []
    for index in range(0 , end):
        try:
            url = urls[index]["url"]
            lat = urls[index]["lat"]
            lon = urls[index]["lon"]
            item = scrape_data(url, bill, d_type ,lat , lon)
            if item:
                data.append(item)
                i += 1

        except Exception as e:
            print(e)
            print("This URL doesn't conain any data")
    
    result = {
        "data" : data,
        "message" : "success the pages has been scraped succefully",
        "type" : "success"
    }
    data = json.dumps(result)
    pusher_client.trigger('webScraper', 'scrape-finished', {'message': data})
    return "success"

   