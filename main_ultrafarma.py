import os
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

item = 'fortificante'
url_pagina = f'https://www.ultrafarma.com.br/busca?resultsperpage=30&sortby=relevance&q={item}&page={"{}"}'

response = requests.get(url_pagina.format(1))
soup = bs(response.text)
try:
    qtd_paginas = int(soup.find('ul', {'pagination pagination-vitrine'}).findAll('li')[-1].find('a')['data-pagina'])
except:
    qtd_paginas = 1
lista_products = []
print('Capturando dados...')
for pagina in range(1,qtd_paginas+1):
    response = requests.get(url_pagina.format(pagina))
    soup = bs(response.text)
    products = soup.find_all('div', {'col-xs-6 col-sm-6 col-lg-2 prd-list-item'})
    for p in products:
        try:
            nome_produto = p.find('h3',{'class':'product-name font-bold'}).text.strip()
        except:
            nome_produto = None
        try:
            preco_atual = p.find('span',{'class':'product-price-sell'}).text.strip()
        except:
            preco_atual = None
        try:
            preco_antigo = p.find('span',{'class':'product-price-old'}).text.strip()
        except:
            preco_antigo = None
        try:
            link_produto = p.find('a', {'class': 'product-item-link in_stock'})['href']
        except:
            link_produto = None
        
        lista_products.append({'nome_produto':nome_produto, 'preco_atual':preco_atual, 'preco_antigo':preco_antigo, 'link_produto':link_produto})

    for i in range(len(lista_products)):
        url = lista_products[i]['link_produto']
        response = requests.get(url)
        soup = bs(response.text)
        try:
            codigo_ean = str(soup.find('div', {'id': 'pdp-section-outras-informacoes'}).findAll('span')[1].text.strip())[5:]
        except:
            codigo_ean = None
        lista_products[i]['cod_ean'] = codigo_ean
        
df_products = pd.DataFrame(lista_products)
absFilePath = os.path.dirname(os.path.realpath(__file__))
arq = f'{absFilePath}\products_{item}.csv'
df_products.to_csv(arq, encoding='utf-8', index=False, sep=';')
print(f'Arquivo products_{item}.csv Exportado!')


