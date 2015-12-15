# -*- coding: utf-8 -*-
'''
	# Title : 58同城招聘信息爬虫 - 职位搜索页、职位详情页、企业主页、企业信用档案页
	# Author: Solomon Xie
	# Usage : 
	# Notes : 
	# Update: 
'''
# === 必备基础模块 ===
import urllib2, urllib, re
from bs4 import BeautifulSoup
# === 自制工具模块 ===
from WebspiderToolbox import *
from DBProcessor import sqlInsert

def gen58JobUrl(pn='1'):
	'''
	Function : 生成58招聘的搜索URL链接
	Notes    : 1. 58的页码默认为空：不出现在URL中。因为在没有搜索结果时，加入页码后服务器会返回404
	'''
	uv = {
		'key'       : '助理',#ask('搜索关键词'),             # [查询参数] 查询关键字 
		'city'      : 'bj',                          # [域名] bj,tj,sh,gz等城市简称
		'loc'       : '', # [目录] [可省略] 城市某地区或某地点，海淀区为'haidian/'
		'catg'      :'job',                          # [目录] 职位类别，全部类别为'job'
		'pn'        : pn,                            # [目录] 页码，第一页可以省略。
		'industry'  : '',                            # [拆分目录1] [可省略] 行业代码,互联网行业为244
		'cmpType'   : '',                            # [拆分目录2] [可省略] 公司类型代码
		'eduReq'    : '',                            # [拆分目录3] 学历代码，[可省略]，本科代码为6
		'workingAge': '',                            # [拆分目录4] 工作经验代码，[可省略]，6-7年代码为7
		'wf'        : '',                            # [查询参数] [可省略] 福利待遇
		'pay'       : '',                            # [查询参数] [可省略] 月薪范围
		'postdate'  : '',                            # [查询参数] [可省略] 发布时间范围
		'sptp'      : ''                             # [查询参数] [可省略] SpecialType，一般为'gls'，不知道是什么
	}
	# === 根据参数编制URL ===
	if uv['loc']:  uv['loc'] = '/%s'%uv['loc']
	if pn and int(pn)<=1: uv['loc'] = '/pn%s'%pn
	more = [] # 这4项条件组合后，位置在页码前的一处。
	if uv['industry']:   more.append( 'pve_5363_%s'%uv['industry'] )
	if uv['cmpType']:    more.append( 'pve_5754_%s'%uv['cmpType'] )
	if uv['eduReq']:     more.append( 'pve_5356_%s'%uv['eduReq'] )
	if uv['workingAge']: more.append( 'pve_5357_%s'%uv['workingAge'] )
	uv['more'] = '/' + '_'.join(more) + '' if more else ''
	url = 'http://%(city)s.58.com%(loc)s/%(catg)s%(more)s%(pn)s/?key=%(key)s&params6693=%(wf)s&minixinzi=%(pay)s&specialtype=%(sptp)s'%uv
	return url

