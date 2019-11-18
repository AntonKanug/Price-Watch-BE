'''
Anton Kanugalwattage
Nov 7, 2019
Adding New Product
Amazon Price Watch Application
'''

import time
import requests
import os
import json
import datetime
from bs4 import BeautifulSoup
from sendEMail import sendEMail

##User Agent
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'

def priceChecker ():

    #Reading data.json file
    with open('data.json', mode='r', encoding='utf-8') as listContent:
        content = json.load(listContent)
    
    #Adding new price of products to a temp
    with open('temp.json', mode='w', encoding='utf-8') as listContent:
        print("")
        for product in content:
            #Getting data for each URL
            response = requests.get(product['URL'], headers = {'User-Agent' : agent})
            soup = BeautifulSoup(response.text, "lxml")  #Intializing soup
            newPrice = soup.find('span', {'class':'a-color-price'}).text.strip()  #Price of the product

            newPriceF = float(newPrice[5:].replace(',',''))
            oldPrice = product['priceList'][-1]['price']

            #Send Email if price lower than 5%
            if (newPriceF - oldPrice)*100/newPriceF <= -5 :
                sendEMail(product['id'], newPriceF)

            #Appending price to list
            product['priceList'].append({
                'price': newPriceF, 
                'dateTime': str(datetime.datetime.now())
                })

            #Printing confirmation
            print("✅  %s - Price Updated"% product['title'])
            print("💵  $%.2f - New Price  \n📅  %s \n"  % (newPriceF,  str(datetime.datetime.now())))
        json.dump(content, listContent, indent=2)


    #Putting the updated list into data.json
    with open('data.json', mode='w', encoding='utf-8') as cpListContent:
        json.dump(content, cpListContent, indent=2)
    
    print("✅  Content of data.json updated")
    
    os.remove('temp.json')
    print("❌  temp.json removed")