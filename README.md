aqicn
=====
#####Scraper for aqicn.org

####Install

#####OS X:

1. Install from [Python 3.4](https://www.python.org/downloads/release/python-341/)
2. Install the required libraries using pip (see below for libraries)
3. Download [aqicn.py](https://github.com/bryanroscoe/aqicn/blob/master/aqicn.py)
3. Setup the output directory inside the script
4. run the script aqicn.py (you may need to chmod +x)

#####Cent OS:
* You must download and compile Python 3.4

Follow this guide
http://toomuchdata.com/2014/02/16/how-to-install-python-on-centos/
```
wget https://www.python.org/ftp/python/3.4.1/Python-3.4.1.tgz --no-check-certificate
tar -xzvf Python-3.4.1.tgz
cd Python-3.4.1
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
./configure --prefix=/usr/local --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
make && sudo make altinstall
#PyPi will be installed at /usr/local/bin/pip3.4
sudo /usr/local/bin/pip3.4 install requests
sudo /usr/local/bin/pip3.4 install beautifulsoup4
```
* Download [aqicn.py](https://github.com/bryanroscoe/aqicn/blob/master/aqicn.py)
* Setup the output directory inside the script
* run the script aqicn.py (you may need to chmod +x)
* change the script to look use the python /usr/local/bin/python3.4 instaed of /usr/bin/python

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

###Written in [Python 3.4](https://www.python.org/downloads/release/python-341/)

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
