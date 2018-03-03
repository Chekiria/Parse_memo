import requests
from bs4 import BeautifulSoup
'''session = requests.session()
session.proxies = {'http':  'socks5://localhost:9150',
                   'https': 'socks5://localhost:9150'}
#Ваш ip
print(requests.get("http://httpbin.org/ip").text)
#Другой ip
print(session.get("http://httpbin.org/ip").text)'''


session = requests.session()
session.proxies = {'http':  'socks5://localhost:9150',
                   'https': 'socks5://localhost:9150'}
''''#Ваш ip
print(requests.get("http://www.canadianbusiness.com/profit500/2017-ranking-p500/"))
#Другой ip
print(session.get("http://www.canadianbusiness.com/profit500/2017-ranking-p500/"))'''



link = session.get('http://www.canadianbusiness.com/profit500/2017-ranking-p500/')

html = link.content

soup = BeautifulSoup(html,'html.parser')
print(soup)