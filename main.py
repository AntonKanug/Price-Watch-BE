'''
Anton Kanugalwattage
July 4, 2019
Amazon Price Watch Application
'''

import webbrowser 
import time
import requests
import json
from bs4 import BeautifulSoup
from priceChecker import priceChecker
from newProduct import newProduct
from pricePlot import pricePlot

newProduct("beats studio")
#priceChecker()
pricePlot('https://www.amazon.ca/VicTsing-Wireless-Receiver-Adjustment-Computer/dp/B01563HW6U/ref=sr_1_3?keywords=mouse&qid=1573326208&sr=8-3')