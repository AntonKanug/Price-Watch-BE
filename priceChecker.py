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
import urllib.request as urllib2
import pymongo
from pymongo import MongoClient

##User Agent
agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'

proxies = {"http": "http://10.10.1.10:3128",
           "https": "http://10.10.1.10:1080"}

def priceChecker ():

    cluster = MongoClient("mongodb+srv://pwUser:gOpJtmdj6JNWAQpy@pricewatch-zurxa.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster['PriceWatch']
    collection = db['PriceWatch-Products']
    
    content = list(collection.find())
    print("")
    for product in content:
        # try:
        #Getting data for each URL
        response = requests.get(product['URL'], headers = {'User-Agent' : agent})
        soup = BeautifulSoup(response.text, "lxml")  #Intializing soup

        # response = urllib2.urlopen(product['URL']).read()
        # soup = BeautifulSoup(response.decode('utf-8'), "html.parser")  #Intializing soup

        #Price of the product
        newPrice = soup.find('span', {'class':'a-color-price'}).text.strip() 
        try:
            newPriceF = float(newPrice[5:].replace(',',''))
        except:
            continue
        oldPrice = product['priceList'][-1]['price']

        #Send Email if price lower than 5%
        if int(abs((newPriceF - oldPrice)*100/newPriceF)) >= 5 :
            # sendEMail(product['_id'], newPriceF)
            collection.update_one({'_id': product['_id']}, {'$set': {'priceToCompare': newPriceF}})

        #Appending price to list
        collection.update({'_id': product['_id']}, 
        {'$push': {
            'priceList': {
                'price': newPriceF, 
                'dateTime': str(datetime.datetime.now())
            }}})

        #Printing confirmation
        print("✅  %s - Price Updated"% product['title'])
        print("💵  $%.2f - New Price  \n📅  %s \n"  % (newPriceF,  str(datetime.datetime.now())))
        # except:
        #     print("❌  parser not working")
        #     exit()
    
    print("✅  MongoDB updated")