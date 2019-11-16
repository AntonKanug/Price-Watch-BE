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
from sendEMail import sendEMail

#newProduct("Samsung 49' monitor", 'antondilon2@gmail.com')
#priceChecker()
#sendEMail([ "antondilon@gmail.com", "antondilon2@gmail.com" ], 'https://www.amazon.ca/Corsair-CH-9304111-NA-Scimitar-Backlit-Optical/dp/B01MU3DZYN/ref=sr_1_3?keywords=corsair+mouse&qid=1573324170&sr=8-3')
#pricePlot('https://www.amazon.ca/Corsair-Gaming-Backlit-Optical-CH-9300011-NA/dp/B01D63UU52/ref=sr_1_3?keywords=corsair+mouse&qid=1573918398&sr=8-3')
#pricePlot('https://www.amazon.ca/Corsair-CH-9206015-NA-Gaming-Keyboard-Backlit/dp/B01M4LIKLI/ref=sr_1_3?keywords=corsair+keyboard&qid=1573918414&sr=8-3')