def FiveEightJobs(assignPage='1', totalPages=1, nextUrl=''):
	'''
	# Function: 向服务器提交搜索信息,并获取职位搜索页的所有职位信息
	# Params  : keyword=搜索关键词,assignPage=页码
	# Notes   : 
	'''
	print 'Tring processing General  Search List Page %s ==========='%(assignPage if assignPage else '1')		
	# === 获取网页源码 ===
	url = nextUrl if nextUrl else gen58JobUrl(pn=assignPage)
	webTarget = webPageSourceCode( url )
	if not webTarget : return '' # 如果没有获取到网络信息 则退出 # 不过目前这一句的逻辑是否正确还没想通-_-!
	# === BeautifulSoup解析源码,也是最花时间的,解析器不对则会造成7秒/页面 ===
	soup = BeautifulSoup(webTarget['html'], 'html5lib')
	# === 检测当前页是否有结果 ===
	with open('log.html', 'w') as f:
		f.write(soup.prettify('utf-8'))
	if bsGet(soup, css='#searchTip', withTxt='抱歉') or bsGet(soup, css='h1[class="item"]', withTxt='抱歉'): 
		print 'No any result or you have been blocked.-_-!' # 如果没有显示结果 则推出
		return ''
	# === 获取真实页码 ===
	truePage = bsGet(soup, css='div[class="pagerout"] div[class="pager"] strong')
	truePage = int(truePage) if truePage else 1 # 如果结果少于1页,则不会有任何结果
	# === 获取下一页链接 === # 58的下一页链接是不完整的-_-!再去补完还不如自己造呢
	try: nextUrl = bsGet(soup,css='div[class="pagerout"] a[class="next"]',attri='href')
	except: print 'No link of next-page found.'
	# === 获取信息条目 ===
	blocks = soup.select('[logr$="ses^composite^0"]')
	print '=== Detected %d Job Information in this page.' %len(blocks)
	if len(blocks):
		titles = 'jobName,jobLink,cmpName, cmpLink, cmpLoc, jobUpdate'
		values = []
		for row in blocks:
			if bsGet(row, css='div[class="tuiguang"]'): continue # 排除推广信息
			values.append([
				bsGet(row, css='a[_t="common"]'),
				bsGet(row, css='a[_t="common"]',attri='href'),
				bsGet(row, css='div[class="titbar"] h2'),
				bsGet(row, css='dd[class="w96"]'),
				bsGet(row, css='dd[class="w68"]')
			])
		# 输出结果：MySQL的sql文件输出
		sqlfile = './data/INSERT_INTO_TEMP_SEARCHRESULTS_FiveEight.sql'
		fback = sqlInsert('TEMP_SEARCHRESULTS_FiveEight', titles, values, sqlfile=sqlfile)
		# print fback
	else: 
		print 'No any record found in this page.'
	if int(truePage) < int(totalPages):
		if not nextUrl and truePage < assignPage: FiveEightJobs(keyword, assignPage='%d'%(int(truePage)+1), totalPages=totalPages)
		else: FiveEightJobs(keyword, assignPage=truePage+1, nextUrl=nextUrl, totalPages=totalPages)
	else: print '-'*50 + 'Reached the end of records. truePage[%s], assignPage[%s], totalPages[%s].' %(truePage,assignPage,totalPages)

def FiveEightJobPage(detailUrl=''):
	'''	
	# Function: 获取58招聘的职位详细信息页面
	# Params  : detailUrl=页面网址
	'''
	print 'Analyzing a job page.'
	# === 获取网页源码 ===
	webTarget = webPageSourceCode(detailUrl)
	# src = open('./Templates/test-FiveEight-detail-page - AttributeError _ NoneType object has no attribute next_element.html', 'r') # 测试用
	# webTarget = {'html':unicode(src.read(),'utf-8')}  # 测试用
	if not webTarget : return '' # 如果没有结果 则推出
	# === BeautifulSoup解析源码,也是最花时间的,解析器不对则会造成7秒/页面 ===
	soup = BeautifulSoup(webTarget['html'], 'html5lib')
	# === 获取职位头信息 ===
	posi    = bsGet(soup, css='[class*=inner-left] h1')
	firm    = bsGet(soup, css='[class*=inner-left] h2')
	welfare = bsGet(soup, css='[class*=welfare-tab-box]')
	descri  = bsGet(soup, css='[class*=tab-inner-cont]', more=True) # 正常有2项结果。1.职位描述 2.企业简介
	data = [posi, firm, welfare, descri[0], descri[1]]
	# === 获取职位多项基本信息 ===
	resu = bsGet(soup, css='[class*=terminal-ul] li strong')
	# ^这个框架中的数据list顺序为：职位月薪->工作地点->发布日期->工作性质->工作经验->最低学历->招聘人数->职业类别
	data += resu # 合并两个列表
	# === 获取企业基本信息的框架 ===
	resu = bsGet(soup, css='[class*=terminal-company] li strong')
	# ^这个框架中的数据list顺序为：公司规模->公司性质->公司行业->公司主页->公司地址
	data += resu # 合并两个列表
	outname = './data/%s.txt' % urllib.quote(detailUrl).split('/')[-1]
	# ^将网页名作为日志文件名
	with open(outname, 'w') as f:
		f.write('\n'.join(data).encode('utf-8')) # 全文操作除了这里全是Unicode格式！
	print '-------- Done analyzing the job page : %s' %posi
	return data

