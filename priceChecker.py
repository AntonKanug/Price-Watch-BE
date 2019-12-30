'''
Anton Kanugalwattage
Nov 7, 2019
Adding New Product
Amazon Price Watch Application
'''

import time
import requests
import os
import datetime
from bs4 import BeautifulSoup
from sendEMail import sendEMail
import urllib.request as urllib2
import pymongo
from pymongo import MongoClient

##User Agent
agent = 'Mozilla/5.0'
proxies = {"http": "http://10.10.1.10:3128",
           "https": "http://10.10.1.10:1080"}

def priceChecker():
    cluster = MongoClient("mongodb+srv://pwUser:gOpJtmdj6JNWAQpy@pricewatch-zurxa.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster['PriceWatch']
    collection = db['PriceWatch-Products']
    
    content = list(collection.find())
    print("")
    for product in content:
        try:
            #Getting data for each URL
            payload = {'api_key': '29fb367e04dcdb47f7d59ad95563e75c', 'url': product['URL']}
            response = requests.get('http://api.scraperapi.com', params=payload)
            soup = BeautifulSoup(response.text, "lxml")  #Intializing soup

            # response = urllib2.urlopen(product['URL']).read()
            # soup = BeautifulSoup(response.decode('utf-8'), "html.parser")  #Intializing soup

            #Price of the product
            newPrice = soup.find('span', {'class':'a-color-price'}).text.strip()
            # availability = soup.find(id='availability').text.strip()
            if newPrice == "Currently unavailable.":
                collection.update_one({'_id': product['_id']}, {'$set': {'available': False}})
                continue
            else:
                collection.update_one({'_id': product['_id']}, {'$set': {'available': True}})

            try:
                newPriceF = float(newPrice[5:].replace(',',''))
            except:
                collection.update_one({'_id': product['_id']}, {'$set': {'available': False}})
                continue

            oldPrice = product['priceToCompare']
            #Send Email if price lower than 5%
            if int(abs((newPriceF - oldPrice)*100/newPriceF)) >= 5 :
                # sendEMail(product['_id'], newPriceF, product['priceToCompare'], product['title'], product['URL'], product['image'], product['emailList'])
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
        except:
            print("❌  parser not working")
            return "Not Updated", 404
    
    print("✅  MongoDB updated")
    return "Updated", 201