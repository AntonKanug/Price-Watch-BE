'''
Anton Kanugalwattage
Nov 9, 2019
Function for adding New Product
Amazon Price Watch Application
'''

import time
import requests
import json
import datetime
from bs4 import BeautifulSoup
import urllib.request as urllib2

##User Agent
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'

def newProduct(product, email):

    try:
        #Requesting the serach page 

        ##---REQUESTS
        #URL = 'https://www.amazon.ca/s?k=' + product #Search URL
        # response = requests.get(URL, headers = {'User-Agent' : agent})
        # soup = BeautifulSoup(response.text, "lxml") #Intializing soup

        ##---URLLIB2
        URL = 'https://www.amazon.ca/s?k=' + urllib2.quote(product)  #Search URL
        response = urllib2.urlopen(URL).read()
        soup = BeautifulSoup(response.decode('utf-8'), "html.parser")  #Intializing soup

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
        # productURL = 'https://www.amazon.ca' + productAddress
        # response = requests.get(productURL, headers = {'User-Agent' : agent})
        # soup = BeautifulSoup(response.text, "lxml") #Intializing soup

        ##---URLLIB2
        productURL = 'https://www.amazon.ca' +  urllib2.quote(productAddress)
        response = urllib2.urlopen(productURL).read()
        soup = BeautifulSoup(response.decode('utf-8'), "html.parser")  #Intializing soup


        ##Price of the product
        productPrice = soup.find('span', {'class':'a-color-price'}).text.strip() #Accesing through product page to avoid discounts and sponosored products

        ##Title of the product
        productTitle = soup.find(id='productTitle').text.strip()

        #Rating of the product
        rating=soup.find('span', {'class':'a-icon-alt'}).text
        if rating[0]=='o':
            rating = 0
        else:
            rating = float(rating[0:4])
        ##Image of the product
        imageURLScraped = soup.find('img', {"class": 'a-dynamic-image'})['data-a-dynamic-image']
        imageURLList = imageURLScraped.split("\"") #Due to multiple sizes of images spliting to select one
        imageURL = imageURLList[1]

        ##JSON 
        #Reading data.json file
        with open('data.json', mode='r', encoding='utf-8') as listContent:
            content = json.load(listContent)
        
        #Adding the product to data.json file
        with open('data.json', mode='w', encoding='utf-8') as listContent:
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
                    #If not in list add it to the email list
                    if not emailInList:
                        product['emailList'].append(email)
                        print("📤  %s is added to email list" % email)
                    print("")

            #Adding product if not in databse
            if not productInList:
                entry = { 'id': len(content), 
                        'title': productTitle,
                        'priceToCompare': float(productPrice[5:].replace(',','')),  
                        'priceList': [{
                            'price': float(productPrice[5:].replace(',','')), 
                            'dateTime': str(datetime.datetime.now())
                            }],
                        'emailList': [email],
                        'rating': rating, 
                        'URL': productURL,
                        'image': imageURL}
                content.append(entry)
                print("\n📦  Product %s is added to databse" % productTitle)
                print("📤  %s is added to email list\n" % email)
            #JSON dumping data
            json.dump(content, listContent, indent=2) 
    
    except IndexError:
        print("\n❌  %s not found\n" % product)