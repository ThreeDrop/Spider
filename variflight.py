import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.variflight.com/sitemap/flight?AE71649A58c77='
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
r = requests.get(url, headers=headers)
html=r.text
soup = BeautifulSoup(html, 'lxml')
sub=soup.find(attrs={'id':'wrap'})
table=sub.find_all(class_="innerRow")
link_s='https://www.variflight.com' 
flight_name=[]
flight_dep=[]
flight_arr=[]
flight_link=[]
for i in table:   
	aaa=i.select('a')
	for bb in aaa:
		#print(bb.string)
		flight_link.append(bb.attrs['href'])
		flight_name.append(bb.string)
		flight_dep.append(bb.attrs['depcode'])
		flight_arr.append(bb.attrs['arrcode'])
		
flight_dep_time=[]
flight_arr_time=[]
flight_dep_real=[]
flight_arr_real=[]
flight_from=[]
flight_to=[]
flight_status=[]
for i in flight_link:
	url = link_s+i
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
	}
	r = requests.get(url, headers=headers)
	html=r.text
	soup = BeautifulSoup(html, 'lxml')

	airport=[]
	flight_number=[]
	flight_company=[]
	aaa=soup.find_all(attrs={'class':'li_com'})
	for i in aaa:
		#flight_number.append(i.b) # flight number & company
		for kk in i.select('b a'):
			flight_company.append(kk.find(text=re.compile('\D+航+\D*')))
			flight_number.append(kk.find(text=re.compile('\w+\d+')))
	
	for i in aaa:
		kkk=i.find_all('span')
		flight_dep_time.append(kkk[1].text.strip())
		flight_dep_real.append(kkk[2].text.strip())
		flight_from.append(kkk[3].text.strip())
		flight_arr_time.append(kkk[4].text.strip())
		flight_arr_real.append(kkk[5].text.strip())
		flight_to.append(kkk[6].text.strip())
		flight_status.append(kkk[8].text.strip())
		
final={"Airport":airport,"flightNO":flight_number,"flight_company":flight_company,
	  "flight_dep_time":flight_dep_time,"flight_dep_real":flight_dep_real,"flight_arr_time":flight_arr_time,
	  "flight_arr_real":flight_arr_real,"flight_from":flight_from,"flight_to":flight_to,"flight_status":flight_status}
data=pd.DataFrame(final,columns=['Airport','flightNO','flight_company','flight_dep_time','flight_dep_real','flight_arr_time',
								 'flight_arr_real','flight_from','flight_to','flight_status'])        

    