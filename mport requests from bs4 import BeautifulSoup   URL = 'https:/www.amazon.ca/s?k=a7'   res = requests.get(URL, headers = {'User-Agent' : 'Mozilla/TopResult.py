import requests
from bs4 import BeautifulSoup


URL = 'https://www.amazon.ca/s?k=a7'


res = requests.get(URL, headers = {'User-Agent' : 'Mozilla/5.0'})
soup = BeautifulSoup(res.text, "lxml")
price1 = soup.select('.a-price-whole')[0].text
price2= soup.select('.a-price-fraction')[0].text
price = price1 + price2
print(price)
