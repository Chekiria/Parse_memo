import  requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

UserAgent().chrome


#page_link = 'http://www.canadianbusiness.com/profit500/2017-ranking-p500/'
page_link = 'https://us7.proxysite.com/process.php?d=QvjmeGEf8uj8ZBwNOKUDe%2Bg9BTHco%2FVDd7B374FjtKN%2B1IgCqVqidcxtaDhwAt7%2BBef2pSUQUMA%3D&b=1&f=norefer'
response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
html = response.content
soup = BeautifulSoup(html, 'html.parser')
print(soup)



'''session = requests.session()
session.proxies = {'http':  'socks5://localhost:9150',
                   'https': 'socks5://localhost:9150'}
#Ваш ip
print(requests.get("http://httpbin.org/ip").text)
#Другой ip
print(session.get("http://httpbin.org/ip").text)'''