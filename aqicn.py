#!/usr/bin/python
#Author:Bryan Roscoe
#https://github.com/bryanroscoe/aqicn
import json
import sys
import re
from builtins import len
import requests
from bs4 import BeautifulSoup
import time
import datetime
import os
from math import ceil
import traceback
import gc
from symbol import except_clause

#
#from memory_profiler import profile

directory= "./"

#Function to make sure a directory exists
def ensureDir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def getTime(utime, long):
    try:
        cityTime = time.strptime(utime, "%A %H:%M")
    except ValueError:
        utime= utime.replace(".", "")
        cityTime = time.strptime(utime, "%a %H:%M")
    
    curDateTime = datetime.datetime.utcnow()

    curDateTime += datetime.timedelta(hours=ceil(float(long)/15))
    cityDateTime = curDateTime.replace(hour=cityTime.tm_hour, minute=cityTime.tm_min)
    diffDays = curDateTime.weekday() -cityTime.tm_wday
    
    if diffDays > 0:
        cityDateTime += datetime.timedelta(days=-diffDays)
    elif diffDays < 0:
        cityDateTime += datetime.timedelta(days=diffDays)
    return cityDateTime

def writeData(name, city):
        shortName = name[4:]
        curFilename = directory + '/' +'Data/AQICN/' + str(shortName) + "/"
        curFilename += city['dateTime'].strftime("%Y/%m/%d/")
        curFilename += city['dateTime'].strftime("%Y%m%d")
        curFilename += str(shortName) + ".csv"
        ensureDir(curFilename)
        f = open(curFilename, 'a')
        if name == "cur_aqi":
            f.write(city['dateTime'].strftime("%Y%m%d%H%M") + ",")
        else:
            f.write(city['dateTimeUpdated'].strftime("%Y%m%d%H%M") + ",")
        f.write(str(city['g'][0]) + ",")
        f.write(str(city['g'][1]) + ",")
        f.write(str(city['data'][name]) + "\n")
        f.close()    
#@profile
def handleCity(i, city, cities):
    try:
        city['dateTime'] = getTime(city['utime'], str(city['g'][1]))
        print("Scraping "+ city["city"] , i+1, "of",len(cities), city["g"], city["x"])
        #Get the details url from the popup
        city["popupURL"]=("http://aqicn.info/json/mapinfo/@" + str(city["x"]))
        cityDetailPage = requests.get(city["popupURL"]).text
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

            newTime = re.search( "(?<=Updated on ).*$",soup.find(text=re.compile("(?<=Updated on ).*?"))).group(0)
            city['dateTimeUpdated'] = getTime(newTime, str(city['g'][1]))
            curList = soup.find_all("td", {"id" : re.compile('^cur_')})
            #Go on to the next city if we don't find anything
            if not curList:
                print("Nothing found for", city['city'])
                return
            #Loop through all the variables for this city
            savedVars = ""
            for cur in curList:
                curId = cur['id']
                savedVars += curId + ","
                curDiv = cur.find('div')
                if not curDiv:
                    continue
                city['data'][curId] = curDiv.contents[0]
                writeData(curId, city)
            
            city['data']['cur_aqi'] = city['aqi'];
            writeData('cur_aqi', city)
            
            print("Saved", savedVars + "aqi", "for city", city['city'])
            del soup
            del city
            del curList
            cities[i] = None
            gc.collect()
                
        
        else:
            print('Not found')
    except KeyboardInterrupt:
        sys.exit()
    except:

        print(city["city"], "encountered an error:", traceback.format_exc() )
            

def getCities():
    #First we must get the main map page
    print("Getting the main page")
    fullMap = requests.get("http://aqicn.org/map/world/").text
    #fullMap = urllib.request.urlopen("http://aqicn.org/map/world/")
    #fullMap = fullMap.read().decode("utf-8")
    
    #Find the json embedded in the main page
    print("Finding the json")
    fullMapJsonString = re.search("(?<=mapInitWithData\()\[.*\](?=\))", fullMap)
    
    #Parse the json
    cities = None
    if fullMapJsonString:
        cities = json.loads(fullMapJsonString.group(0))
    
    #Loop through the cities and load each one
    print("There are" ,len(cities) , "cities")
    for i, city in enumerate(cities):
        #if i%500 != 0:
        #    continue
        handleCity(i, city, cities)
        
if __name__ == '__main__':
    getCities()
    
