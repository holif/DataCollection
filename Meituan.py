#encoding:utf-8
'''
Created on 2016-7-22
python version 3.5
@author: holif
'''
from html.parser import HTMLParser
import re
import urllib.request

import xlwt
import time

#create a list for acquisition of business information
arraystr = list()

#parse web source
class MyHTMLParser(HTMLParser):
    tempstr = str()
    divsum = int()
    def handle_starttag(self, tag, attrs):
        if tag=='div':
            for attr,value in attrs:
                if attr=='class' and value.find('poi-tile-nodeal')!=-1:
                    self.tempstr=''
                    self.divsum = 0

    def handle_data(self, data):
        if(data.isspace()==False):
            data = data.replace('·', '·')
            if  data=='¥':
                if '¥' not in self.tempstr:
                    self.tempstr+='无' +'\t'
                self.tempstr+=data
            elif data=='¥':
                if '¥' not in self.tempstr:
                    self.tempstr+='无' +'\t'
                self.tempstr+='¥'
            elif data=='人评价':
                self.tempstr=self.tempstr[0:-1]+data+'\t'
            elif data=='人均 ':
                self.tempstr+='人均'
            elif data[0]=='起':
                self.tempstr=self.tempstr[0:-1]+'起'
            else:
                self.tempstr+=data+'\t'
        
    def handle_endtag(self, tag):
        if tag=='div':
            self.divsum+=1
            if self.divsum==6:
                if (self.tempstr.find('¥'))!=-1:
                    if (re.split(r'\t', self.tempstr).__len__())==5:
                        teststr = str()
                        flg = 0
                        for stmp in re.split(r'\t',self.tempstr):
                            if flg==2:
                                teststr+='无位置信息'+'\t'
                            teststr+=stmp+'\t'
                            flg+=1
                        self.tempstr=teststr
                    if (re.split(r'\t', self.tempstr).__len__())==6:
                        arraystr.append(self.tempstr)
                        self.divsum=0
                        self.tempstr=''

#get online url cities
class GetCityUrl(HTMLParser):
    part = ('gaevent','changecity/build')
    urldic = {}
    def handle_starttag(self, tag, attrs):
        if tag=='a' and (self.part in attrs):
            for att,value in attrs:
                if att=='href':
                    self.urldic.__setitem__(value, value+'/category/meishi/all/rating')
                    
    def getUrl(self):
        return self.urldic

#get other pager url
class GetPages(HTMLParser):
    pagelist = list()
    temphref = str()
    flg = 0
    initurl = str()
    def setInitUrl(self,url):
        self.initurl = url
    def handle_starttag(self, tag, attrs):
        if tag=='a':
            for attr,value in attrs:
                if attr=='href' and ('page' in value):
                    self.temphref = self.initurl + value
                    if self.temphref not in self.pagelist:
                        self.pagelist.append(self.temphref)

    def getList(self):
        return self.pagelist

#collect web source
def getHtml(url):
    headers = ('User-Agent',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    htmldata = opener.open(url).read()
    htmldata=htmldata.decode('utf-8')
    return htmldata

#save to Excel
def SaveExcel(listdata):
    head=['商家名','类型','地理位置','评论人数','均价','最低价格']
    wbk=xlwt.Workbook()
    sheet1=wbk.add_sheet("sheet1")
    ii=0
    for testhand in head:
        sheet1.write(0,ii,testhand)
        ii+=1
    i=1
    j=0
    for stt in listdata:
        j=0
        lis = re.split(r'\t',stt)
        for ls in lis:
            sheet1.write(i,j,ls)
            j=j+1
        i+=1
    wbk.save('e:/test3.xls')

par = GetCityUrl()
#Choose city page in MeiTuan
par.feed(getHtml('http://www.meituan.com/index/changecity/initiative'))
urldic = par.getUrl()

par = MyHTMLParser()

print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))

ffwait=1

for url in urldic:
    data = getHtml(urldic.get(url))
    
    getpage = GetPages()
    getpage.setInitUrl(url)
    getpage.feed(data)
    pageurllist = getpage.getList()
 
    par.feed(data)
    for urltemp in pageurllist:
        par.feed(getHtml(urltemp))

    if ffwait ==4:#collect four city data
        break;
    ffwait+=1

SaveExcel(arraystr)
print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
print('Done')