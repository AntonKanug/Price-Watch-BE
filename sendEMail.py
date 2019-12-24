'''
Anton Kanugalwattage
Nov 16, 2019
Function to send an E-Mail to a user
Amazon Price Watch Application
'''

import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders 

def sendEMail(id, newPrice, oldPrice, title, URL, image, emailList):
    try:
        ##Initializing  Server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        ##Login to server
        #server.login('antondilon2@gmail.com', 'drpehshhdqzshmju')
        server.login('noreplyPriceWatch@gmail.com', 'fjcrfaubmimqbfty')

        ##Creating Message
        msg = MIMEMultipart() 
        msg['From'] = 'Price Watch'

        if newPrice < oldPrice:
            colour = 'rgb(84, 209, 0)'
            msg['Subject'] = 'Price of ' + title + ' Went Down to $' + str(str(newPrice)) + '!'
            msgTitle = 'Price Went Down!'
            sign = ''
        else:
            colour = 'rgb(209, 59, 0)'
            msg['Subject'] = 'Price of ' + title+  ' Went Up to $' + str(newPrice) + '!'
            msgTitle = 'Price Went Up!'
            sign= '+'
        # body = '%s\nPrice changed by %.2f%% \nNew Price: $%.2f\nOld Price: $%.2f \nCheck link: %s\n' % (title, (newPrice - oldPrice)*100/newPrice, newPrice, oldPrice, URL)
        # msg.attach(MIMEText(body, 'plain')) 
        # msg.attach(image)
        html = """\
                <!DOCTYPE html>
                    <link href="https://fonts.googleapis.com/css?family=Nunito+Sans:700,800,900&display=swap" rel="stylesheet" type='text/css'>
                    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" rel="stylesheet" type='text/css'>
                    <html>
                    <body>
                    <div style="margin:auto; max-width:860px; background-color:#F5F7FA; border-radius:25px; " >
                    <div style="padding:20px; font-family: 'Nunito Sans', sans-serif; margin-bottom: 10px; flex-wrap: wrap; flex-direction: row; display: flex" >
                        <div style="margin:auto; margin-top:20px; margin-bottom: 20px; padding: 10px; background: white; border-radius: 25px;">

                        <img src=" """+ image +"""" " style="max-width:260px; max-height:400px; margin-top: 10%;">
                        </div>
                        <div style="margin:20px; margin:auto; margin-top:40px; max-width:360px; padding-left: 15px;">
                        <p style="font-size:30px; font-family: 'Nunito Sans', sans-serif; margin-top:0px; margin-bottom: 0px; font-weight: 800; color: #232F3E" >"""+msgTitle+"""</p>
                        <p style="font-size:15px; font-family: 'Nunito Sans', sans-serif; margin-top:10px; margin-bottom: 10px; font-weight: 800; color: #232F3E">"""+title+"""</p>
                        <p style="font-size:25px; color:"""+colour+ """;font-family: 'Nunito Sans', sans-serif;  font-weight: 800; display: inline;" >$"""+str(newPrice)+ """</p>
                        <p style="font-size:17px; color:"""+colour+ """;font-family: 'Nunito Sans', sans-serif;  font-weight: 800; display: inline;" >("""+sign+str(round( ((newPrice-oldPrice)*100/oldPrice) ,2))+ """%)</p>
                        <a
                        style="padding-top: 0px;
                                display:inherit;
                                font-size: 18px;
                                height: 35px;
                                width: 250px;   
                                border: 0;
                                border-radius: 280px;
                                font-family: 'Nunito Sans', sans-serif;
                                font-weight: 700;
                                font-size: 19px;
                                filter: drop-shadow(1px 2px 2px rgba(0,0,0,0.16));
                                background: #FEBD69;
                                margin-top: 10px;
                                text-decoration: none;
                                color: #232F3E;
                                padding-top: 8.25px;
                                text-align: center;
                                display:inherit;"
                                href=\""""+ URL + """\"
                                target = "_blank"
                            >View Product</a>
                                <p style="font-size: 13px;  margin-top: 30px; font-family: 'Nunito Sans', sans-serif; font-weight: 600;">Thanks for using Price Watch!</p>
                                <p style="font-size: 13px;  margin-top: -13px; font-family: 'Nunito Sans', sans-serif; font-weight: 600;">Made by Anton Kanugalawattage, 2019</p>
                                </div>
                            </div>
                            <div style="height: 50px; width:100%; background:#37475A; border-radius:0px 0px 23px 23px; font-family: 'Nunito Sans', sans-serif; flex-direction: row;  flex-wrap: wrap;display: flex">
                            <div>
                                <img src="https://i.imgur.com/hGaCEWT.png" width="auto" height="37px" style="padding:6px">
                            </div>
                        <!-- <div style="flex-grow: 1"></div>
                        <p style="margin-top:12px; padding-right:20px; color: rgb(173, 173, 173); font-size: 16px">Contact Us: info@helpinghandsapp.com</p>
                        </div> -->
                    </div>
                </body>
                </html>"""

        text = MIMEText(html, 'html')
        msg.attach(text)

        for email in emailList:
            ##Sending E-Mail
            server.sendmail(
                'noreplyPriceWatch@gmail.com',
                email,
                msg.as_string()
            )
            print("📤  Email Sent to: %s" % email)

        ##Quit the server
        server.quit
    except smtplib.SMTPDataError:
        print("\n❌  Emails not sent")