def FiveEightFirmPage(firmUrl=''):
	'''	
	# Function: 获取58招聘的企业详细信息页面里面的企业基本信息及招聘列表。
	# Params  : firmUrl=页面网址
	# Steps   : 先判断域名,如果是“标准页面”则正常解析,如果是“Special页面”则在得到“标准页面”后才正式解析。
	# Notes   : 企业页面就复杂了,分为普通页面和VIP页面,网址不同,源码也不同
	'''
	# === 开始解析网址 ===
	# 无论是Special页面还是标准页面,都必须要解析。
	webTarget = webPageSourceCode(firmUrl)
	soup = BeautifulSoup(webTarget['html'], 'html5lib')
	# === 根据域名判断当前为“标准页面”还是“Special页面” ===
	subDomain = urlAnalyse(firmUrl)['subloc'][0]
	if subDomain == 'special' :
		# 如果是"Special页面"则获取其标准页面的URL,并重新加载此函数。
		# 只能用正则表达式获取`<!-- -->`隐藏标签的内容。
		finder = re.findall(re.compile(r' href="(.+?)"'), str(soup.select('td[align=right]')))
		standardUrl = finder[0] if finder else ''
		if len(standardUrl) : 
			print 'Redirecting from a special company page to a standard page...'
			FiveEightFirmPage(standardUrl) # 以标准页面重新加载此函
			return ''		
	# === 在标准页面中获取该公司所有招聘信息的链接 ===
	# ===>>> 不过有一点：页面只会显示一个城市的招聘，其他城市的信息则是Javascript动态加载的。
	# 		 也就是说，还不如直接在搜索主页按照企业名搜索的强。
	resu = soup.select('[class=positionListContent1] [class*=jobName] a[href]')
	data = [t['href'] for t in resu ]
	print 'Done of retrieving %d job links of this company.' %len(resu)
	return data # 返回所有正在招聘的职位链接

def FiveEightRoster(nextUrl='', assignPage=1, city='', industry=''):
	'''
	# Function: 抓取58同城的“企业名录”网页。只抓取"名称"和"链接"。
	# Notes   : 1. 为求效率,这是个"三重递归"函数。逻辑是这样的：第一次运行，挨个找城市链接，然后点开一个城市链接，
				然后再挨个点开行业链接，循环读取所有名录之后再进入下一个城市链接进行循环。
				2. 运行后发现。。。这玩意效率太高！不到2分钟就被58屏蔽IP了-_-!怎么办。。
	'''
	# === 先从主页抓取所有子城市、行业类别的名录页 ===
	if not nextUrl:
		print '='*80 + 'First Run.'
		webTarget = webPageSourceCode('http://qy.58.com/citylist/') # 初始先从全部城市页面入手
		if not webTarget: return ''
		soup = BeautifulSoup(webTarget['html'], 'html5lib')
		if not city:
			ctLinks = soup.select('#clist a[href^="http://qy.58.com/"]')
			for ct in ctLinks: 
				FiveEightRoster(ct['href'], city=ct.get_text(strip=True))
		else:
			indLinks = soup.select('[class^="indCateList"] a[href^="http://qy.58.com/"]')
			for link in indLinks: FiveEightRoster(link['href'], city=city, industry=link.get_text(strip=True))
		return ''

	# === 读取一个分类的所有页面数据 === OK 可以独立运行
	print 'Tring processing the list-page %d of Firm Roster in the city [%s] ==========='%(assignPage, city)
	url = 'http://qy.58.com/%s/pn%d'%(city,assignPage) if not nextUrl else nextUrl
	# url = './templates/58Firm-Roster.html'
	webTarget = webPageSourceCode(url)
	if not webTarget: return ''
	soup = BeautifulSoup(webTarget['html'], 'html5lib')
	firms = soup.select('[class="compList"] a[href^="http://qy.58.com/"]')
	if not len(firms): # 说明已经到结尾了
		print 'You have reached the end of records, or maybe you have been blocked.'
		return ''
	titles  = 'cmpName, cmpLink_58, cmpCity, industry'
	values  = [[tag.get_text(strip=True), tag['href'], city, industry] for tag in firms]
	print '=== Detected %d Firms in this page.' %len(values)
	subpath = '_'.join(urlAnalyse(url)['path'].split('/'))
	sqlfile = './data/INSERT_INTO_FIRMS%spn%d.sql'%(subpath, assignPage)
	sqls = sqlInsert(table='FIRMS',titles=titles, values=values, sqlfile=sqlfile)
	# === 按递归循环读取所有页面 ===
	# FiveEightRoster(assignPage=assignPage+1, city=city) # 注释掉的话，就只读取一页数据

# ===============================================================================================
if __name__ == '__main__':
	# timeup(eval('FiveEightJobs()')) # 在线解析3秒,本地解析2秒	
	FiveEightRoster()
	# FiveEightJobPage('')
	# FiveEightFirmPage('http://special.zhaopin.com/pagepublish/25244851/index.html')