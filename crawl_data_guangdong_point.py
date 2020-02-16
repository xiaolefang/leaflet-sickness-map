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

ssl._create_default_https_context = ssl._create_unverified_context

while True:
    timestamp = time.time()
    engine = create_engine("mysql+mysqlconnector://root:19840318@149.129.112.41:3306/test") 
    sql = "select name from guangdong_sick_point"
    cur = engine.execute(sql)
    datas = list(cur.fetchall())
    nameList = []
    for data in datas:
        nameList.append(data[0])
    url = "https://m.mp.oeeee.com/data/uploads/PneumoniaArea/json/all_guangdong.json?v="+str(int(timestamp))+"000"
    print(url)
    urldata=quote(url,safe=";/?:@&=+$,", encoding="utf-8")
    req = urllib.request.Request(urldata, headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
    html = urllib.request.urlopen(req)
    hjson=json.loads(html.read())
    datas = hjson['data']
    for data in datas:
        districts = data['districtList']
        for district in districts:
            places = district['placeList']
            for place in places:
                place_name = place['place']
                if (place_name in nameList):
                    print('in')
                else:
                    print('not')
                    latlog = place['location']
                    latlog = latlog.replace(","," ")
                    source = place['source']
                    city_name = place['city']
                    district_name = place['district']
                    sql = "insert into guangdong_sick_point(id,name,source,city,district,pnt) values (null,'"+place_name+"','"+source+"','"+city_name+"','"+district_name+"',"+"POINTFROMTEXT('POINT("+latlog+")'))"
                    print(sql)
                    cur = engine.execute(sql)
    print(time.ctime())
    time.sleep(3600*24)
    print(time.ctime())
