import requests
import re
from bs4 import BeautifulSoup
import random

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
]

s=requests.Session()
url='https://accounts.douban.com/j/mobile/login/basic'
data={
    'ck':'',
    'name':'****',
    'password':'****',
    'ticket':''
}
headers = {
    'User-Agent': random.choice(user_agent_list)
}
r = s.post(url, data=data,headers=headers)

comment_time=[]
score=[]
score_name=[]
for i in range(7):
    offset=i*20
	url = 'https://movie.douban.com/subject/27195020/collections?start=' + str(offset)
	hh=s.get(url,headers=headers)
	html=hh.text
	soup = BeautifulSoup(html, 'lxml')
	sub=soup.find(attrs={'class':'sub_ins'})
	table=sub.find_all(name="table")
	for i in table:
		bi=i.find_all(class_="pl")
		c=bi[0]
		if c.span is not None:
			#print(str(c.find(text=re.compile('20+'))))
			#print((c.select('span')[-1].attrs['title']))
			#print((c.select('span')[-1].attrs['class'])[0])
			comment_time.append(str(c.find(text=re.compile('20+')))[0:10])
			score.append((c.select('span')[-1].attrs['class'])[0])
			score_name.append((c.select('span')[-1].attrs['title']))							

spider_={"comment_time":comment_time,"score":score,"score_name":score_name}
data=pd.DataFrame(spider,columns=['comment_time','score','score_name'])


from pymongo import MongoClient
client = MongoClient(host='localhost',port=27017)
db = client['douban_score']
collection=db.douban
for i in range(len(data)):
    result=collection.insert_one(dict(data.iloc[i]))

results = collection.find({'comment_time': '2020-03-15'})
for result in results:
    print(result)
