
import time
import requests
import os
import datetime
from bs4 import BeautifulSoup
from sendEMail import sendEMail
import urllib.request as urllib2
import pymongo
from pymongo import MongoClient
from priceChecker import priceChecker
from newProduct import newProduct

# newProduct("nike shoes", "antondilon@gmail.com")
# agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
# URL = "https://www.amazon.ca/ICEBERG-Water-Harvested-Newfoundland-Icebergs/dp/B07WNXTJNH/ref=sr_1_2_sspa?keywords=water&qid=1573991948&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFLWFlDVFhKRk03VjcmZW5jcnlwdGVkSWQ9QTA3ODMyNzMzVlJXV0FRUEI3Vlg2JmVuY3J5cHRlZEFkSWQ9QTA1MjAyMTgxSUJTMjVGNjNCS0ExJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="

# response = requests.get(URL, headers = {'User-Agent' : agent})
# soup = BeautifulSoup(response.text, "lxml")  #Intializing soup

# # response = urllib2.urlopen(product['URL']).read()
# # soup = BeautifulSoup(response.decode('utf-8'), "html.parser")  #Intializing soup

# #Price of the product
# newPrice = soup.find('span', {'class':'a-color-price'}).text.strip()
# availability = soup.find(id='availability').text.strip()
# print(newPrice)

# params = {'access_key': '99ea3af699d6d012f9e7df82ac868e3f', 'url':
# 'https://www.amazon.ca/Nintendo-Switch-Neon-Blue-Joy%E2%80%91/dp/B07VGRJDFY/ref=sr_1_3?keywords=nintendo+switch&qid=1577814008&sr=8-3'}

# response = requests.get('http://api.scrapestack.com/scrape', params)
# soup = BeautifulSoup(response.text, "lxml") #Intializing soup
# productPrice = soup.find('span', {'class':'a-color-price'}).text.strip()
# productTitle = soup.find(id='title').text.strip()
# rating=soup.find('span', {'class':'a-icon-alt'}).text
# print(rating)
# if rating[0]=='o':
#     rating = 0
# else:
#     rating = float(rating[0:4])

# productPriceArr = productPrice.split()
# print(productPriceArr[1])


# x = "https://www.amazon.ca/s?k="
# print(x[0:21])

# newProduct("apple", 'antondilon@gmail.com')
URL = "https://www.amazon.com/Hewlett-Packard-Enterprise-Graphics-Card/dp/B07SZWX14R/ref=sr_1_1?qid=1577956512&s=computers-intl-ship&sr=1-1"
params = {'access_key': '99ea3af699d6d012f9e7df82ac868e3f', 'url': URL}
response = requests.get('http://api.scrapestack.com/scrape', params)
soup = BeautifulSoup(response.text, "lxml")  #Intializing soup
available = True
# response = urllib2.urlopen(product['URL']).read()
# soup = BeautifulSoup(response.decode('utf-8'), "html.parser")  #Intializing soup

#Price of the product
try:
    newPrice = soup.find(id='priceblock_ourprice').text.strip()
except:
    try:
        newPrice = soup.find(id='priceblock_dealprice').text.strip()
    except:
        try:
            newPrice = soup.find('span', {'class':'a-color-price'}).text.strip()
        except:
            available = False
print(available)
print(newPrice)
# availability = soup.find(id='availability').text.strip()
if newPrice == "Currently unavailable.":
    available = False
else:
    available = True

newPrice = newPrice.replace(",","")

try:
    newPriceArr = newPrice.split()
    newPriceF = float(newPriceArr[1])
except:
    try:
        newPriceF = float(newPrice[1:])
    except:
        available = False
print(available)
print(newPriceF)