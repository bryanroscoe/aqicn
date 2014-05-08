#!/usr/bin/python

import json
import urllib.request
import re
from builtins import len
import requests
from bs4 import BeautifulSoup


print("Getting the main page")
fullMap = urllib.request.urlopen("http://aqicn.org/map/world/")

fullMap = fullMap.read().decode("utf-8")

print("Finding the url")
fullMapJsonString = re.search("(?<=mapInitWithData\()\[.*\](?=\))", fullMap)

#print(fullMapJsonString.group(0))
cities = None
if fullMapJsonString:
    cities = json.loads(fullMapJsonString.group(0))
    
print("There are" ,len(cities) , "cities")
print("Populating the city URLS")
cityPopupUrls = []
for i, city in enumerate(cities):
    print("Scraping "+ city["city"] , i+1, "of",len(cities), city["g"])
    city["popupURL"]=("http://aqicn.info/json/mapinfo/@" + str(city["x"]))
    cityDetailPage= urllib.request.urlopen(city["popupURL"]).read().decode("utf-8")
    city["detailURL"] = re.search("http://aqicn\.info/[^\']*", cityDetailPage)
    
    if city["detailURL"]:
        city["detailURL"] = city["detailURL"].group(0).replace("info", "org", 1)
        #print("Found", city["detailURL"])
        
        headers = {
                'User-agent': 'Mozilla/5.0'
        }
        
        page = requests.get(city["detailURL"],allow_redirects=False, headers=headers)
        page = requests.get(page.headers.get('location') + "m",allow_redirects=True, headers=headers)
        #print("Pages",page.history, page.url, page.status_code, page.headers.get('location'))
        
        soup = BeautifulSoup(page.text)
        city["data"] = {}
        city["data"]["pm25"] = soup.find("td", {"id" : "cur_pm25"}).find("div").contents[0]
        print("pm25" ,city["data"]["pm25"])
        city["data"]["pm10"] = soup.find("td", {"id" : "cur_pm10"}).find("div").contents[0]
        print("pm10" ,city["data"]["pm10"])

    else:
        print('Not found')

