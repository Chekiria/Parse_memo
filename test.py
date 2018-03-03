import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import  re
import json


def get_html (url):
    try:
        response = requests.get(url)
        html = response.text
        return html
    except Exception:
        return None


def make_soup(myString):
    """ Принимает HTML в виде строки, возвращает обьект BeautifulSoup """
    try: # Пробуем что-то сделать
        soup = BeautifulSoup(myString, 'html.parser') # Варим "Суп"
        return soup # Возвращаем обьект "Супа"
    except Exception: # Если произошла ошибка - отлавливаем её(что бы программа не крашнулась)
        return None # В случае ошибки возвращаем None(типо NULL в SQL)

def parse_page(link):
    """ Принимает ссылку страницы, возвращает список результатов """
    try: # Пробуем что-то сделать
        html = get_html(link) # Получаем HTML страницы
        if html != None: # Если HTML удалось получить(то есть в функции [get_html(url)] не было ошибок)
            soup = make_soup(html) # Варим суп
            if soup != None: # Если суп успешно сварился(то есть в функции [make_soup(myString)] не было ошибок)
                divs = soup.find_all('div', class_='genTable') # Ищем все нужные нам div'ы
                if divs: # Если div'ы были найдены
                    cmpLinks = [] # Создаем список дня хранения результатов с текущей страницы
                    for div in divs: # Проходим по списку div'ов
                        a = div.findall('a', rel_='nofollow') # Ищем внутри текущего div тег a
                        if a: # Если ссылку внутри div удалось найти
                            href = a['href'] # получаем значение атрибута href тега a, заодно удаляя все пробелы в начале и в конце
                            #absolute_link = "https://rabota.nur.kz"+href # так как на сайте ссылка относительная, руками делаем её абсолютной
                            cmpLinks.append(href) # добавляем текущую ссылку в наш список результатов
                    return cmpLinks # после обхода всех div'ов возвращаем список результатов с текущей страницы
                else: # Если не удалось найти div'ы
                    raise Exception('Не нашел ни одного <div class="b-seo-one-company__title"> на странице [{0}]'.format(link))  # Генерируем исключение
            else: # Если суп не сварился, то есть функция make_soup вернула None
                raise Exception('Суп не удалось сварить из ссылки: [{0}]'.format(link)) # Генерируем исключение
        else:  # Если HTML не удалось получить, то есть функция get_html вернула None
            raise Exception('HTML не удалось получить  [{0}]'.format(link)) # Генерируем исключение
    except Exception as e: # Если поймали исключение
        print('Ошибка в функции parse_page(). Текст ошибки [{0}]'.format(str(e))) # Выводим на екран сообщение ошибки
        return None # Возвращаем None
#print(parse_page('https://www.nasdaq.com/screening/companies-by-name.aspx?page=1'))


