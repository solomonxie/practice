# coding:utf-8
import urllib, urllib2
import cookielib
import json

def test_json():
	url = 'https://api.douban.com/v2/book/1220562'
	html = urllib2.urlopen(url)
	#print html.read()
	# 读取json格式的返回值
	data_json = json.loads(html.read())
	print type(data_json)
	print data_json

def login_post():
	url = 'https://accounts.douban.com/login'
	data = urllib.urlencode({
		'form_email' : '', 
		'form_password' : '', 
		'source' : 'movie'
	})
	headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
	req = urllib2.Request(url, data, headers)
	page = urllib2.urlopen(req).read()
	#print html
	f = open('douban-after-login.html','w')
	f.write(page)
	f.close()
	print '成功生成post提交后页面的代码'

def store_cookie_with_variables():
	url = 'https://movie.douban.com'
	cookie = cookielib.CookieJar()
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)
	response = opener.open(url)
	for item in cookie:
		print item.name + ' : ' + item.value

def logoin_with_cookie():
	url = 'http://movie.douban.com/mine'
	# 将cookie 保存到文件中
	cookie = cookielib.MozillaCookieJar('cookie.txt')
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)
	response = opener.open(url)
	cookie.save(ignore_discard=True, ignore_expires=True)

	# 读取txt文件中的cookie
	cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
	opener = urllib2.HTTPCookieProcessor(cookie)
	handler = urllib2.HTTPCookieProcessor(cookie)
	opener = urllib2.build_opener(handler)

	# 发出登录请求并返回网页
	data = urllib.urlencode({
		#'form_email' : '', 
		#'form_password' : ''
	})
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
	req = urllib2.Request(url, data, headers)
	page = opener.open(req).read()

	# 将读取到的网页写入html文件
	f = open('douban-after-login.html', 'w')
	f.write(page)
	f.close()

if __name__ == '__main__':
	logoin_with_cookie()