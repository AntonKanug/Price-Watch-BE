import time
import requests
from bs4 import BeautifulSoup
import json

agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'

def priceChecker ():

    with open('data.json', mode='r', encoding='utf-8') as listContent:
        content = json.load(listContent)

    with open('data.json', mode='w', encoding='utf-8') as listContent:
        for i in content:
            response = requests.get(i['URL'], headers = {'User-Agent' : agent})
            soup = BeautifulSoup(response.text, "lxml")  #Intializing soup
            productPrice = soup.find('span', {'class':'a-color-price'}).text.strip()  #Price of the product

            i['price'].append(float(productPrice[5:]))

        json.dump(content, listContent, indent=2)