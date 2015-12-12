# -*- coding: utf-8 -*-
'''
	# Title : 智联招聘信息爬虫 - 搜索列表部分
	# Author: Solomon Xie
	# Usage : A practise with python: 
				get job information from a chinese job seeking web Zhilian.com.
				This little project is auctually a web crawler, 
				which uses some techniques such as BeautifulSoup and urllib2 and so on.
	# Notes : 切记：全文操作除了输出外，所有和BeautifulSoup相关的变量存储和被操作的全是Unicode格式！否则绝对出问题
	# Update: v1.0 已经能够准确获取智联招聘搜索结果列表的职位信息了
'''
# 必备模块
import urllib2, urllib, re
from bs4 import BeautifulSoup
# 小工具用模块
import time, urlparse
# 如果要做一些bs4专有类型的判断就必须导入
# import bs4 

def ZhilianSearchJoblist(keyword='数据', assignPage=1, scope=0):
	'''
	# Function: 向智联招聘提交搜索信息，并获取智联搜索页的所有职位信息
	# Params : keyword=搜索关键词，assignPage=页码
	'''
	# 暂时手动制定总的读取页数
	total_pages = 90
	if   scope==0 : print '=========== Tring processing General  Search List Page %d ==========='%assignPage
	elif scope==1 : print '----------- Tring processing Company  Search List Page %d -----------'%assignPage
	elif scope==2 : print '----------- Tring processing Position Search List Page %d -----------'%assignPage
	# === 编制URL参数 ===
	urlParams = {
		'kw' : keyword, # 搜索关键词
		'sm' : 0, # 显示方式代码： 列表是'0',详细是'1'。显示不同源码也不同，尽量选列表模式，源码更好解析。
		'jl' : '北京', # 搜索城市：'北京'，多项用'+'连接(URL编码为%2B)
		#'bj' : '', # 职位类别代码：互联网产品/运营管理 的代码为 '160200'，多项用'%3B'连接(URL编码的%)
		#'in' : '', # 行业代码：多项用';'连接(URL编码为%3B)
		'kt' : scope, # 关键词搜索范围：全文'0' | 公司名'1' | 职位名'2'
		'isadv' : 0, # 是否高级搜索：快速搜索'0' | 高级搜索'1'
		# 'isfilter' : 1, # 是不是筛选器： '0' | '1'
		# 'ispts' : '', # 通常为 '1'
		#'sj' : '', # 职位子类别代码：
		# 'gc' : '5号', # 地铁线路： '5号'
		# 'ga' : '立水桥', # 地名或地铁站名： '天通苑南' 、 '小汤山'
		# 'sb' : 0, # 排序方式代码：默认排序是'0',相关度排序是'1', 首发日排序是'2'
		#'fjt' : '10000', # 职位标签 五险一金'10000' 年底双薪'10001' 绩效奖金'10002' 等等
		# 'sf' : -1, # 月薪底线：'8001' 不限是'-1'
		# 'st' : -1, # 月薪上限：'10000' 不限是'-1'
		# 'ct' : -1, # 公司性质代码
		# 'el' : -1, # 学历代码
		# 'we' : -1, # 工作经验代码
		# 'et' : -1, # 职位类型代码：兼职'1' 全职'2' 实习'4'
		# 'pd' : -1, # 发布时间(天数)：一周是'7'，一个月是'30'，不限是'-1'
		'p' : assignPage, # 页码，超出总页码时，则会显示最后一页
		#'gr' : '', # 
		# 're' : '2015', # 这个限制了搜素数量，但是其实也不是按年份搜索
		'sg' : '', # 即全网唯一标示符——GUID
		#'' : '' #
	}
	# === 获取网页源码 ===
	webTarget = webPageSourceCode('http://sou.zhaopin.com/jobs/searchresult.ashx', urlParams)
	if not webTarget : return '' # 如果没有获取到网络信息 则退出 # 不过目前这一句的逻辑是否正确还没想通-_-!
	# === BeautifulSoup解析源码，也是最花时间的，解析器不对则会造成7秒/页面 ===
	soup = BeautifulSoup(webTarget['html'], 'html5lib')
	# === 获取搜索结果的数量 ===
	total_results = int(bsText(soup, pattr='[class$=search_yx_tj] em'))
	if total_results == 0: return 0 # 如果当前页面没有结果，则不进行处理了。
	print 'There are %d results found as total.' %total_results
	'''
	# === 获取全网唯一ID，即url中的sg参数 ===
	tags = soup.select('#guid')
	guid = tags[0]['value'] if len(tags)  else ''
	print 'The "guid" is %s.' %guid
	'''
	# === 获取真实页码 ===
	truePage = bsText(soup, pattr='[class*="pagesDown"] a[class*="current"]')
	truePage = int(truePage) if truePage else 1 # 如果结果少于1页，则不会有任何结果
	# === 获取信息条目 ===
	records = soup.select('[class$=newlist]')
	print '=== Detected %d Job Information' %len(records)
	if len(records):
		data = []
		for row in records:
			data += [
				bsText(row, pattr='[class$=zwmc]'),     # 职位名称
				bsText(row, pattr='[class$=gsmc]'),     # 公司名称
				bsText(row, pattr='[class$=fk_lv]'),    # 反馈比率
				bsText(row, pattr={'t':u'经验：'}),     # 工作经验
				bsText(row, pattr={'t':u'学历：'}),     # 学历背景
				bsText(row, pattr={'t':u'公司性质：'}), # 公司性质
				bsText(row, pattr={'t':u'公司规模：'}), # 公司规模
				bsText(row, pattr={'t':u'岗位职责：'}), # 岗位职责
				bsText(row, pattr=['[class$=zwyx]', {'t':u'职位月薪：'}]),   # 职位月薪
				bsText(row, pattr=['[class$=gzdd]', {'t':u'地点：'}]),       # 工作地点
				bsText(row, pattr=['[class$=gxsj]', 'dl p']),                # 更新时间
				bsAttrs(row,pattr=['[class$=zwmc] a[href^="http"]','href']), # 招聘网址
				bsAttrs(row,pattr=['[class$=gsmc] a[href^="http"]','href'])  # 企业网址
			]
			# === 跳转并解析职位信息页面 ===
			jobUrl = bsAttrs(row,['[class$=zwmc] a[href^="http"]','href'])
			if jobUrl : ZhilianJobPage(jobUrl)
			else      : print 'Failed on retrieving URL of the job: %s' %data[0]
			'''
			# === 跳转并解析企业信息页面 ===
			# 递归本函数，用企业名搜索其下所有招聘信息。
			# 但是会有问题就是，如果`识别重复`方面没有做好，这里就会形成无限循环。
			# 可以想到的笨方法就是，先取得所有相关的企业名称和链接，然后再用函数把它读取出来，循环生成。
			# ZhilianSearchJoblist(data[1].encode('utf-8'), 1, scope=3) 
			'''
		# 输出结果：暂时用txt文件输出，后面会用到数据库
		with open('./data/log-search-scope%d-page%d.txt' %(scope,truePage), 'w') as f:
			f.write('\n%s\n' %' , '.join(data).encode('utf-8') + '='*40)
		print '%sDone of retrieving page %d' %('_'*80, truePage)
	'''
		# === 递归调用函数自身，循环读取下一页 ===
		# 循环读取每一页的信息
		# 智联招聘一般全网同时会有100,000个职位
		# 但是都不超过90个页面，一页有40个，所以顶多只能获取3600个
		# 另外，如果页码超过现有的，则会仍显示一些招聘信息，但是都是重复的。
		# 唯一不同是，上方会显示“共0个职位满足条件”
		# 如果真实的页码并没有指定页码那么多，就代表搜索到头了。
		# >>>
	'''
	if truePage < total_pages and truePage == assignPage:
		ZhilianSearchJoblist(keyword, truePage+1)
	else: print '-'*50 + 'Reached the end of records.'

