import requests
from bs4 import BeautifulSoup

URL = 'https://www.amazon.com/Hamilton-Beach-58148A-Smoothies-function/dp/B00EI7DPI0/ref=sr_1_1_sspa?keywords=blender&qid=1562349076&s=gateway&sr=8-1-spons&psc=1'

res = requests.get(URL, headers = {'User-Agent' : 'Mozilla/5.0'})
soup = BeautifulSoup(res.text, "lxml")
price = soup.select_one('#priceblock_ourprice').text
print(price)
