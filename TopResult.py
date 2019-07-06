'''
Anton Kanugalwattage
July 4, 2019
'''

import time
import requests
from bs4 import BeautifulSoup

product = "pencils"

agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'

#Search URL
URL = 'https://www.amazon.ca/s?k=' + product

#Requesting the serach page 
response = requests.get(URL, headers = {'User-Agent' : agent})
soup = BeautifulSoup(response.text, "lxml") #Intializing soup

#Excluding sponsored content from search results
sponsored, i = True, 0

while sponsored:
    if soup.findAll("span", {"class": "a-size-base a-color-secondary"})[i].text == "Sponsored":
        sponsored=True
        i+=1
    else:
        sponsored=False


#Title of the product
title = soup.findAll("a", {"class": "a-link-normal a-text-normal"})[i].text.strip()

#Product's page
productAddress = soup.findAll("a", {"class": "a-link-normal a-text-normal"})[i]['href']
productURL = 'https://www.amazon.ca' + productAddress

##Price of the product
priceWhole = soup.select('.a-price-whole')[i].text
priceDecimal = soup.select('.a-price-fraction')[i].text
price = priceWhole + priceDecimal

##Image of the product
imageLink = soup.find('img', attrs = {'srcset' : True})["src"]


#Requesting the serach page 
response = requests.get(productURL, headers = {'User-Agent' :agent})
soup = BeautifulSoup(response.text, "lxml") #Intializing soup

#Rating of the product
rating=soup.find('span', {'class':'a-icon-alt'}).text

print("")
print(rating)
print("")
print(price)
print("")
print(title)
print("")
print(productURL)
print("")
print(imageLink)
print("")
