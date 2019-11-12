'''
Anton Kanugalwattage
Nov 7, 2019
Adding New Product
Amazon Price Watch Application
'''

import time
import requests
from bs4 import BeautifulSoup
import json

agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'

def priceChecker ():
    #Reading data.json file
    with open('data.json', mode='r', encoding='utf-8') as listContent:
        content = json.load(listContent)
    
    #Adding new price of products
    with open('data.json', mode='w', encoding='utf-8') as listContent:
        for product in content:
            response = requests.get(product['URL'], headers = {'User-Agent' : agent})
            soup = BeautifulSoup(response.text, "lxml")  #Intializing soup
            productPrice = soup.find('span', {'class':'a-color-price'}).text.strip()  #Price of the product

            product['price'].append(float(productPrice[5:].replace(',','')))

        json.dump(content, listContent, indent=2)