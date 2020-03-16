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


url = 'https://www.msra.cn/zh-cn/jobs?language=chinese&job-type=internship'
headers = {
	'User-Agent': random.choice(user_agent_list)

}
r = requests.get(url, headers=headers)
html=r.text
soup = BeautifulSoup(html, 'lxml')
sub=soup.find(class_='recruit_table')
table=sub.find_all(class_="msr-table-schedule")
intern_name=[]
intern_city=[]
intern_link=[]
intern_group=[]
intern_demand=[]
for i in range(5):
    intern_name.append(table[0].select('a')[2*i].text)
    intern_link.append(table[0].select('tr')[2*i].select('a')[0].attrs['href'])
    intern_city.append(table[0].td.td.text)
    intern_group.append(table[0].select('tr')[2*i].select('td')[0].select('td')[1].text)
    intern_demand.append(table[0].select('tr')[2*i].select('td')[0].select('td')[2].text)
    
url = 'https://www.msra.cn/zh-cn/jobs?pg={}&language=chinese&job-type=internship%2F'
headers = {
	'User-Agent': random.choice(user_agent_list)

}

for page in range(2,10):
    headers = {
        'User-Agent': random.choice(user_agent_list)
    }
    r = requests.get(url.format(page), headers=headers)
    html=r.text
    soup = BeautifulSoup(html, 'lxml')
    sub=soup.find(class_='recruit_table')
    table=sub.find_all(class_="msr-table-schedule")
    for i in range(5):
        intern_name.append(table[0].select('a')[2*i].text)
        intern_link.append(table[0].select('tr')[2*i].select('a')[0].attrs['href'])
        intern_city.append(table[0].td.td.text)
        intern_group.append(table[0].select('tr')[2*i].select('td')[0].select('td')[1].text)
        if len(table[0].select('tr')[2*i].select('td')[0].select('td'))>2:
            intern_demand.append(table[0].select('tr')[2*i].select('td')[0].select('td')[2].text)
        else:
            intern_demand.append('unknown')

for i in range(45):
    link=intern_link[i]
    r = requests.get(link,headers=headers)
    html=r.text
    soup = BeautifulSoup(html, 'lxml')
    
    recruit=soup.find(class_='recruit_des remove_style')
    intern_period.append(recruit.find(text=re.compile('.*月')))
    
final={"name":intern_name,"link":intern_link,"city":intern_city,"group":intern_group,"demand":intern_demand,"period":intern_period}
data=pd.DataFrame(final,columns=['name','link','city','group','demand','period'])   