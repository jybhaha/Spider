#encoding=utf-8
import cookielib
import urllib2
import urllib
from bs4 import BeautifulSoup
import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import re

searchPagesNum=100
Title = []
Link=[]
Size = []
FileNum=[]
ClickNum = []
Time = []
Torrent = []
Download = []
Finished = []

frame=DataFrame(columns=['Title','Size','FileNum','ClickNum','Time','Torrent','Download','Finished'])



def login():
    filename = 'cookie.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
    postdata = urllib.urlencode({
                'formhash':'fab5aaa7',
    			'username':'jyb_haha',
    			'password':'!85789821j',
                'invitecode':'',
                'submit':'submit'
    		})


    loginUrl = 'http://pt.zhixing.bjtu.edu.cn/user/login'

    opener.open(loginUrl,postdata)
    cookie.save(ignore_discard=True, ignore_expires=True)

def findpages():
    filename = 'cookie.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    for i in range(0,searchPagesNum):
        if i==0:
            gradeUrl = 'http://pt.zhixing.bjtu.edu.cn/search/movie/'
            result = opener.open(gradeUrl)
            searchData(i,result)
        elif i==1:
            continue
        else:
            gradeUrl = 'http://pt.zhixing.bjtu.edu.cn/search/movie/p%d'%i
            result = opener.open(gradeUrl)
            searchData(i,result)



def searchData(num,str):

    soup=BeautifulSoup(str)
    table=soup.find('table',attrs={'class':'torrenttable'})
    details=table.findAll('td')
    title=soup.findAll('a',attrs={'name':'title'})
    titlenum=len(title)

    for i in range(0,titlenum):
        Title.append(title[i].text)
        Link.append("http://pt.zhixing.bjtu.edu.cn/"+title[i].attrs['href'])
        Size.append(details[i*11+3].text)
        FileNum.append(details[i*11+4].text)
        ClickNum.append(details[i*11+5].text)
        Time.append(details[i*11+6].text)
        Torrent.append(details[i*11+7].text)
        Download.append(details[i*11+8].text)
        Finished.append(details[i*11+9].text)
    print"正在分析第：%d 页"%num

def savecsv():
    data=np.array([Title,Link,Size,FileNum,ClickNum,Time,Torrent,Download,Finished])
    frame=DataFrame(data.T,columns=['Title','Link','Size','FileNum','ClickNum','Time','Torrent','Download','Finished'])
    frame.to_csv('data//data.csv', encoding='utf-8', index=False)
    print'完成存储！！'

if __name__ == '__main__':
    login();
    findpages();
    savecsv()
    #frame=pd.read_csv('data//data.csv')

