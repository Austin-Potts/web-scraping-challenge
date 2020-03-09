Mission to Mars Web Scraping Challenge
--------------------------------------
The purpose of this project is to gather data from several different websites including Twitter, the Mars news website, a mars facts website, and other sources to generate a front end website which can be refreshed with freshly scraped code at the click of a button. The screenshots folder contains two images of the final front end. Templates contains the index.html file, and the geckodriver.exe is a necessary component in the root of the repository to run splinter. The notebook, and scrape_mars.py serve the same purpose but the scrape_mars file is used by the app.py to load the data generated into MongoDB. This data from MongoDb is then placed into the index.html to generate the final result. 

Getting Started
--------------------------------------
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
Keep all of the files in their current locations, some pip installs may be necessary to run all of the code, do not move the location of the geckdriver.exe.

All Dependencies Used:
-----------------------
from bs4 import BeautifulSoup as bs (pip install beautifulsoup4)
-------------------
import requests
-------------------
from splinter import Browser (pip install splinter)
-------------------
import pandas as pd (pip install pandas)
 -------------------
import time
 -------------------
from flask import Flask, render_template, request (pip install -U Flask)
 -------------------
from flask_pymongo import PyMongo (pip install pymongo)
 -------------------

