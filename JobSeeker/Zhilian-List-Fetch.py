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
# === 必备模块 ===
import urllib2, urllib, re
from bs4 import BeautifulSoup
# === 小工具用模块 ===
import time, urlparse
# === 如果要做一些bs4专有类型的判断就必须导入 ===
# import bs4 

def ZhilianSearchJoblist(keyword='数据', assignPage=1, totalPages=1, scope=0):
	'''
	# Function: 向智联招聘提交搜索信息，并获取智联搜索页的所有职位信息
	# Params : keyword=搜索关键词，assignPage=页码
	'''
	# ^暂时手动制定总的读取页数
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
			# 方法1
			# 但是会有问题就是，如果`识别重复`方面没有做好，这里就会形成无限循环。
			# 可以想到的笨方法就是，先取得所有相关的企业名称和链接，然后再用函数把它读取出来，循环生成。
			# publicJobs = ZhilianFirmPage(data[-1])
			# print 'This company is recruiting %d jobs now.' %len(publicJobs)
			# 方法2
			# 递归本函数，用企业名搜索其下所有招聘信息。
			# ZhilianSearchJoblist(data[1].encode('utf-8'), 1, scope=3) 
			'''
		# 输出结果：暂时用txt文件输出，后面会用到数据库
		outname = './data/ZhilianSearch-%s-p%d.txt' %(soup.title.get_text(), truePage)
		# outname = './data/log-search-scope%d-page%d.txt' %(scope,truePage)
		with open(outname, 'w') as f:
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
	if truePage < totalPages and truePage == assignPage:
		ZhilianSearchJoblist(keyword, truePage+1)
	else: print '-'*50 + 'Reached the end of records.'

def ZhilianJobPage(detailUrl=''):
	'''	
	# Function: 获取智联招聘的职位详细信息页面
	# Params  : detailUrl=页面网址
	'''
	print 'Analyzing a job page.'
	# === 获取网页源码 ===
	webTarget = webPageSourceCode(detailUrl)
	# src = open('./Templates/test-Zhilian-detail-page - AttributeError _ NoneType object has no attribute next_element.html', 'r') # 测试用
	# webTarget = {'html':unicode(src.read(),'utf-8')}  # 测试用
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
	resu = bsText(soup, pattr='[class*=terminal-ul] li strong', more=True)
	# ^这个框架中的数据list顺序为：职位月薪->工作地点->发布日期->工作性质->工作经验->最低学历->招聘人数->职位类别
	data += resu # 合并两个列表
	# === 获取企业基本信息的框架 ===
	resu = bsText(soup, pattr='[class*=terminal-company] li strong', more=True)
	# ^这个框架中的数据list顺序为：公司规模->公司性质->公司行业->公司主页->公司地址
	data += resu # 合并两个列表
	outname = './data/%s.txt' % urllib.quote(detailUrl).split('/')[-1]
	# ^将网页名作为日志文件名
	with open(outname, 'w') as f:
		f.write('\n'.join(data).encode('utf-8')) # 全文操作除了这里全是Unicode格式！
	print '-------- Done analyzing the job page : %s' %posi
	return data

def ZhilianFirmPage(firmUrl=''):
	'''	
	# Function: 获取智联招聘的企业详细信息页面里面的企业基本信息及招聘列表。
	# Params  : firmUrl=页面网址
	# Steps   : 先判断域名，如果是“标准页面”则正常解析，如果是“Special页面”则在得到“标准页面”后才正式解析。
	# Notes   : 企业页面就复杂了，分为普通页面和VIP页面，网址不同，源码也不同
	'''
	# === 开始解析网址 ===
	# 无论是Special页面还是标准页面，都必须要解析。
	webTarget = webPageSourceCode(firmUrl)
	soup = BeautifulSoup(webTarget['html'], 'html5lib')
	# === 根据域名判断当前为“标准页面”还是“Special页面” ===
	subDomain = urlAnalyse(firmUrl)['subloc'][0]
	if subDomain == 'special' :
		# 如果是"Special页面"则获取其标准页面的URL，并重新加载此函数。
		finder = re.findall(re.compile(r' href="(.+?)"'), str(soup.select('td[align=right]')))
		standardUrl = finder[0] if finder else ''
		if len(standardUrl) : 
			print 'Redirecting from a special company page to a standard page...'
			ZhilianFirmPage(standardUrl) # 以标准页面重新加载此函
			return ''		
	# === 在标准页面中获取该公司所有招聘信息的链接 ===
	resu = soup.select('[class=positionListContent1] [class*=jobName] a[href]')
	data = [t['href'] for t in resu ]
	print 'Done of retrieving %d job links of this company.' %len(resu)
	return data # 返回所有正在招聘的职位链接

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
	if urlParams : fullUrl = '%s?%s' %(baseUrl, urllib.urlencode(urlParams))
	else : fullUrl = baseUrl
	# fullUrl = '%s?%s' %(baseUrl, urllib.urlencode(urlParams)) if urlParams else baseUrl
	print 'Processing a web page: %s' %fullUrl
	try: 
		src = urllib2.urlopen(fullUrl)
	except Exception as e:
		print 'No resources found : %s\nThe error internet resource is :' %fullUrl
		print e
		return {'html':'','fullUrl':'','trueUrl':''}
	trueUrl = src.geturl() # 获取真实Url网址
	# print 'Processing Url: %s' %fullUrl # 测试用。显示正在处理的网页
	# === 本地方式读取源码 ===
	# src = open('./Templates/test-Zhilian-list-page-sm0.html', 'r') # 测试用，0.001秒
	html_doc = unicode(src.read(),'utf-8') # 用时1秒。

	# === 函数返回网页源码，及必要信息 ===
	return {'html':html_doc,'fullUrl':fullUrl,'trueUrl':trueUrl}

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
		retr = [t.replace(pattr['t'], '') for t in retr]
		# ^字符替换处理。如原文是"职位月薪：8000-10000"，则去掉前面的"职位月薪："几个字
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
def timeup(foo, attr1, attr2, attr3):
	start = time.clock()
	val = foo(attr1, attr2, attr3)
	end = time.clock()
	timeuse = end-start
	print '=== Spend %d sec. on running %s()\n' %(timeuse, foo.__name__)
	return val

def urlAnalyse(url=''):
	'''
	# Function : 分析拆解URL，并返回相应的数据
	# Examples : 如URL为`http://sou.zhaopin.com/jobs/searchresult.ashx?p=13sm=0&kt=0#body`
				 则返回值为：{'scheme':'http','netloc':'sou.zhaopin.com','path':'/jobs/searchresult.ashx',
				 'params':'','query':'p=13sm=0&kt=0','fragment'='body','values':{['p':'13','sm':'0','kt':'0']}
	'''
	import urlparse
	oo = urlparse.urlparse(url)
	return {
		'scheme'   : oo[0], # 协议。如'http'/'https'/'ftp'等
		'netloc'   : oo[1], # 网址。如'www.baidu.com'/'sou.zhaopin.com'等
		'subloc'   : oo[1].split('.'), # 域名块，list列表。如'www.baidu.com'就会被解析为['www','baidu','com']
		'path'     : oo[2], # 路径。如'/jobs/2015/123124.html'
		'file'     : oo[2].split('/')[-1],                # 文件全称。如'searchresult.ashx'
		'filename' : oo[2].split('/')[-1].split('.')[0],  # 文件名  。如'searchresult'
		'params'   : oo[3], # ...
		'query'    : oo[4], # 参数。如'p=13sm=0&kt=0'
		'fragment' : oo[5], # 分片。如'#title'
		'quote'    : urllib.quote(url),   # 将url转为带%符号的
		'unquote'  : urllib.unquote(url), # 将带%符号的转为原url（含中文的话就复杂了，需要双重unquote或字符转编码）
		'values'   : dict([
						(key,value[0]) for key, value in urlparse.parse_qs(oo.query).items()
					])     # 参数值，字典形式。如{['key':'关键词','city':'北京']}
	}

if __name__ == '__main__':
	timeup(ZhilianSearchJoblist, '数据', 1, 90) # 在线解析3秒，本地解析2秒
	# ZhilianJobPage('')
	# ZhilianFirmPage('http://special.zhaopin.com/pagepublish/25244851/index.html')
