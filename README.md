aqicn
=====
#####Scraper for aqicn.org

####How To use

Just install the needed libraries below and Python 3.4 and you are good to go.

If you UnicodeException you made need to set the environment variable PYTHONIOENCODING to utf-8

####Output

#####Console
It should look like this
```
Getting the main page
Finding the json
There are 3181 cities
Scraping Weifang () 1 of 3181 ['36.706774', '119.161756'] 1510
Saved cur_pm25,cur_pm10,cur_o3,cur_no2,cur_so2,cur_co,aqi for city Weifang ()
```

Errors will be printed as they occur. Sometimes unicode handling in Python has some issues.
#####Files
Files will be saved to

[directory]/Data/AQICN/Variable/YYYY/MM/yyyymmdd-variable.csv

You can change the base [directory] by editing the script. 

###Written in [Python 3.4](https://www.python.org/downloads/release/python-34/)

####Libraries
Uses [PyPi](https://pypi.python.org/pypi) Versions of

* [Requests2.2.1:](http://docs.python-requests.org/en/latest/)
pip install requests
* [BeautifulSoup4.3.2:](http://www.crummy.com/software/BeautifulSoup/)
pip install beautifulsoup4


###Developed in Eclipse
####Eclipse Plugins

* [PyDev](http://pydev.org/)
* [Markdown Editor](http://www.winterwell.com/software/markdown-editor.php)
* [Markdown Viewer](https://github.com/satyagraha/gfm_viewer)