# -*- coding: utf-8 -*-
'''
	# Title : 网络爬虫工具函数
	# Author: Solomon Xie
	# Usage : 
	# Notes : 
	# Update: 
'''
# === 必备模块 ===
import urllib2, urllib, re
from bs4 import BeautifulSoup

def bsGet(tag, css='', withTxt='', withKey='', attri='', more=False):
	'''
	# Function : 根据搜索条件,返回搜索结果的字符串(Unicode格式！！)
	# Params   : tag=BeautifulSoup返回的Tag对象,css=按css选择器搜索,withTxt=按标签内文本搜索,more=是否返回所有结果,attri=是否返回属性值如果不是则返回标签文本内容
	# Notes    : 1.不管css和withTxt有多少个，attri只能有一个，不可能css配一个并且withTxt也配一个！那样就太复杂了
				   如果attri为空，则取标签包含的内容，如果有attri，则取标签的相应属性值
				 2.withKey指的是通过Tag.find_all()函数来查找，返回的是Tags；这和withTxt的方式大不同。
				 3.如果a=[]的话，a += '' 仍是[]，而不是['']
				 4.Tag.select(xx)不支持参数为空
				 5.Tag.find_all('')时，会返回一大堆空字符串结果，即内容为空的标签的内容。
				 6.Tag.find_all(text='xx')时候，返回的不是Tag而是String，而且不是Unicode的字符串，而是普通编码！
				 7.本函数用法：css/withTxt/withKey可以是字符串或列表，
				   三参数时or的关系可组合应用，但是withTxt不能和attri合用。因为withTxt只返回字符串没有属性值。
				   withKey，
				 8.本函数如果有多个结果，则返回列表；如果只有一个结果，返回字符串；如果没有结果返回空字符串。
				   多重查询即是这样，目的是增加搜索条件，也就增加机率获取信息。多重条件直接是多选关系，而不是限制关系。
				 9.如果有attri参数，则返回所有结果Tag的属性值；如果没有，则返回所有结果Tag的文本内容。
	'''
	# print 'css=%s, withTxt=%s, withKey=%s, attri=%s, more=%s' %(repr(css),repr(withTxt),repr(withKey),repr(attri),repr(more)) # 测试用
	retr = [] # 待返回的列表对象
	# 不管css和withTxt是列表、字符、空，统一化为列表进行循环，方便处理
	for c in css if isinstance(css, list) else [css]: 
		try:
			result = tag.select(c) if css else ''
			if attri: retr += [t[attri]                 for t in result] if result else ''
			else:     retr += [t.get_text(strip=True)   for t in result] if result else ''
		except: continue # print 'Failed on analyzing "%s"' %str(css) # 测试用
	for wt in withTxt if isinstance(withTxt, list) else [withTxt]:
		if not wt: break
		try:
			wt = unicode(wt, 'utf-8') # 符合“全程Unicode”规则
			result = tag.find_all(text=re.compile(wt))
			retr += [s.replace(wt, '') for s in result] if result else ''
		except: continue # print 'Failed on analyzing "%s"' %str(css) # 测试用
	# for wk in withKey if isinstance(withKey, list) else [withKey]:
	# 	try:
	# 		result = tag.find_all(wk)
	# 		if attri: retr += [t[attri] for t in result] if result else ''
	# 		else:     retr += [t.string for t in result] if result else ''
	# 	except: continue # print 'Failed on analyzing "%s"' %str(withKey) # 测试用
	# print len(retr) # 测试用
	if not retr : return u''
	return retr[0] if not more else retr
def TEST_bsGet():
	# ============ Start -> 测试块 ================
	src = open('./Templates/Zhilian-list-page-sm1.html', 'r')
	# src = urllib.urlopen('http://sou.zhaopin.com/jobs/searchresult.ashx')
	html_doc = unicode(src.read(),'utf-8')
	soup = BeautifulSoup(html_doc, 'html5lib')
	rows = soup.select('[class$=newlist]')
	# test for -> Call the target function --------------->>>>>>>>>>>>>>
	cs = bsGet(rows[2], css='[class*=zwmc]')
	at = bsGet(rows[2], css='input', attri='value')
	wt = bsGet(rows[2], withTxt='地点：')
	# wk = bsGet(rows[2], withKey='') # 暂时没想好withKey要放在哪用
	mu = bsGet(rows[2], css=['td[class=gxsj]', 'dl p'], attri='class')
	mr = bsGet(soup, css=['td[class=gxsj]', 'dl p'], withTxt='公司性质：', more=True)
	print 'CSS:', cs
	print 'Attribute:', at
	print 'WithTxt:', wt
	# print 'WithKey:', wk
	print 'Multi-Search:', mu
	print mr
	# test for -> charset of return infos by different methods --------------->>>>>>>>>>>>>>
	print 'CSS feedback an unicode string: ',type(cs) == type(u'')
	print 'Attribute feedback an unicode string: ',type(at) == type(u'')
	print 'WithTxt feedback an unicode string: ',type(wt) == type(u'')
	# print 'WithKey feedback an unicode string: ',type(wk) == type(u'')
	print 'Multi-Search feedback an unicode string: ',type(mu) == type(u'')
	# ============ End   -> 测试块  ==============

