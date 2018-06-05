# -*- coding: utf-8 -*-
# 这是用来做黑板课的一个爬虫挑战题，第一关
# http://www.heibanke.com/lesson/crawler_ex00/
# 顺带说一句 递归后，最终的答案是83679

import urllib2
import re

def ReadNum(num=''):
    url = 'http://www.heibanke.com/lesson/crawler_ex00/' + num
    res = urllib2.urlopen(url)
    #print res.read()
    pattern = re.compile(r'<h3.*?>.*?(\d{5}).*?</h3>')
    match = re.findall(pattern, res.read())
    for m in match:
        if m :
            print m
            ReadNum(m)

if __name__ == '__main__' :
    ReadNum()
