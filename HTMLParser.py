#encoding:utf-8
'''
Created on 2016-7-21
python version 3.5
@author: holif
'''

from html.parser import HTMLParser
import urllib.request
import re

liststr = list()	#Create a list to hold the train information

class MyHTMLParser(HTMLParser):
    tempstr=str()
    def handle_starttag(self, tag, attrs):
        if tag=='tr':
            self.tempstr=''

    def handle_endtag(self, tag):
        if tag=='tr':
			 #Matching train types Filter the useless tr labels
            matchObj = re.match( r'G|D|K|T|Z|\d', self.tempstr)
            if matchObj:
                liststr.append(self.tempstr)

    def handle_data(self, data):
        if(data.isspace()==False):
            self.tempstr+=data+'\t'

url = 'http://qq.ip138.com/train/anhui/HeFei.htm'
data = urllib.request.urlopen(url).read()
data = data.decode('gb2312') #According to the web page code set data coding
par = MyHTMLParser()
par.feed(data)
for value in liststr:
    print(value)
print(liststr.__len__())