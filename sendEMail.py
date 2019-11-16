'''
Anton Kanugalwattage
Nov 16, 2019
Function to send an E-Mail to a user
Amazon Price Watch Application
'''

import smtplib

def sendEMail(emailList, URL):
    ##Initializing  Server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    ##Login to server
    server.login('noreplyPriceWatch@gmail.com', 'hiedscgylqjcpjhd')

    ##Creating Message
    subject = 'Amazon Price Watch Update!'
    body = 'Check link: \n'+ URL
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