import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import random 

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
]
data=pd.DataFrame(columns=['ip','port','location','type','http','before','date','when','speed','connect'])

ii=-1
for page in range(1,6):
    start_url='https://www.xicidaili.com/nn/'+str(page)
	headers = {
    'User-Agent': random.choice(user_agent_list)
	}
    html=requests.get(start_url,headers=headers)
    soup=BeautifulSoup(html.text,'lxml')
    ip_list=soup.find(attrs={'id':'ip_list'})
    ip_all=ip_list.select('tr')
    for i in range(1,101):
        speed=ip_all[i].find_all(class_='country')[2].div.attrs['title']
        connect=ip_all[i].find_all(class_='country')[3].div.attrs['title']
        info=ip_all[i].text.split()
        info.append(speed)
        info.append(connect)
        ii=ii+1
        if len(info)==10:
            data.loc[ii]=info
			
			