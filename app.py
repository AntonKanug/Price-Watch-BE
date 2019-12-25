'''
Anton Kanugalwattage
July 4, 2019
Amazon Price Watch application
'''

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pymongo
from pymongo import MongoClient
from priceChecker import priceChecker
from newProduct import newProduct
from sendEMail import sendEMail

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "<h3>Welcome to backend of Price Watch</h3><h4>By Anton Kanugalawattage</h4>"

@app.route('/products')
def products():
    cluster = MongoClient("mongodb+srv://pwUser:gOpJtmdj6JNWAQpy@pricewatch-zurxa.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster['PriceWatch']
    collection = db['PriceWatch-Products']
    content = list(collection.find())
    return jsonify(content)

@app.route('/addProduct', methods = ['POST'])
def addProduct():
    productData = request.get_json()
    return newProduct(productData['title'], productData['email'])

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run()
