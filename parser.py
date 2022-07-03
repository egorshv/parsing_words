import string

import requests
from bs4 import BeautifulSoup

from db_dispatcher import DbDispatcher

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36',
    'Accept': '*/*'}


def get_data():
    table = DbDispatcher('urls.db')
    urls = [item[2] for item in table.read_all_data('urls')]
    DATA = []
    for url in urls:
        req = requests.get(url, headers=HEADERS)
        src = req.text
        # with open('temp.html', 'w', encoding='utf-8') as f:
        #     f.write(src)
        # with open('temp.html', 'r', encoding='utf-8') as f:
        #     src = f.read()
        soup = BeautifulSoup(src, 'lxml')
        p_all = soup.find_all('p')
        for p in p_all:
            symb = '123567890!@#%^&*()_+=<>/"\'[]{}'
            line = p.text
            line = line.replace('.', '')
            line = line.replace(',', '')
            line = ''.join(x for x in line if x in string.printable)
            text = [word for word in line.split() if not (set(symb) & set(word))]
            text = [word for word in text if word not in DATA]
            DATA.extend(text)

    DATA = list(set(DATA))
    return DATA
