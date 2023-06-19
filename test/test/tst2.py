
from asyncio import constants
import requests
import asyncio

#request = requests.get('https://api.github.com')
#print(request.json()['current_user_url'])

from pyppeteer import launch
import logging
import re

import csv

with open('http.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        print(row[0])
        a=row[0][row[0].find("\"")+1:row[0].rfind("\"")]
        print(a)
        https_proxy = f'https://{a}'#f"{row[0]}"
        print(https_proxy)
        proxies = { 
              "https" : https_proxy, 
            }
        url = 'http://www.python.org/index.html'
        dat={
            'method': 'GET'
            #'mode': 'no-cors',
        }
        try:           
            r =  requests.post(url, params=dat, proxies=proxies, timeout=3)
            print(a)
            print(r.status_code)
            print()
        except:
            continue
        


exit()
# Allows you to intercept a request; must appear before
# your first page.goto()

dat={
    'method': 'POST',
    'mode': 'no-cors',
}
url = 'https://ww3.torlook.info'
   




#page.on( 'request', lambda req: ( data = {'method': 'POST','postData': dat}; req.continue(data)))



r =  requests.post(url, params=dat, proxies=proxies)

print(r.url)
print(r.text)
print(r.url)
