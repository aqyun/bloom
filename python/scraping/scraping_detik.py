import csv
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

detik = requests.get('https://news.detik.com/')
beautify = BeautifulSoup(detik.content)

news = beautify.find_all('h3', {'class','media__title'})
arti = []
for each in news:
    nu = each.a.get('dtr-id')
    title = each.a.get('dtr-ttl')
    lnk = each.a.get('href')
    newss = beautify.find_all('div', {'class','media__date'})
    ge = requests.get(lnk)
    soup = BeautifulSoup(ge.text, 'html.parser')

    for x in newss:
        date = x.span.get('title')
        sop = soup.find_all('div', {'class', 'page__breadcrumb'})
    for x in sop:
        kategori = x.getText().replace('\n', '').replace('detikNews', '')
        sops = soup.find_all('div', {'class', 'detail__author'})
    for x in sops:
        author = x.getText().replace('-', '').replace('detikNews', '')
        content = soup.find_all('div', {'class', 'detail__body-text itp_bodycontent'})
    for x in content:
        x = x.find_all('p')
        y = [y.text for y in x]
        content_ = ''.join(y).replace('\n', '').replace('ADVERTISEMENT', '').replace('SCROLL TO CONTINUE WITH CONTENT', '')

        arti.append({
            'Id': nu,
            'Kategori' : kategori,
            'Judul': title,
            'Tanggal dan Waktu Terbit' : date,
            'Penulis' : author,
            'Isi Berita' : content_
        })

df = pd.DataFrame(arti)
df.to_csv('detiknews.csv', index=False)

df

detik = requests.get('https://news.detik.com/')
beautify = BeautifulSoup(detik.content, 'html.parser')

links = soup.find_all('a')
for link in links:
    cond = link.get('dtr-evt')
    if cond == 'header' and link.get('dtr-act')=='first navbar':
        print(link.get('href'))
