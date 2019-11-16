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
from datetime import date
import datetime
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'

def priceChecker ():

    today = date.today()
    #Reading data.json file
    with open('data.json', mode='r', encoding='utf-8') as listContent:
        content = json.load(listContent)
    
    #Adding new price of products
    with open('data.json', mode='w', encoding='utf-8') as listContent:
        print("")
        for product in content:
            #Getting data for each URL
            response = requests.get(product['URL'], headers = {'User-Agent' : agent})
            soup = BeautifulSoup(response.text, "lxml")  #Intializing soup
            newPrice = soup.find('span', {'class':'a-color-price'}).text.strip()  #Price of the product

            #Appending price to list
            newPriceF = float(newPrice[5:].replace(',',''))
            product['priceList'].append({
                'price': newPriceF, 
                'dateTime': str(datetime.datetime.now())
                })

            #Printing confirmation
            print("✅  %s - Price Updated"% product['title'])
            print("💵  %.2f - New Price  \n📅  %s \n"  % (newPriceF,  str(today.strftime("%B %d, %Y"))))
        json.dump(content, listContent, indent=2)