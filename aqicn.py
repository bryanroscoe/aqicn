#!/usr/bin/python

import json
import urllib.request
import re
from builtins import len
import requests
from bs4 import BeautifulSoup
import time
import datetime
import os

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

datetime.time
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
    
    cityTime = time.strptime(city['utime'], "%A %H:%M")
    curDateTime = datetime.datetime.utcnow()
    cityDateTime = curDateTime.replace(hour=cityTime.tm_hour, minute=cityTime.tm_min)
    diffDays = curDateTime.weekday() -cityTime.tm_wday
    
    if diffDays == -1 or diffDays == 6:
        cityDateTime += datetime.timedelta(days=1)
    elif diffDays > 0:
        cityDateTime += datetime.timedelta(days=-diffDays)
    elif diffDays < 0:
        cityDateTime += datetime.timedelta(days=diffDays)
    city['dateTime'] = cityDateTime
    
    if (i+1)%750 !=0:
        continue
    print(city)
    print("Scraping "+ city["city"] , i+1, "of",len(cities), city["g"])
    city["popupURL"]=("http://aqicn.info/json/mapinfo/@" + str(city["x"]))
    cityDetailPage= urllib.request.urlopen(city["popupURL"]).read().decode("utf-8")
    city["detailURL"] = re.search("http://aqicn\.info/[^\']*", cityDetailPage)
    
    if city["detailURL"]:
        city["detailURL"] = city["detailURL"].group(0).replace("info", "org", 1)

        
        headers = {
                'User-agent': 'Mozilla/5.0'
        }
        
        page = requests.get(city["detailURL"],allow_redirects=False, headers=headers)

        if page.headers.get('location'):
            page = requests.get(page.headers.get('location') + "m",allow_redirects=True, headers=headers)
        else:
            soup = BeautifulSoup(page.text)
            titleLink = soup.find(id="aqiwgttitle1")
            if titleLink:
                print("titleLink", titleLink['href'])
                page = requests.get(titleLink['href'] + "m",allow_redirects=True, headers=headers)
        
        soup = BeautifulSoup(page.text)
        city["data"] = {}
        curList = soup.find_all("td", {"id" : re.compile('^cur_')})
        
        if not curList:
            continue
        
        for cur in curList:
            curId = cur['id']
            curIdStripped = curId[4:]
            curDiv = cur.find('div')
            if not curDiv:
                continue
            city['data'][curId] = curDiv.contents[0]
            print(curId, city['data'][curId])
            curFilename = 'Data/AQICN/' + str(curIdStripped) + "/"
            curFilename += cityDateTime.strftime("%Y/%m/%d/")
            curFilename += cityDateTime.strftime("%Y%m%d")
            curFilename += str(curIdStripped) + ".csv"
            print(curFilename)
            ensure_dir(curFilename)
            f = open(curFilename, 'a')
            f.write(cityDateTime.strftime("%Y%m%d%H%M") + ",")
            f.write(str(city['g'][0]) + ",")
            f.write(str(city['g'][1]) + ",")
            f.write(str(city['data'][curId]) + "\n")
            f.close()
            
            

    else:
        print('Not found')
        


