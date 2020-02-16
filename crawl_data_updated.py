# coding: utf-8
import urllib
import json
import urllib.request
from urllib.request import quote, unquote 
import pymysql
import ssl
import bs4
import datetime
from sqlalchemy import create_engine
import time

while True:
    engine = create_engine("mysql+mysqlconnector://root:19840318@149.129.112.41:3306/test")  
    today=datetime.date.today()
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "https://3g.dxy.cn/newh5/view/pneumonia?from=singlemessage&isappinstalled=0"
    urldata=quote(url,safe=";/?:@&=+$,", encoding="utf-8")
    req = urllib.request.Request(urldata, headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
    html = urllib.request.urlopen(req)
    #print(html.read().decode('utf-8'))
    soup = bs4.BeautifulSoup(html.read().decode('utf-8'),"html.parser")
    elems = soup.select("script[id='getAreaStat']")
    contents = str(elems[0])
    c = contents.split("window.getAreaStat = ",1)[1]
    c1 = c.split("}catch(e){}</script>",1)[0]
    hjson=json.loads(c1)
    num = 0
    for province in hjson:
        if province['provinceName']=='广东省':
            break
        num = num + 1
    guangdong = hjson[num]['cities']
    print(guangdong)
    num = 0
    for city in guangdong:
        cityName = (city['cityName'])
        confirmedCount =  (city['confirmedCount'])
        crueCount = (city['curedCount'])
        sql = "insert into city_confirm_count(id,city_name,value,confirmed_date,crue_vale) values (null,'"+cityName+"',"+str(confirmedCount)+",'"+str(today)+"',"+str(crueCount)+")"
        print(sql)
        cur = engine.execute(sql)
        sql = "update city_confirm_map set value="+str(confirmedCount)+", crue_value="+str(crueCount)+" where city_name like '%"+cityName+"%'"
        print(sql)
        cur = engine.execute(sql)
    print(time.ctime())
    time.sleep(3600*24)
    print(time.ctime())
