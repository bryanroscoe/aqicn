#!/usr/local/bin/python3.4
#Author:Bryan Roscoe
#https://github.com/bryanroscoe/aqicn
import json
import sys
import re
from builtins import len
import requests
from bs4 import BeautifulSoup
import datetime
import os
import traceback
import gc
from dateutil.parser import parse
from dateutil.tz import tzutc

directory= "/home/teamlary/aqicn"

#Function to make sure a directory exists
def ensureDir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def getTime(city):
    long = str(city['g'][1])
    utime = city["utime"] 
    print("Stripping time:", utime, ",", long);
    utime = utime.strip()
    utime = re.sub(r"on |\.|-", "", utime)
    print("Trying to parse time:", utime + " " + city["tz"]);
    try:
        cityTime = parse(utime + " " + city["tz"]).astimezone(tzutc());
    except:
        utime = re.sub(r"am$|pm$", "", utime)
        cityTime = parse(utime + " " + city["tz"]).astimezone(tzutc());

    print("Time parsed as:", cityTime);
    return cityTime


def writeData(name, city):
        shortName = name[4:]
        curFilename = directory + '/' +'Data/AQICN/' + str(shortName) + "/"
        curFilename += city['dateTime'].strftime("%Y/%m/%d/")
        curFilename += city['dateTime'].strftime("%Y%m%d")
        curFilename += str(shortName) + ".csv"
        ensureDir(curFilename)
        f = open(curFilename, 'a')
        f.write(city['dateTime'].strftime("%Y%m%d%H%M") + ",")
        f.write(str(city['g'][0]) + ",")
        f.write(str(city['g'][1]) + ",")
        f.write(str(city['data'][name]) + "\n")
        f.close()

def handleCity(i, city, cities):
    try:
        print("\n\nScraping "+ city["city"] , i+1, "of",len(cities), city["g"], city["x"])
        city = getUpdatedCity(city);
        if city == None:
            return
        city['dateTime'] = getTime(city)
        #Get the details url from the popup
        city["popupURL"]=("http://aqicn.org/aqicn/json/mapinfo/@" + str(city["x"]))

        print("Popup url is:", city["popupURL"])

        cityDetailPage = requests.get(city["popupURL"]).text
        city["detailURL"] = re.search("http://aqicn\.org/[^\']*", cityDetailPage)

        if city["detailURL"]:
            city["detailURL"] = city["detailURL"].group(0)
            print("City Detail url is:", city["detailURL"])
            page = requests.get(city["detailURL"])

            soup = BeautifulSoup(page.text, "html.parser")
            city["data"] = {}

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
                city['data'][curId] = cur.contents[0]
                writeData(curId, city)

            city['data']['cur_aqi'] = city['aqi']
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

def getUpdatedCity(city):
    cities = getCities()
    for c in cities:
        if c["x"] == city["x"]:
            print("Matched cities for time update")
            print("Old", city)
            print("New", c)
            if c["city"] != city["city"]:
                print("Whoops city is not the same")
            return c
    print("Whoops city not found")
    return None

def getCities():
    #First we must get the main map page
    print("Getting the cities")
    fullMap = requests.get("http://aqicn.org/map/world/").text

    #Find the json embedded in the main page
    print("Finding the json")
    fullMapJsonString = re.search("(?<=mapInitWithData\()\[.*\](?=\))", fullMap)

    #Parse the json
    cities = None
    if fullMapJsonString:
        cities = json.loads(fullMapJsonString.group(0))
    return cities

#helper function for searching, sorting cities
def getX(city):
    try:
        return int(city["x"])
    except:
        print("Not a number", city)
        return -99

if __name__ == '__main__':
    print("Start" ,datetime.datetime.now())
    cities = getCities()
    #Loop through the cities and load each one
    print("There are" ,len(cities) , "cities")
    for i, city in enumerate(cities):
        try:
            int(city["x"])
        except:
            continue
        handleCity(i, city, cities)   
    print("End" ,datetime.datetime.now())
