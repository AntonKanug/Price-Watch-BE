'''
Anton Kanugalwattage
Nov 9, 2019
Adding New Product
Amazon Price Watch Application
'''

import time
import requests
from bs4 import BeautifulSoup
import json

agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'

def newProduct(product):

    #Search URL
    URL = 'https://www.amazon.ca/s?k=' + product

    #Requesting the serach page 
    response = requests.get(URL, headers = {'User-Agent' : agent})
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
    productURL = 'https://www.amazon.ca' + productAddress


    ##Requesting the product page 
    response = requests.get(productURL, headers = {'User-Agent' : agent})
    soup = BeautifulSoup(response.text, "lxml") #Intializing soup

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
        for product in content:
            if product['title'] == productTitle:
                productInList = True

        if not productInList:
            entry = { 'id': len(content), 
                    'title': productTitle, 
                    'price': [float(productPrice[5:].replace(',',''))],
                    'rating': rating, 
                    'URL': productURL,
                    'image': imageURL}
            content.append(entry)

        json.dump(content, listContent, indent=2)