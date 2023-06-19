
from asyncio import constants
from pyparsing import line
import requests
import asyncio
from pyppeteer import launch
import urllib
import datetime
from threading import Thread

now = datetime.date.today()+datetime.timedelta(days=-1)


#чтение по ссылке

url1=f'https://webanetlabs.net/proxylist2022/spisok_proksi_na_{now.strftime("%d.%m.%Y")}.html'
url2='https://advanced.name/freeproxy/6240642a03e73'
url_list = [url1, url2]
#print(type(url_list[1]))
good_p=[]

def get_(url):
    get = requests.get(url)
    a=get.text
    if ('<html>' in a):
        z=a.replace('</body>','<body>').split('<body>')
        a=z[1].replace('<br>','').replace('\r','').split('\n')
        return a
    else:

        a=a.replace('\r','').split('\n')
        #a.split()
        return a

def check(url):
    print(f'\t\t\t{url}')
    line_count = 0
    z=get_(url)

    for i in range(len(z)):
        
        a=z[i]
        print(a)

        https_proxy = f'http://{a}'#f"{row[0]}"
        proxies = { 
                "http" : https_proxy, 
            }
        url = 'http://www.python.org'
        dat={
            'method': 'GET'
            #'mode': 'no-cors',
        }
        line_count +=1
        try:           
            r =  requests.post(url, params=dat, proxies=proxies, timeout=5)
            if (r.status_code == 200):
                print('--------------------------------------------------------')
                print(f'\t\t\t\t\t{a}')
                print(f'\t\t\t\t\t{r.status_code}')
                print('--------------------------------------------------------')
                good_p.append(a)
            else:
                print('--------------------------------------------------------')
                print(f'{a}')
                print(f'{r.status_code}')
                print('--------------------------------------------------------')
        except:
            if (line_count%10==0):
                print(line_count)
            continue

for i in range(len(url_list)):
    check(url_list[i])
print('\n\nWorked Proxy = {good_p}')
'''
#чтение из csv файла
import csv

with open('http.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        
        a=row[0][row[0].find("\"")+1:]#row[0].rfind("\"")]
        print(a)

        https_proxy = f'http://{a}'#f"{row[0]}"
        proxies = { 
              "http" : https_proxy, 
            }
        url = 'http://www.python.org'
        dat={
            'method': 'GET'
            #'mode': 'no-cors',
        }
        line_count +=1
        try:           
            r =  requests.post(url, params=dat, proxies=proxies, timeout=5)
            if (r.status_code == 200):
                print('--------------------------------------------------------')
                print(f'\t\t\t\t\t{a}')
                print(f'\t\t\t\t\t{r.status_code}')
                print('--------------------------------------------------------')
            else:
                print('--------------------------------------------------------')
                print(f'{a}')
                print(f'{r.status_code}')
                print('--------------------------------------------------------')
        except:
            if (line_count%10==0):
                print(line_count)
            continue
'''