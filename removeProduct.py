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

    product = collection.find_one({"_id": id})
    emailList = product['emailList']
    try:
        emailList.remove(email)
    except:
        return "Not Removed, Email not found", 404

    if not len(emailList):
       emailList = [""] 
    collection.update_one({'_id': id}, {'$set': {'emailList': emailList}})
    print("✅ " + email + " Removed from " + product['title'])

    return "Email Removed", 201
