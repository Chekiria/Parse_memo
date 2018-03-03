import requests
import numpy as np
import pandas as pd
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from tqdm import tqdm_notebook
import json

'''page_link = 'http://knowyourmeme.com/memes/all/page/1'
response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
#print(response)

#for key, value in response.request.headers.items ():
#    print(key+": " + value)

html = response.content
#html[:100]
#print(html[:1000])

soup = BeautifulSoup(html, 'html.parser')
#p=soup.html.head.title.text

#obj = soup.find(lambda tag: tag.name =='a' and tag.get('class')==['photo'])
#a = obj.attrs['href']
#print(a)

meme_links = soup.findAll(lambda tag: tag.name =='a' and tag.get('class')==['photo'])
meme_links = [link.attrs['href'] for link in meme_links]
meme_links[:10]


#print(meme_links)'''



def getPageLinks(page_number):
    """
        Возвращает список ссылок на мемы, полученный с текущей страницы

        page_number: int/string
            номер страницы для парсинга

    """
    # составляем ссылку на страницу поиска
    page_link = 'http://knowyourmeme.com/memes/all/page/{}'.format(page_number)

    # запрашиваем данные по ней
    response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})

    if not response.ok:
        # если сервер нам отказал, вернем пустой лист для текущей страницы
        return []
    # получаем содержимое страницы и переводим в суп
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    # наконец, ищем ссылки на мемы и очищаем их от ненужных тэгов
    meme_links = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['photo'])
    meme_links = ['http://knowyourmeme.com' + link.attrs['href'] for link in meme_links]

    return meme_links


'''#meme_links = getPageLinks(1)
#print(meme_links[:2])

meme_page = 'http://knowyourmeme.com/memes/doge'
response = requests.get(meme_page, headers={'User-Agent': UserAgent().chrome})
html = response.content
soup = BeautifulSoup(html,'html.parser')

views = soup.find('dd', attrs={'class':'views'})
#print(views)

views = views.find('a').text
views = int(views.replace(',', ''))
#print(views)'''

def getStats(soup, stats):
    """
        Возвращает очищенное число просмотров/коментариев/...

        soup: объект bs4.BeautifulSoup
            суп текущей страницы

        stats: string
            views/videos/photos/comments

    """

    obj = soup.find('dd', attrs={'class':stats})
    obj = obj.find('a').text
    obj = int(obj.replace(',', ''))

    return obj


'''views = getStats(soup, stats='views')
videos = getStats(soup, stats='videos')
photos = getStats(soup, stats='photos')
comments = getStats(soup, stats='comments')

print("Просмотры: {}\nВидео: {}\nФото: {}\nКомментарии: {}".format(views, videos, photos, comments))


date = soup.find('abbr', attrs ={'class':'timeago'}).attrs['title']
print(date)'''


def getProperties(soup):
    """
        Возвращает список (tuple) с названием, статусом, типом,
        годом и местом происхождения и тэгами

        soup: объект bs4.BeautifulSoup
            суп текущей страницы

    """
    # название - идёт с самым большим заголовком h1, легко найти
    meme_name = soup.find('section', attrs = {'class':'info'}).find('h1').text.strip()

    # достаём все данные справа от картинки
    properties = soup.find('aside', attrs = {'class':'left'})

    # статус идет первым - можно не уточнять класс
    meme_status = properties.find("dd")

    # oneliner, заменяющий try-except: если тэга нет в properties, вернётся объект NoneType,
    # у которого аттрибут text отсутствует, и в этом случае он заменится на пустую строку

    meme_status = "" if not meme_status else meme_status.text.strip()

    # тип мема - обладает уникальным классом
    meme_type = properties.find('a', attrs = {'class':'entry-type-link'})
    meme_type = "" if not meme_type else meme_type.text

    # год происхождения первоисточника можно найти после заголовка Year,
    # находим заголовок, определяем родителя и ищем следущего ребенка - наш раздел
    meme_origin_year = properties.find(text='\nYear\n')
    meme_origin_year = "" if not meme_origin_year else meme_origin_year.parent.find_next()
    meme_origin_year = meme_origin_year.text.strip()

    # сам первоисточник
    meme_origin_place = properties.find('dd', attrs = {'class':'entry_origin_link'})
    meme_origin_place = "" if not meme_origin_place else meme_origin_place.text.strip()

    # тэги, связанные с мемом
    meme_tags = properties.find('dl', attrs={'id':'entry_tags'}).find('dd')
    meme_tags = "" if not meme_tags else meme_tags.text.strip()

    return  meme_name, meme_status, meme_type, meme_origin_year, meme_origin_place, meme_tags



