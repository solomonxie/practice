# -*- coding: utf-8 -*-
# 这是用来做黑板课的一个爬虫挑战题，第二关
# http://www.heibanke.com/lesson/crawler_ex01/
# 顺带一提 通关密码是：7

import urllib, urllib2
import re

def ReadNum(num=0):
    if num < 31 :
        postdata = urllib.urlencode({
            'username' : '测试',
            'password' : str(num),
        })
        req = urllib2.Request(
            url = 'http://www.heibanke.com/lesson/crawler_ex01/',
            data = postdata
        )
        page = urllib2.urlopen(req)
        #print page.read()
        pattern = re.compile(r'密码错误')
        match = re.findall(pattern, page.read())
        if not match :
            print '通关密码：' + str(num)
        else:
            num = num + 1
            ReadNum(num)

if __name__ == '__main__' :
    ReadNum()
