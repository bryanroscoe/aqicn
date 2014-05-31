aqicn
=====
#####Scraper for aqicn.org

####Install

1. Make sure you have Python 3.4 installed.
2. Install the required libraries using pip (see below for libraries)
3. Setup the output directory inside the script
4. Run the script aqicn.py

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

You can change the base [directory] by editing the script. It is defaulted to "./"

####Troubleshooting

If you UnicodeException you made need to set the enviroment variable PYTHONIOENCODING to utf-8

###Written in [Python 3.4](https://www.python.org/downloads/release/python-34/)

####Libraries
Uses [PyPi](https://pypi.python.org/pypi) Versions of

* [Requests2.2.1:](http://docs.python-requests.org/en/latest/)
pip install requests
* [BeautifulSoup4.3.2:](http://www.crummy.com/software/BeautifulSoup/)
pip install beautifulsoup4

Just run the command after the colon to install them with pip. pip is installed with Python 3.4

###Developed in Eclipse
####Eclipse Plugins

* [PyDev](http://pydev.org/)
* [Markdown Editor](http://www.winterwell.com/software/markdown-editor.php)
* [Markdown Viewer](https://github.com/satyagraha/gfm_viewer)