def getText(soup):
    """
        Возвращает текстовые описания мема

        soup: объект bs4.BeautifulSoup
            суп текущей страницы

    """

    # достаём все тексты под картинкой
    body = soup.find('section', attrs={'class':'bodycopy'})
    # раздел about (если он есть), должен идти первым, берем его без уточнения класса
    meme_abaut = body.find('p')
    meme_abaut = "" if not meme_abaut else meme_abaut.text

    # раздел origin можно найти после заголовка Origin или History,
    # находим заголовок, определяем родителя и ищем следущего ребенка - наш раздел
    meme_origin = body.find(text='Origin') or body.find(text='History')
    meme_origin = "" if not meme_origin else meme_origin.parent.find_next().text

    # весь остальной текст (если он есть) можно запихнуть в одно текстовое поле
    if body.text:
        other_text = body.text.strip().split('\n')[4:]
        other_text = " ".join(other_text).strip()
    else:
        other_text = ""

    return  meme_abaut, meme_origin, other_text


'''meme_about, meme_origin, other_text = getText(soup)

print("О чем мем:\n{}\n\nПроисхождение:\n{}\n\nОстальной текст:\n{}...\n"\
      .format(meme_about, meme_origin, other_text[:200]))'''


def getMemeData(meme_page):
    """
            Запрашивает данные по странице, возвращает обработанный словарь с данными

            meme_page: string
                ссылка на страницу с мемом

        """

    # запрашиваем данные по ссылке
    response = requests.get(meme_page, headers={'User-Agent': UserAgent().chrome})

    if not response.ok:
        # если сервер нам отказал, вернем статус ошибки
        return response.status_code

    # получаем содержимое страницы и переводим в суп
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    # используя ранее написанные функции парсим информацию
    views = getStats(soup=soup,stats='views')
    videos = getStats(soup=soup, stats='videos')
    photos = getStats(soup=soup, stats='photos')
    comments = getStats(soup=soup, stats='comments')

    # дата
    date = soup.find('abbr', attrs={'class': 'timeago'}).attrs['title']

    # имя, статус, и т.д.
    meme_name, meme_status, meme_type, meme_origin_year, meme_origin_place, meme_tags=\
    getProperties(soup=soup)

    # текстовые поля
    meme_about, meme_origin, other_text = getText(soup=soup)

    # составляем словарь, в котором будут хранится все полученные и обработанные данные
    data_row = {"name":meme_name, "status":meme_status,
                "type":meme_type, "origin_year":meme_origin_year,
                "origin_place":meme_origin_place,
                "date_added":date, "views":views,
                "videos":videos, "photos":photos, "comments":comments, "tags":meme_tags,
                "about":meme_about, "origin":meme_origin, "other_text":other_text}

    return data_row




#print(getMemeData)

'''final_df = pd.DataFrame(columns=['name', 'status', 'type', 'origin_year', 'origin_place', 'date_added', 'views', 'videos', 'photos', 'comments', 'tags', 'about', 'origin', 'other_text'])

data_row = getMemeData('http://knowyourmeme.com/memes/doge')
final_df = final_df.append(data_row, ignore_index=True)
print(final_df)

for meme_link in meme_links:
    data_row = getMemeData(meme_link)
    final_df = final_df.append(data_row, ignore_index=True)

#print(final_df)'''

