import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import  re
import json

def pageLinks(page_number):
    page_link = 'https://www.nasdaq.com/screening/companies-by-name.aspx?page={}'.format(page_number)
    response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    meme_links = soup.findAll(lambda tag: tag.name == 'a' and tag.get('rel') == ['nofollow'])
    #meme_links = [link.attrs['href'].replace('https://', '') for link in meme_links]
    meme_links = [link.attrs['href'].replace('companies-by-name', '') for link in meme_links]
    return meme_links



final_df = []

for page_number in range(1,2):
    # собрали хрефы с текущей страницы
    meme_links = pageLinks(page_number)
    page = 0
    for meme_link in meme_links:
        # иногда с первого раза страничка не парсится
        for i in range(1):
            try:
                final_df.append(meme_links)
                print(meme_link)
                # если всё получилось - выходим из внутреннего цикла
                break
            except:
                # Иначе, пробуем еще несколько раз, пока не закончатся попытки
                print('AHTUNG! parsing once again:', meme_link)
                continue

resultFileName = 'nasdaq.txt'



if final_df: # Если список результатов не пустой
        with open('nasdaq.txt', 'w',encoding='utf-8') as outfile:
            #file = open(resultFileName, 'w', encoding='utf-8') # Создаем и открываем файл для записи
            for result in final_df: # Бежим по списку результатов
                json.dump(result, outfile) # Пишем в файл результат + перенос строки
            #file.close() # Закрываем файл
            outfile.close()  # Закрываем файл
            print("Записал [{0}] результатов в файл [{1}]".format(len(final_df), resultFileName))
else:
        print("Нет записей в файл.")
