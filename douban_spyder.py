import requests
import re
from bs4 import BeautifulSoup

comment_time=[]
score=[]
score_name=[]
for i in range(7):
    offset=i*20
    url = 'https://movie.douban.com/subject/27195020/collections?start=' + str(offset)
    headers = {
        'Cookie':'douban-fav-remind=1; _vwo_uuid_v2=DFC68B72C19D6A9ECFD52D6C47045F7C7|e5ee4292548f3f3fde8db0e49d0e5018; gr_user_id=d18a78de-d864-40d4-90a6-0f16892d0a06; __gads=ID=6c7a4c45556fab25:T=1562690329:S=ALNI_MZSRA3GRH7A3POXri7clpF9_vJTjg; __yadk_uid=Dlx4HSpcCAbnsQN8C2FvwJCl9efgjKwi; trc_cookie_storage=taboola%2520global%253Auser-id%3De99f0bff-5924-4934-920d-0ce008e27f3e-tuct480ba32; _ga=GA1.2.144684937.1559896462; bid=iKd33p1Oqo0; ll="108288"; viewed="5377415_26657923_26979890_20432061_25713576_1320347_1143843_25832015_4242172_3360791"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.14282; douban-profile-remind=1; __utmz=30149280.1583610627.109.105.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=30149280; dbcl2="142826962:w7nB8tivERk"; ck=KEGA; __utmc=223695111; __utmz=223695111.1583863406.44.43.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1583870212%2C%22https%3A%2F%2Fwww.douban.com%2Fsearch%3Fsource%3Dsuggest%26q%3Dchenqingling%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.144684937.1559896462.1583863223.1583870212.111; __utmb=30149280.0.10.1583870212; __utma=223695111.1658187889.1559896462.1583865449.1583870212.46; __utmb=223695111.0.10.1583870212; ap_v=0,6.0; _pk_id.100001.4cf6=72221cc646b1e816.1559896462.46.1583870595.1583865449.',
        'Host':'movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    r = requests.get(url, headers=headers)

    html=r.text
    soup = BeautifulSoup(html, 'lxml')
    sub=soup.find(attrs={'class':'sub_ins'})
    table=sub.find_all(name="table")
    
    for i in table:
        bi=i.find_all(class_="pl")
        for c in bi:
            #print(c.find(text=re.compile('20+')))
            #print(len(c.select('span')))
            #print(str(c.find(text=re.compile('20+'))))
            #print((c.select('span')[-1].attrs['title']))
            #print((c.select('span')[-1].attrs['class'])[0])
            comment_time.append(str(c.find(text=re.compile('20+')))[0:10])
            score.append((c.select('span')[-1].attrs['class'])[0])
            score_name.append((c.select('span')[-1].attrs['title']))