'''for i in range(1075):  # Проходим по списку [0,1,2,3...99]
    page = i + 1  # Плюсуем 1, потому что на сайте пейджинг начинается с 1
    curPageUrl = baseUrl.replace('PAGE', str(page))  # В строке baseUrl меняем PAGE на номер текущей страницы
    curPageResult = parse_page(curPageUrl)  # Пробуем парсить текущую страницу
    if curPageResult:  # Если есть результат парсинга и он не пустой и вообще все прошло заебись
        print('Страница [{0}] - успешно. Кол-во результатов - [{1}]'.format(page, len(curPageResult)))
        totalResults.extend(
            curPageResult)  # Добавляем результат парсинга текущей страницы к нашему общему списку резлультатов всех страниц
    else:  # Если результата парсинга нет - то есть где-то внутри функции parse_page произошло исключение
        print('Страница [{0}] - неудача.'.format(page))
        continue  # Просто переходим к следующей странице

# Немного красивых циклов. При желании пакет можно отключить и
# удалить команду tqdm_notebook из всех циклов
#from tqdm import tqdm_notebook'''

'''final_df = pd.DataFrame(columns=['name', 'status', 'type', 'origin_year', 'origin_place',
                                 'date_added', 'views', 'videos', 'photos', 'comments',
                                 'tags', 'about', 'origin', 'other_text'])

for page_number in tqdm_notebook(range(1075), desc='Pages'):
    # собрали хрефы с текущей страницы
    meme_links = getPageLinks(page_number)
    for meme_link in tqdm_notebook(meme_links, desc='Memes', leave=False):
        # иногда с первого раза страничка не парсится
        for i in range(5):
            try:
                # пытаемся собрать по мему немного даты
                data_row = getMemeData(meme_link)
                # и закидываем её в таблицу
                final_df = final_df.append(data_row, ignore_index=True)
                # если всё получилось - выходим из внутреннего цикла
                break
            except:
                # Иначе, пробуем еще несколько раз, пока не закончатся попытки
                print('AHTUNG! parsing once again:', meme_link)
                continue

print(final_df)'''




final_df = []

for page_number in range(1):
    # собрали хрефы с текущей страницы
    meme_links = getPageLinks(page_number)
    for meme_link in meme_links:
        # иногда с первого раза страничка не парсится
        for i in range(1):
            try:
                # пытаемся собрать по мему немного даты
                data_row = getMemeData(meme_link)
                # и закидываем её в таблицу
                final_df.append(data_row)
                # если всё получилось - выходим из внутреннего цикла
                break
            except:
                # Иначе, пробуем еще несколько раз, пока не закончатся попытки
                print('AHTUNG! parsing once again:', meme_link)
                continue
    page_number += 1
#print(meme_links)

#print(final_df)

resultFileName = 'result.txt'

'''if final_df: # Если список результатов не пустой
        file = open(resultFileName, 'w', encoding='utf-8') # Создаем и открываем файл для записи
        for result in final_df: # Бежим по списку результатов
            file.write(result) # Пишем в файл результат + перенос строки
        file.close() # Закрываем файл
        print("Кончил и записал [{0}] результатов в файл [{1}]".format(len(final_df), resultFileName))
else:
        print("Нехуй записывать в файл.")'''



if final_df: # Если список результатов не пустой
        with open('result.txt', 'w',encoding='utf-8') as outfile:
            #file = open(resultFileName, 'w', encoding='utf-8') # Создаем и открываем файл для записи
            for result in final_df: # Бежим по списку результатов
                json.dump(result, outfile) # Пишем в файл результат + перенос строки
            #file.close() # Закрываем файл
            outfile.close()  # Закрываем файл
            print("Кончил и записал [{0}] результатов в файл [{1}]".format(len(final_df), resultFileName))
else:
        print("нет записей в файл.")
