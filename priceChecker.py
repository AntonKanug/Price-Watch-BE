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

##User Agent
agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'

proxies = {"http": "http://10.10.1.10:3128",
           "https": "http://10.10.1.10:1080"}

def priceChecker ():

    #Reading data.json file
    with open('data.json', mode='r', encoding='utf-8') as listContent:
        content = json.load(listContent)
    
    #Adding new price of products to a temp
    with open('temp.json', mode='w', encoding='utf-8') as listContent:
        print("")
        for product in content:
            try:
                #Getting data for each URL

                # response = requests.get(product['URL'], headers = {'User-Agent' : agent})
                # soup = BeautifulSoup(response.text, "lxml")  #Intializing soup

                response = urllib2.urlopen(product['URL']).read()
                soup = BeautifulSoup(response.decode('utf-8'), "html.parser")  #Intializing soup

                #Price of the product
                newPrice = soup.find('span', {'class':'a-color-price'}).text.strip() 
                
                newPriceF = float(newPrice[5:].replace(',',''))
                oldPrice = product['priceList'][-1]['price']

                #Send Email if price lower than 5%
                if abs((newPriceF - oldPrice)*100/newPriceF) >= 5 :
                    # sendEMail(product['id'], newPriceF)
                    product['priceToCompare'] = newPriceF

                #Appending price to list
                product['priceList'].append({
                    'price': newPriceF, 
                    'dateTime': str(datetime.datetime.now())
                    })

                #Printing confirmation
                print("✅  %s - Price Updated"% product['title'])
                print("💵  $%.2f - New Price  \n📅  %s \n"  % (newPriceF,  str(datetime.datetime.now())))
            except:
                print("❌  parser not working")
                os.remove('temp.json')
                print("❌  temp.json removed\n")
                exit()
        json.dump(content, listContent, indent=2)


    #Putting the updated list into data.json
    with open('data.json', mode='w', encoding='utf-8') as cpListContent:
        json.dump(content, cpListContent, indent=2)
    
    print("✅  Content of data.json updated")
    
    os.remove('temp.json')
    print("❌  temp.json removed")