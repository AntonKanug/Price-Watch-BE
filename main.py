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

newProduct("anne pro")
#priceChecker()
#pricePlot('https://www.amazon.ca/Corsair-Gaming-Backlit-Optical-CH-9300011-NA/dp/B01D63UU52/ref=sr_1_3?keywords=corsair+mouse&qid=1573326183&sr=8-3')