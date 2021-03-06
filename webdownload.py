# -*- coding: utf-8 -*-
import os
import re
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
​
overlap=[]
url = 'https://www.kamis.or.kr/customer/trend/trade/weekly.do?'  #반복되는 곳 사이트 몸통
site = 'https://www.kamis.or.kr/'   #가져올 사이트 앞부분
rec = "/customer/trend/trade/weekly.do?" #반복되는 부분 뒷부분
dl = "/customer/board/board_file.do?"   #클릭해서 다운 받는 부분
​
def get_download(url, fname, directory):
   try:
       os.chdir(directory)
       request.urlretrieve(url, fname)
       print('다운로드 완료\n')
   except HTTPError as e:
       print('error')
       return
​
def downSearch(getDLATag):
   for getDLLink in getDLATag:
       try:
           if dl in getDLLink.get('href'):
               print("다운로드 링크 : {}".format(site) + getDLLink.get('href'))
               accessDLUrl = site + getDLLink.get('href')
               fileOriginalNM = re.sub('<.+?>', '', str(getDLLink), 0).strip().replace('_', ' ')
               fileNM = "[KAMIS주간동향] " + fileOriginalNM
               path = "D:\\KAMIS\\"
               if os.path.isfile(path + fileNM):
                   print("다운로드 실패 : 동일 파일 존재\n")
               else:
                   get_download(accessDLUrl, fileNM, path)
       except:pass
​
def Search(getA):
   for getLink in getA:
       data = getLink.get('href')
       try:
           if rec in getLink.get("href"):
               if len(data) >= 100 and data not in overlap:
                   overlap.append(data)
                   accessUrl = site + getLink.get("href")
                   r = requests.get(accessUrl)
                   soup = BeautifulSoup(r.text, "html.parser")
                   getDLATag = soup.find_all("a")
                   downSearch(getDLATag)
​
               elif len(data) >= 85 and data not in overlap:
                   overlap.append(data)
                   accessUrl = site + getLink.get("href")
                   r = requests.get(accessUrl)
                   soup = BeautifulSoup(r.text, "html.parser")
                   getDLATag = soup.find_all("a")
                   Search(getDLATag)
                   # Search(getDLATag,depth+1)
       except:pass
​
# request 모듈을 사용하여 웹 페이지의 내용을 가져온다
r = requests.get(url)
print("KAMIS 자료실 요청 : ", r)
​
# beautiful soup 초기화
soup = BeautifulSoup(r.text, "html.parser")
# 태그로 찾기 (모든 항목)
getA = soup.find_all("a")
Search(getA)