def ZhilianJobPage(detailUrl=''):
	'''	
	# Function: 获取智联招聘的职位详细信息页面
	# Params  : detailUrl=页面网址
	'''
	print 'Analyzing Job Page : %s' %detailUrl
	# === 获取网页源码 ===
	webTarget = webPageSourceCode(detailUrl)
	if not webTarget : return '' # 如果没有结果 则推出
	# === BeautifulSoup解析源码，也是最花时间的，解析器不对则会造成7秒/页面 ===
	soup = BeautifulSoup(webTarget['html'], 'html5lib')
	# === 获取职位头信息 ===
	posi    = bsText(soup, pattr='[class*=inner-left] h1')
	firm    = bsText(soup, pattr='[class*=inner-left] h2')
	welfare = bsText(soup, pattr='[class*=welfare-tab-box]')
	descri  = bsText(soup, pattr='[class*=tab-inner-cont]', more=True) #第一个是职位描述，第二个是企业简介
	data = [posi, firm, welfare, descri[0], descri[1]]
	# === 获取职位基本信息的框架 ===
	# 这个框架中的数据list顺序为：职位月薪->工作地点->发布日期->工作性质->工作经验->最低学历->招聘人数->职位类别
	resu = bsText(soup, pattr='[class*=terminal-ul] li strong', more=True)
	data += resu # 合并两个列表
	# === 获取企业基本信息的框架 ===
	# 这个框架中的数据list顺序为：公司规模->公司性质->公司行业->公司主页->公司地址
	resu = bsText(soup, pattr='[class*=terminal-company] li strong', more=True)
	data += resu # 合并两个列表
	# 将网页名作为日志文件名
	txt = './data/%s.txt' % urllib.quote(detailUrl).split('/')[-1]
	with open(txt, 'w') as f:
		f.write('\n'.join(data).encode('utf-8')) # 全文操作除了这里全是Unicode格式！
	print '-------- Done analyzing the job page : %s' %posi
	return data

