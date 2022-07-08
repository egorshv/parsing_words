import string

import requests
from bs4 import BeautifulSoup

from config import HEADERS
from db_dispatcher import DbDispatcher


def get_data():
    table = DbDispatcher('urls.db')
    url = [item[2] for item in table.read_all_data('urls')][-1]
    DATA = []
    req = requests.get(url, headers=HEADERS)
    src = req.text
    # with open('temp.html', 'w', encoding='utf-8') as f:
    #     f.write(src)
    # with open('temp.html', 'r', encoding='utf-8') as f:
    #     src = f.read()
    soup = BeautifulSoup(src, 'lxml')
    p_all = soup.find_all('p')
    for p in p_all:
        symb = '1234567890!@#%^&*()_+=<>/"\'[]{};:\\'
        line = p.text
        line = line.replace('.', '')
        line = line.replace(',', '')
        line = ''.join(x for x in line if x in string.printable)
        text = [word for word in [i for i in line.split() if len(i) > 1] if not (set(symb) & set(word))]
        text = [word for word in text if word not in DATA]
        DATA.extend(text)

    DATA = list(set(DATA))
    return DATA
