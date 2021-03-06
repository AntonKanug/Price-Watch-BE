'''
Anton Kanugalwattage
Nov 9, 2019
Function for adding New Product
Amazon Price Watch Application
'''

import time
import requests
import datetime
from bs4 import BeautifulSoup
import urllib.request as urllib2
import pymongo
from pymongo import MongoClient

##User Agent
agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'

def newProduct(product, email):
    try:
        # #Requesting the serach page 
        if product[:22] != "https://www.amazon.ca/" and product[:23] != "https://www.amazon.com/":
            ##---REQUESTS
            URL = 'https://www.amazon.ca/s?k=' + product #Search URL
            params = {'access_key': '99ea3af699d6d012f9e7df82ac868e3f', 'url':URL}
            response = requests.get('http://api.scrapestack.com/scrape', params)
            soup = BeautifulSoup(response.text, "lxml") #Intializing soup

            #Excluding sponsored content from search results
            sponsored, i = True, 0
            while sponsored:
                if soup.findAll("span", {"class": "a-size-base a-color-secondary"})[i].text == "Sponsored": #Checking if sponsored
                    sponsored=True
                    i+=1
                else:
                    sponsored=False
            '''
            #To avoid sponsored content on the header
            if soup.find('span', {'class':'sponsoredBy__label'}).text=="Sponsored by ":
                i+=3 #If there are sponsored content on the header there is always 3 products
            '''

            #Product's page
            productAddress = soup.findAll("a", {"class": "a-link-normal a-text-normal"})[i]['href']

            ##Requesting the product page 

            ##---REQUESTS
            productURL = 'https://www.amazon.ca' + productAddress

        else:
            productURL = product

        params = {'access_key': '99ea3af699d6d012f9e7df82ac868e3f', 'url':productURL}
        response = requests.get('http://api.scrapestack.com/scrape', params)
        soup = BeautifulSoup(response.text, "lxml")

        ##Title of the product
        productTitle = soup.find(id='productTitle').text.strip()

        # MongoDB
        cluster = MongoClient("mongodb+srv://pwUser:gOpJtmdj6JNWAQpy@pricewatch-zurxa.mongodb.net/test?retryWrites=true&w=majority")
        db = cluster['PriceWatch']
        collection = db['PriceWatch-Products']
        content = list(collection.find())
        productInList = False

        #Checking if entered product is in database
        for product in content:
            if product['title'] == productTitle:
                productInList = True
                print("\n📦  Product %s is already in databse" % product['title'])

                #Checking if email already in list
                emailInList = False
                for userEMail in product['emailList']:
                    if userEMail == email:
                        emailInList = True
                        print("📤  %s is already in email list" % email)
                        return "Email in list", 204
                #If not in list add it to the email list
                if not emailInList:
                    collection.update({'_id': product['_id']}, {'$push': {'emailList': email}})
                    print("📤  %s is added to email list" % email)
                    return "Email Added", 200
                print("")

        #Adding product if not in databse
        if not productInList:

            ##Price of the product
            try:
                productPrice = soup.find(id='priceblock_ourprice').text.strip() #Accesing through product page to avoid discounts and sponosored products
            except:
                try:
                    productPrice = soup.find(id='priceblock_dealprice').text.strip()
                except:
                    productPrice = soup.find('span', {'class':'a-color-price'}).text.strip()

            ##Title of the product
            productTitle = soup.find(id='productTitle').text.strip()

            #Rating of the product
            try:
                rating=soup.findAll('span', {'class':'a-icon-alt'})[1].text
                rating = float(rating[0:4])
            except:
                rating = 0
                
            ##Image of the product
            imageURLScraped = soup.find('img', {"class": 'a-dynamic-image'})['data-a-dynamic-image']
            imageURLList = imageURLScraped.split("\"") #Due to multiple sizes of images spliting to select one
            imageURL = imageURLList[1]
            print(productURL)
            
            productPrice = productPrice.replace(",","")
            
            try:
                productPriceArr = productPrice.split()
                newPriceF = float(productPriceArr[1])
                productAvailable = True
            except:
                try:
                    newPriceF = float(productPrice[1:])
                    productAvailable = True
                except:
                    productAvailable = False
                    exit()

            post = { '_id': content[-1]['_id']+1, 
                    'title': productTitle,
                    'available': productAvailable,
                    'rating': rating,
                    'URL': productURL,
                    'image': imageURL,
                    'priceToCompare': newPriceF,  
                    'priceList': [{
                        'price': newPriceF, 
                        'dateTime': str(datetime.datetime.now().strftime("%c"))
                        }],
                    'emailList': [email]}
            collection.insert_one(post)
            print("\n📦  Product %s is added to databse" % productTitle)
            print("📤  %s is added to email list\n" % email)
            return "Added", 201
    
    except:
        print("\n❌  %s not found\n" % product)
        return "Not Added", 404