def main(): # Точка входа в программу(ПРОГРАММА НАЧИНАЕТ РАБОТАТЬ ЗДЕСЬ)

    baseUrl = 'https://www.nasdaq.com/screening/companies-by-name.aspx?page=PAGE' # Страницы сайта в виде https://rabota.nur.kz/companies-1
    pagesCount = 2 # Сколько страниц будем парсить
    totalResults = [] # Пустой список для результатов всех страниц
    resultFileName = 'result.txt'

    for i in range(pagesCount): # Проходим по списку [0,1,2,3...99]
        page = i + 1 # Плюсуем 1, потому что на сайте пейджинг начинается с 1
        curPageUrl = baseUrl.replace('PAGE', str(page)) # В строке baseUrl меняем PAGE на номер текущей страницы
        curPageResult = parse_page(curPageUrl) # Пробуем парсить текущую страницу
        if curPageResult: # Если есть результат парсинга и он не пустой и вообще все прошло заебись
            print('Страница [{0}] - успешно. Кол-во результатов - [{1}]'.format(page,len(curPageResult)))
            totalResults.extend(curPageResult) # Добавляем результат парсинга текущей страницы к нашему общему списку резлультатов всех страниц
        else: # Если результата парсинга нет - то есть где-то внутри функции parse_page произошло исключение
            print('Страница [{0}] - неудача.'.format(page))
            continue # Просто переходим к следующей странице

    # После выполнения цикла for у нас есть список рузальтатов со всех страниц типа:
    # ['https://rabota.nur.kz/ТОО+EDU+Stream+ЭДУ+Стрим-jobs-57789', 'https://rabota.nur.kz/ТОО+GO+Travel-jobs-57756', 'https://rabota.nur.kz/ИП+Камажай-jobs-57747'...]

    if totalResults: # Если список результатов не пустой
        file = open(resultFileName, 'wt', encoding='utf-8') # Создаем и открываем файл для записи
        for result in totalResults: # Бежим по списку результатов
            file.write(result+"\n") # Пишем в файл результат + перенос строки
        file.close() # Закрываем файл
        print("Кончил и записал [{0}] результатов в файл [{1}]".format(len(totalResults), resultFileName))
    else:
        print("Нехуй записывать в файл.")

if __name__ == "__main__": # Если этот файл был запущен, а не импортирован
    main() # Вызываем функцию [main()]


'''def pageLinks(page_number):
    page_link = 'https://www.nasdaq.com/screening/companies-by-name.aspx?page={}'.format(page_number)
    response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    meme_links = soup.findAll(lambda tag: tag.name == 'a' and tag.get('rel') == ['nofollow'])
    meme_links = [link.attrs['href'].replace('https://', '') for link in meme_links]
    return meme_links



def main(): # Точка входа в программу(ПРОГРАММА НАЧИНАЕТ РАБОТАТЬ ЗДЕСЬ)

    baseUrl = 'https://rabota.nur.kz/companies-PAGE' # Страницы сайта в виде https://rabota.nur.kz/companies-1
    pagesCount = 5 # Сколько страниц будем парсить
    totalResults = [] # Пустой список для результатов всех страниц
    resultFileName = 'result.txt'

    for i in range(pagesCount): # Проходим по списку [0,1,2,3...99]
        page = i + 1 # Плюсуем 1, потому что на сайте пейджинг начинается с 1
        curPageUrl = baseUrl.replace('PAGE', str(page)) # В строке baseUrl меняем PAGE на номер текущей страницы
        curPageResult = parse_page(curPageUrl) # Пробуем парсить текущую страницу
        if curPageResult: # Если есть результат парсинга и он не пустой и вообще все прошло заебись
            print('Страница [{0}] - успешно. Кол-во результатов - [{1}]'.format(page,len(curPageResult)))
            totalResults.extend(curPageResult) # Добавляем результат парсинга текущей страницы к нашему общему списку резлультатов всех страниц
        else: # Если результата парсинга нет - то есть где-то внутри функции parse_page произошло исключение
            print('Страница [{0}] - неудача.'.format(page))
            continue # Просто переходим к следующей странице

    # После выполнения цикла for у нас есть список рузальтатов со всех страниц типа:
    # ['https://rabota.nur.kz/ТОО+EDU+Stream+ЭДУ+Стрим-jobs-57789', 'https://rabota.nur.kz/ТОО+GO+Travel-jobs-57756', 'https://rabota.nur.kz/ИП+Камажай-jobs-57747'...]

    if totalResults: # Если список результатов не пустой
        file = open(resultFileName, 'wt', encoding='utf-8') # Создаем и открываем файл для записи
        for result in totalResults: # Бежим по списку результатов
            file.write(result+"\n") # Пишем в файл результат + перенос строки
        file.close() # Закрываем файл
        print("Кончил и записал [{0}] результатов в файл [{1}]".format(len(totalResults), resultFileName))
    else:
        print("Нехуй записывать в файл.")'''