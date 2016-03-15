#coding:utf-8
from threading import Thread
import requests, re

def read(url):
    html = requests.get(url).text
    print ''.join(re.findall('<title>([^<>]+)</title>', html))

urls = 'http://www.baidu.com http://www.youku.com http://cn.bing.com'.split()
thlist = []

for u in urls:
    t = Thread(target=read, args=(u, ))
    t.start()
    thlist.append(t)

for sub in thlist:
    sub.join()