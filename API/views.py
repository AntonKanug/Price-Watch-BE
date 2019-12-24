'''
Anton Kanugalwattage
July 4, 2019
Amazon Price Watch mainlication
'''

import pymongo
from pymongo import MongoClient
from flask import Flask, Blueprint, jsonify, request
from .priceChecker import priceChecker
from .newProduct import newProduct
from .pricePlot import pricePlot
from .sendEMail import sendEMail
from flask_cors import CORS, cross_origin


main = Blueprint('main', __name__)
CORS(main)
@main.route('/products')
def products():
    cluster = MongoClient("mongodb+srv://pwUser:gOpJtmdj6JNWAQpy@pricewatch-zurxa.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster['PriceWatch']
    collection = db['PriceWatch-Products']
    content = list(collection.find())
    return jsonify(content)

@main.route('/addProduct', methods = ['POST'])
def addProduct():
    productData = request.get_json()
    # newProduct(productData['title'], productData['email'])
    return productData['title'], productData['email'], 201

if __name__ == '__main__':
    main.debug =True


# newProduct("five star notebook", 'antondilon2@gmail.com')
#priceChecker()
# sendEMail(6,1)
#pricePlot('https://www.amazon.ca/Corsair-Gaming-Backlit-Optical-CH-9300011-NA/dp/B01D63UU52/ref=sr_1_3?keywords=corsair+mouse&qid=1573918398&sr=8-3')
#pricePlot('https:/1/www.amazon.ca/Corsair-CH-9206015-NA-Gaming-Keyboard-Backlit/dp/B01M4LIKLI/ref=sr_1_3?keywords=corsair+keyboard&qid=1573918414&sr=8-3')
