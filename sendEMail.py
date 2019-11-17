'''
Anton Kanugalwattage
Nov 16, 2019
Function to send an E-Mail to a user
Amazon Price Watch Application
'''

import smtplib
import json

def sendEMail(id, newPrice):
    ##Initializing  Server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    ##Login to server
    server.login('noreplyPriceWatch@gmail.com', 'hiedscgylqjcpjhd')

    #JSON
    with open('data.json', mode='r', encoding='utf-8') as listContent:
        content = json.load(listContent)
        
    emailList = content[id]['emailList']
    URL = content[id]['URL']
    oldPrice = content[id]['priceList'][-1]['price']
    title = content[id]['title']

    ##Creating Message
    subject = 'Amazon Price Watch Update!'
    body = '%s\nPrice went down by %.2f%% \nNew Price: $%.2f\nOld Price: $%.2f \nCheck link: %s\n' % (title, (newPrice - oldPrice)*100/newPrice, newPrice, oldPrice, URL)
    msg = f"Subject: {subject}\n\n{body}"

    for email in emailList:
        ##Sending E-Mail
        server.sendmail(
            'noreplyPriceWatch@gmail.com',
            email,
            msg
        )
        print("📤  Email Sent to: %s" % email)

    ##Quit the server
    server.quit