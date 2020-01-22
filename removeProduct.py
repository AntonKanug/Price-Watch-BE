'''
Anton Kanugalwattage
Jan 2, 2020
Removing a Product
Amazon Price Watch Application
'''

import pymongo
from pymongo import MongoClient

def removeProduct(id, email):
    cluster = MongoClient("mongodb+srv://pwUser:gOpJtmdj6JNWAQpy@pricewatch-zurxa.mongodb.net/test?retryWrites=true&w=majority")
    db = cluster['PriceWatch']
    collection = db['PriceWatch-Products']
    
    products = list(collection.find())

    for product in products:
        if id == product['_id']:
            emailList = []
            for emailIn in product['emailList']:
                if emailIn == email:
                    emailIn = "" 
                emailList.append(emailIn)
            collection.update_one({'_id': id}, {'$set': {'emailList': emailList}})
            print("✅ " + email + " Removed from " + product['title'])
            break
    return "Updated", 201
