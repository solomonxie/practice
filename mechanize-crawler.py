# coding:utf-8
import mechanize

url = 'http://www.zhihu.com'

br = mechanize.Browser()
br.open(url)

for link in br.links():
    print link
