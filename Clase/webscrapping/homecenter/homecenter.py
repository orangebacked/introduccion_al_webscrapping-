#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 19:14:39 2018

@author: emilianoisaza
"""


# importación de librerias

#librería para mandar preguntas a paginas web y extraer su árbol HTML
import requests 

#librería para parsear el HTML
from lxml import html

#libreria para hacer el csv

import pandas as pd

# libreria para nombrar iterativamente el archivo
import datetime

### acá mando el request
r = requests.get('https://www.homecenter.com.co/homecenter-co/search/?Ntt=cemento+kilos')

### Empiezo a parsear el html
tree = html.fromstring(r.content)


#### lista de todas las urls de cementos
listcementos = tree.xpath('//a[contains(@href,"Cemento")]/@href')



#### pruebas
'''
a = listcementos[1]

r1 = requests.get(f'https://www.homecenter.com.co{a}') 

tree = html.fromstring(r1.content)

price = int((tree.xpath('//*[@id="priceContainer"]/div[1]/p[3]/text()')[1]).replace('.',''))
name = str(tree.xpath('//*[@id="productTitleDisplayContainer"]/h1/span/text()'))
brand = str(tree.xpath('//*[@id="productTitleDisplayContainer"]/h2/span/text()'))
'''



##### función 
def scrapping(elementolista):
    a = elementolista
### string formats to get the request
    r = requests.get(f'https://www.homecenter.com.co{a}')
### create the tree
    tree = html.fromstring(r.content)
### get all the elements
    price = int((tree.xpath('//*[@id="priceContainer"]/div[1]/p[3]/text()')[1]).replace('.',''))
    name = str(tree.xpath('//*[@id="productTitleDisplayContainer"]/h1/span/text()')[0])
    brand = str(tree.xpath('//*[@id="productTitleDisplayContainer"]/h2/span/text()')[0])
    return [price, name, brand]


### looop para mandar todas los requests a la página
dflista = []
for n,elementolista in enumerate(listcementos):
    try:
        dflista.append(scrapping(elementolista))
    except:
        pass
    print(elementolista)
    
    
df=pd.DataFrame(dflista,columns=['price','name', 'brand'])


#### hacer un archivo con la fecha de creación 
now = datetime.datetime.now()

y = now.year
m = now.month
d = now.day

df.to_csv(f'Cementos_Homecenter-{y}-{m}-{d}.csv')