def ZhilianFirmPage(firmUrl=''):
	'''	
	# Function: 获取智联招聘的企业详细信息页面
	# Params  : firmUrl=页面网址
	# Notes   : 企业页面就复杂了，分为普通页面和VIP页面，网址不同，源码也不同
	'''
	# print '已经解析完一家企业：%s' %firmUrl
	return ''

def webPageSourceCode(baseUrl='', urlParams={}, method='GET', antiRobot={}):
	'''	
	# Function: 抽象出来模块化的网页源码获取函数：传入网址及必要信息，返回源码等相关信息
	# Params  : baseUrl=准备抓取的网址，method=GET | POST，urlParams=URL中的参数，antiRobot=爬虫伪装方式
	'''
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
	# === Post方式获取源码 ===
	# req = urllib2.Request(baseUrl, urllib.urlencode(urlParams), headers)
	# src = urllib2.urlopen(req)
	# === Get 方式获取源码 ===
	fullUrl = '%s?%s' %(baseUrl, urllib.urlencode(urlParams)) if urlParams else baseUrl
	try: src = urllib2.urlopen(fullUrl)
	except Exception as e:
		print 'Failed on retrieving internet resource : %s\nThe error description is as below:' %fullUrl
		print e

	trueUrl = src.geturl() # 获取真实Url网址
	# print 'Processing Url: %s' %fullUrl # 测试用。显示正在处理的网页
	# === 本地方式读取源码 ===
	# src = open('./Templates/test-Zhilian-list-page-sm0.html', 'r') # 测试用，0.001秒
	html_doc = unicode(src.read(),'utf-8') # 用时1秒。

	# === 函数返回网页源码，及必要信息 ===
	return {'html':html_doc,'fullUrl':fullUrl,'trueUrl':trueUrl}

def urlParam(url=''):
	'''
	# Function : 读取url中的参数，并以dict字典返回所有参数
	'''
	query  = urlparse.urlparse(url).query
	params = dict([(key,value[0]) for key, value in urlparse.parse_qs(query).items()])
	return params

