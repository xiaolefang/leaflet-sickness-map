# coding: utf-8
import urllib
import urllib.request
from urllib.request import quote, unquote 
import ssl
import datetime
import time

ssl._create_default_https_context = ssl._create_unverified_context
def getInfo(input1):
    url = input1
    urldata=quote(url,safe=";/?:@&=+$,", encoding="utf-8")
    req = urllib.request.Request(urldata, headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
    html = urllib.request.urlopen(req)
    return html.read()

while(True):
    guangdong_city_map=getInfo("https://superfxl.xyz/geoserver/cite/ows?service=WFS&version=1.3.0&request=GetFeature&typeName=cite:city_confirm_map&outputFormat=application/json")
    with open('geojson_guangdong_sickness.js','w',encoding="utf-8") as f:
        f.write("var geo_guangdong_city="+str(guangdong_city_map.decode().strip()))
    guangdong_city_point=getInfo("https://superfxl.xyz/geoserver/cite/ows?service=WFS&version=1.3.0&request=GetFeature&typeName=cite:guangdong_sick_point&outputFormat=application/json")
    with open('guangdong_sick_point.js','w',encoding="utf-8") as f:
        f.write("var guangdong_sick_point="+str(guangdong_city_point.decode().strip()))
    print("finish")
    print(time.ctime())
    time.sleep(3600*24)
    print(time.ctime())
    
