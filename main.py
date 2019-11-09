'''
Anton Kanugalwattage
July 4, 2019
Amazon Price Watch Application
'''
import webbrowser 
import time
import requests
from bs4 import BeautifulSoup
import json
from priceChecker import priceChecker
from newProduct import newProduct

newProduct("pencil")
#priceChecker()