def webPageSourceCode(baseUrl='', urlParams={}, method='GET', antiRobot={}):
	'''	
	# Function: 抽象出来模块化的网页源码获取函数：传入网址及必要信息,返回源码等相关信息
	# Params  : baseUrl=准备抓取的网址,method=GET | POST,urlParams=URL中的参数,antiRobot=爬虫伪装方式
	'''
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
	# === Post方式获取源码 ===
	# req = urllib2.Request(baseUrl, urllib.urlencode(urlParams), headers)
	# src = urllib2.urlopen(req)
	# === Get 方式获取源码 ===
	if urlParams : fullUrl = '%s?%s' %(baseUrl, urllib.urlencode(urlParams))
	else : fullUrl = baseUrl
	# fullUrl = '%s?%s' %(baseUrl, urllib.urlencode(urlParams)) if urlParams else baseUrl
	print 'Connecting this web page: %s' %fullUrl
	try: 
		src = urllib2.urlopen(fullUrl)
		trueUrl = src.geturl() # 获取真实Url网址
		# print 'Processing Url: %s' %fullUrl # 测试用。显示正在处理的网页
		# === 本地方式读取源码 ===
		# src = open('./Templates/test-Zhilian-list-page-sm0.html', 'r') # 测试用,0.001秒
		html_doc = unicode(src.read(),'utf-8') # 用时1秒。
		print 'Succeeded loading this web page.'
		# === 函数返回网页源码,及必要信息 ===
		return {'html':html_doc,'fullUrl':fullUrl,'trueUrl':trueUrl}
	except Exception as e:
		print 'No resources found : %s\nThe error internet resource is :' %fullUrl
		print e
		return {'html':'','fullUrl':'','trueUrl':''}
def TEST_webPageSourceCode():
	pass

def txtLog(data, filename=''):
	'''
	# Function: 将数据输出为txt文件格式。
	'''
	output = '\n'.join(data).encode('utf-8')
	with open(filename, 'w') as f:
		f.write(output)

# 计算时间
def timeup(foo, attr1, attr2, attr3):
	import time
	start = time.clock()
	val = foo(attr1, attr2, attr3)
	end = time.clock()
	timeuse = end-start
	print '=== Spend %d sec. on running %s()\n' %(timeuse, foo.__name__)
	return val

def urlAnalyse(url=''):
	'''
	# Function : 分析拆解URL,并返回相应的数据
	# Examples : 如URL为`http://sou.zhaopin.com/jobs/searchresult.ashx?p=13sm=0&kt=0#body`
				 则返回值为：{'scheme':'http','netloc':'sou.zhaopin.com','path':'/jobs/searchresult.ashx',
				 'params':'','query':'p=13sm=0&kt=0','fragment'='body','values':{['p':'13','sm':'0','kt':'0']}
	'''
	import urlparse
	oo = urlparse.urlparse(url)
	return {
		'scheme'   : oo[0], # 协议。如'http'/'https'/'ftp'等
		'netloc'   : oo[1], # 网址。如'www.baidu.com'/'sou.zhaopin.com'等
		'subloc'   : oo[1].split('.'), # 域名块,list列表。如'www.baidu.com'就会被解析为['www','baidu','com']
		'path'     : oo[2], # 路径。如'/jobs/2015/123124.html'
		'file'     : oo[2].split('/')[-1],                # 文件全称。如'searchresult.ashx'
		'filename' : oo[2].split('/')[-1].split('.')[0],  # 文件名  。如'searchresult'
		'params'   : oo[3], # ...
		'query'    : oo[4], # 参数。如'p=13sm=0&kt=0'
		'fragment' : oo[5], # 分片。如'#title'
		'quote'    : urllib.quote(url),   # 将url转为带%符号的
		'unquote'  : urllib.unquote(url), # 将带%符号的转为原url（含中文的话就复杂了,需要双重unquote或字符转编码）
		'values'   : dict([
						(key,value[0]) for key, value in urlparse.parse_qs(oo.query).items()
					])     # 参数值,字典形式。如{['key':'关键词','city':'北京']}
	}



# ===============================================================================================
if __name__ == '__main__':
	TEST_bsGet()