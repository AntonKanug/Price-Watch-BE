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
            params = {'access_key': '99ea3af699d6d012f9e7df82ac868e3f', 'url': product['URL']}
            response = requests.get('http://api.scrapestack.com/scrape', params)
            soup = BeautifulSoup(response.text, "lxml")  #Intializing soup

            # response = urllib2.urlopen(product['URL']).read()
            # soup = BeautifulSoup(response.decode('utf-8'), "html.parser")  #Intializing soup

            #Price of the product
            try:
                newPrice = soup.find(id='priceblock_ourprice').text.strip() #Accesing through product page to avoid discounts and sponosored products
            except:
                try:
                    newPrice = soup.find(id='priceblock_dealprice').text.strip()
                except:
                    try:
                        newPrice = soup.find('span', {'class':'a-color-price'}).text.strip()
                    except:
                        collection.update_one({'_id': product['_id']}, {'$set': {'available': False}})
                        continue

            # availability = soup.find(id='availability').text.strip()
            if newPrice == "Currently unavailable.":
                collection.update_one({'_id': product['_id']}, {'$set': {'available': False}})
                continue
            else:
                collection.update_one({'_id': product['_id']}, {'$set': {'available': True}})

            newPrice = newPrice.replace(",","")
            
            try:
                newPriceArr = newPrice.split()
                newPriceF = float(newPriceArr[1])
            except:
                try:
                    newPriceF = float(newPrice[1:])
                except:
                    collection.update_one({'_id': product['_id']}, {'$set': {'available': False}})
                    continue

            oldPrice = product['priceToCompare']
            #Send Email if price lower than 5%
            if int(abs((newPriceF - oldPrice)*100/newPriceF)) >= 5 :
                sendEMail(product['_id'], newPriceF, product['priceToCompare'], product['title'], product['URL'], product['image'], product['emailList'])
                collection.update_one({'_id': product['_id']}, {'$set': {'priceToCompare': newPriceF}})

            #Appending price to list
            collection.update({'_id': product['_id']}, 
            {'$push': {
                'priceList': {
                    'price': newPriceF, 
                    'dateTime': str(datetime.datetime.now().strftime("%c"))
                }}})

            #Printing confirmation
            print("✅  %s - Price Updated"% product['title'])
            print("💵  $%.2f - New Price  \n📅  %s \n"  % (newPriceF,  str(datetime.datetime.now().strftime("%c"))))
        except:
            print("❌  parser not working")
            return "Not Updated", 404
    
    print("✅  MongoDB updated")
    return "Updated", 201