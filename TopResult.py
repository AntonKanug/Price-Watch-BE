import requests
from bs4 import BeautifulSoup

#Search URL
URL = 'https://www.amazon.ca/s?k=a7s'

#Requesting the page 
response = requests.get(URL, headers = {'User-Agent' : 'Mozilla/5.0'})
soup = BeautifulSoup(response.text, "lxml") #Intializing soup

#Title of the product
title = soup.findAll("a", {"class": "a-link-normal a-text-normal"})[0].text

#Product's page
productAddress = soup.findAll("a", {"class": "a-link-normal a-text-normal"})[0]['href']
productURL = 'https://www.amazon.ca' + productAddress

##Price of the product
priceWhole = soup.select('.a-price-whole')[0].text
priceDecimal = soup.select('.a-price-fraction')[0].text
price = priceWhole + priceDecimal

##Image of the product
imageLink = soup.find('img', attrs = {'srcset' : True})["src"]
