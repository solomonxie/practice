# -*- coding: utf-8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup

def readLinks() :
	url = 'http://www.cclw.net/Bible/LzzBible/img/list.html'
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html.read())
	print soup.a.get('href')

if __name__ == '__main__' :
	readLinks()