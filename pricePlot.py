from matplotlib import pyplot as pylab
import json

def pricePlot (URL):
    with open('data.json', mode='r', encoding='utf-8') as listContent:
        content = json.load(listContent)
        for i in content:
            if i['URL'] == URL:
                prices = i['price']
    x = []
    for i in range(len(prices)):
        x.append(i)

    pylab.plot(x,prices)
    pylab.xlabel('days')
    pylab.ylabel('Prices')
    pylab.grid()
    pylab.show()