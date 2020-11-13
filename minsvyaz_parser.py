import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# disable warnings InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def write_csv(data):
    ''' Записать в файл csv '''
    with open('reestr_minsvyaz.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow( (data['num'],
                          data['title'], 
                          data['soft_class'],
                          data['soft_url']) )


def get_html(url):
    ''' Получить страницу в виде текста '''
    r = requests.get(url, verify=False)
    return r.text


def get_total_pages(html):
    ''' Получить количество страниц пагинации '''
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='page_nav_area').find_all('a', class_='nav_item')[-2].get('href')
    total_pages = pages.split('=')[1]
    return int(total_pages)


def get_page_data(html):
    ''' Получить данные со страницы '''
    soup = BeautifulSoup(html, 'lxml')

    soft_list = soup.find('div', class_='result_area').find_all('div', class_='line')

    for soft in soft_list:
        try:
            num = soft.find('div', class_='num').text.strip()
        except:
            num = ''

        try:
            title = soft.find('div', class_='name').find('a').text.strip()
        except:
            title = ''
        
        try:
            soft_url = 'https://reestr.minsvyaz.ru' + soft.find('div', class_='name').find('a').get('href')
        except:
            soft_url = ''

        try:
            soft_class = soft.find('div', class_='class').find('span').text.strip()
        except:
            soft_class = ''

        data = {'num': num,
                'title': title,
                'soft_url': soft_url,
                'soft_class': soft_class}

        write_csv(data)


def main():
    start = datetime.now()

    url = 'https://reestr.minsvyaz.ru/reestr/'
    base_url = 'https://reestr.minsvyaz.ru/reestr/?'
    page_part = 'PAGEN_1='
    query_part = ''
    total_pages = get_total_pages(get_html(url))
    
    for i in range(1, total_pages + 1):
        url_gen = base_url + page_part + str(i) + query_part
        html = get_html(url_gen)
        get_page_data(html)

    end = datetime.now()
    total = end - start
    print(str(total))


if __name__ == '__main__':
    main()
