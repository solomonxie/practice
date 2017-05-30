#coding:utf-8

import requests, re

prx = {}
prx = {'http':'52.79.57.12:3128'}

r = requests.get('http://ip.cn', proxies=prx, timeout=5)

for item in re.findall('<code>[^<>]+</code>', r.text):
    print item