def bsText(tag, pattr, more=False):
	'''
	# Function : 根据搜索条件，返回搜索结果的字符串(Unicode格式！)
	# Params   : tag=BeautifulSoup返回的Tag对象，pattr=搜索条件，more=是否以列表形式返回多行数据
	# Steps    : 如果pattr是str字符串，则用select选择器搜索结果
				 如果pattr是dict 字典，则用find_all()搜索结果
				 如果pattr是list 列表，则分别递归自己直到找出结果
	'''
	retr = [] # 待返回的列表对象
	if isinstance(pattr, str): # 如果是str字符串，则用select选择器搜索结果
		result = tag.select(pattr)
		retr = [r.get_text(strip=True) for r in result] if result else ''
	elif isinstance(pattr, dict) and pattr['t']: # 是dict 字典，则用find_all()搜索结果
		result = tag.find_all(text=re.compile(pattr['t']), strip=True)
		retr = [r.string for r in result] if result else ''
		# 字符替换处理。如原文是"职位月薪：8000-10000"，则去掉前面的"职位月薪："几个字
		retr = [t.replace(pattr['t'], '') for t in retr]
	elif isinstance(pattr, list) and len(pattr): # 如果是list列表，则递归本函数直到找出结果
		for sub in pattr:
			result = bsText(tag, sub, more=more)
			retr = result if result else ''
			if result : break # 如果已经找到数据 就退出循环
	# === 返回运算结果 ===
	# 一般只返回第一条字符串结果，如果要求more则返回一个列表
	if not retr : return ''
	if more : return retr    if retr and isinstance(retr, list) else []
	else    : return retr if retr and isinstance(retr, str) else retr[0]

def bsAttrs(tag, pattr):
	'''
	# Function : 根据搜索条件，返回搜索结果的Tag属性
	# Params   : tag=BeautifulSoup返回的Tag对象，pattr=搜索条件
	# Steps    : 一般来讲，pattr是list列表，['搜索条件','Tag属性名']
	'''
	result = tag.select(pattr[0])
	# print '根据 %s 找到%d个结果' %(str(pattr), len(result))
	return result[0][pattr[1]].encode('utf-8') if len(result) else ''

# 计算时间
def timeup(foo, attr1, attr2):
	start = time.clock()
	val = foo(attr1, attr2)
	end = time.clock()
	timeuse = end-start
	print '=== Spend %d sec. on running %s()\n' %(timeuse, foo.__name__)
	return val

def urlQuote(url=''):
	'''
	# Function: 研究url编码转换的把戏
	'''
	url_ori = 'http://sou.zhaopin.com/jobs/searchresult.ashx?sm=1&jl=数据&p=1&gc=5号&ga=立水桥&kt=0&kw=数据'
	url_coded = '%2fjobs%2fsearchresult.ashx%3fsm%3d1%26jl%3d%25E5%258C%2597%25E4%25BA%25AC%26kt%3d0%26kw%3d%25E6%2595%25B0%25E6%258D%25AE%26gr%3d2%26isfilter%3d1%26p%3d1%26re%3d2015%26ga%3d%25e7%258e%258b%25e8%25be%259b%25e5%25ba%2584'
	print url_ori
	print url_coded
	# 把带中文的ur转换编码成这样的：http%3A//sou.zhaopin.com/jobs/searchresult.ashx%3Fsm%3D1%26jl%3D%E6%95%B0%E6%8D%AE%26p%3D1%26gc%3D5%E5%8F%B7%26ga%3D%E7%AB%8B%E6%B0%B4%E6%A1%A5%26kt%3D0%26kw%3D%E6%95%B0%E6%8D%AE
	print urllib.quote(url_ori)
	# 把正常的url再进一步转换：
	print urllib.quote(urllib.quote(url_ori))
	# 把url解码还原成有正常的url：http://sou.zhaopin.com/jobs/searchresult.ashx?sm=1&jl=%E5%8C%97%E4%BA%AC&kt=0&kw=%E6%95%B0%E6%8D%AE&gr=2&isfilter=1&p=1&re=2015&ga=%e7%8e%8b%e8%be%9b%e5%ba%84
	print urllib.unquote(url_coded)
	# 把正常的url还原成显示中文的url：http://sou.zhaopin.com/jobs/searchresult.ashx?sm=1&jl=北京&kt=0&kw=数据&gr=2&isfilter=1&p=1&re=2015&ga=王辛庄
	print urllib.unquote(urllib.unquote(url_coded))

if __name__ == '__main__':
	timeup(ZhilianSearchJoblist, '数据', 1) # 在线解析3秒，本地解析2秒
	# timeup(ZhilianJobPage, 'http://jobs.zhaopin.com/525178924271109.htm?ssidkey=y&ss=201&ff=03', '') # 0~1秒
	# data = [1,2,3]
	# retr = [[4],5,6]
	# data += retr
	# print data
