'''
Anton Kanugalwattage
Nov 13, 2019
Function for plotting the prices of a product
Amazon Price Watch Application
'''

from matplotlib import pyplot as pylab
import json

def pricePlot (URL):
    with open('data.json', mode='r', encoding='utf-8') as listContent:
        content = json.load(listContent)
        #Finding the product
        productFound = False
        for i in content:
            if i['URL'] == URL:
                prices = i['price']
                title = i['title']
                productFound = True

    if productFound:
        #Creating x axis
        x = []
        for i in range(len(prices)):
            x.append(i)

        #Creating graph
        pylab.figure(num=title)
        pylab.plot(x,prices,'.-')
        pylab.xlabel('days')
        pylab.ylabel('Prices')
        pylab.grid()
        pylab.show()

    else:
        print("Product is not found in database")