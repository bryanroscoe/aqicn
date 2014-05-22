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
from math import ceil

directory= "./"

#Function to make sure a directory exists
def ensureDir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def getTime(utime, long):
    cityTime = time.strptime(utime, "%A %H:%M")
    
    curDateTime = datetime.datetime.utcnow()

    curDateTime += datetime.timedelta(hours=ceil(float(long)/15))
    cityDateTime = curDateTime.replace(hour=cityTime.tm_hour, minute=cityTime.tm_min)
    diffDays = curDateTime.weekday() -cityTime.tm_wday
    
    
    if diffDays > 0:
        cityDateTime += datetime.timedelta(days=-diffDays)
    elif diffDays < 0:
        cityDateTime += datetime.timedelta(days=diffDays)
    return cityDateTime
    
#First we must get the main map page
print("Getting the main page")
fullMap = urllib.request.urlopen("http://aqicn.org/map/world/")
fullMap = fullMap.read().decode("utf-8")

#Find the json embedded in the main page
print("Finding the json")
fullMapJsonString = re.search("(?<=mapInitWithData\()\[.*\](?=\))", fullMap)

#Parse the json
cities = None
if fullMapJsonString:
    cities = json.loads(fullMapJsonString.group(0))

#Loop through the cities and load each one
print("There are" ,len(cities) , "cities")
cityPopupUrls = []
for i, city in enumerate(cities):
    
    city['dateTime'] = getTime(city['utime'], str(city['g'][1]))

    ##Remove this line to scrape all cities
    if (i+1)%500 !=0:
        continue
    
    print("Scraping "+ city["city"] , i+1, "of",len(cities), city["g"])
    #Get the details url from the 
    city["popupURL"]=("http://aqicn.info/json/mapinfo/@" + str(city["x"]))
    cityDetailPage= urllib.request.urlopen(city["popupURL"]).read().decode("utf-8")
    city["detailURL"] = re.search("http://aqicn\.info/[^\']*", cityDetailPage)
    
    if city["detailURL"]:
        #Load the detail page and get the redirect page
        city["detailURL"] = city["detailURL"].group(0).replace("info", "org", 1)
        
        headers = {
                'User-agent': 'Mozilla/5.0'
        }
        
        page = requests.get(city["detailURL"],allow_redirects=False, headers=headers)
        
        #Attempt to get the redirect page. If that fails we will assume the page the did not redirect and scrapte the url
        if page.headers.get('location'):
            page = requests.get(page.headers.get('location') + "m",allow_redirects=True, headers=headers)
        else:
            soup = BeautifulSoup(page.text)
            titleLink = soup.find(id="aqiwgttitle1")
            if titleLink:
                page = requests.get(titleLink['href'] + "m",allow_redirects=True, headers=headers)
        
        soup = BeautifulSoup(page.text)
        city["data"] = {}
        curList = soup.find_all("td", {"id" : re.compile('^cur_')})
        #Go on to the next city if we don't find anything
        if not curList:
            print("Nothing found for", city['city'])
            continue
        #Loop through all the variables for this city
        savedVars = ""
        for cur in curList:
            curId = cur['id']
            curIdStripped = curId[4:]
            savedVars += curIdStripped + ","
            curDiv = cur.find('div')
            if not curDiv:
                continue
            city['data'][curId] = curDiv.contents[0]
            curFilename = directory + '/' +'Data/AQICN/' + str(curIdStripped) + "/"
            curFilename += city['dateTime'].strftime("%Y/%m/%d/")
            curFilename += city['dateTime'].strftime("%Y%m%d")
            curFilename += str(curIdStripped) + ".csv"
            ensureDir(curFilename)
            f = open(curFilename, 'a')
            f.write(city['dateTime'].strftime("%Y%m%d%H%M") + ",")
            f.write(str(city['g'][0]) + ",")
            f.write(str(city['g'][1]) + ",")
            f.write(str(city['data'][curId]) + "\n")
            f.close()
        print("Saved", savedVars, "for city", city['city'])
            
            

    else:
        print('Not found')
        


