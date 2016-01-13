# coding:utf-8

import requests
from bs4 import BeautifulSoup
from WebspiderToolbox import *

if __name__ == '__main__':
	for i in range(1,11):
		webTarget = webPageSourceCode('http://www.xiami.com/space/lib-artist/u/38443336/page/%d'%i)
		html = webTarget.get('html')
		print len(html)
		soup = BeautifulSoup(html, 'html5lib')
		with open('artist-%d.html'%i, 'w') as f:
			f.write(soup.prettify('utf-8'))
		print 'done.'