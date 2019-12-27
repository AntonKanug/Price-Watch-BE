
import time
import requests
import os
import datetime
from bs4 import BeautifulSoup
from sendEMail import sendEMail
import urllib.request as urllib2
import pymongo
from pymongo import MongoClient

agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
URL = "https://www.amazon.ca/ICEBERG-Water-Harvested-Newfoundland-Icebergs/dp/B07WNXTJNH/ref=sr_1_2_sspa?keywords=water&qid=1573991948&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFLWFlDVFhKRk03VjcmZW5jcnlwdGVkSWQ9QTA3ODMyNzMzVlJXV0FRUEI3Vlg2JmVuY3J5cHRlZEFkSWQ9QTA1MjAyMTgxSUJTMjVGNjNCS0ExJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="

response = requests.get(URL, headers = {'User-Agent' : agent})
soup = BeautifulSoup(response.text, "lxml")  #Intializing soup

# response = urllib2.urlopen(product['URL']).read()
# soup = BeautifulSoup(response.decode('utf-8'), "html.parser")  #Intializing soup

#Price of the product
newPrice = soup.find('span', {'class':'a-color-price'}).text.strip()
availability = soup.find(id='availability').text.strip()
print(newPrice)