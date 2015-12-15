# -*- coding: utf-8 -*-
'''
	# Title : 智联招聘信息爬虫 - 搜索列表页、职位详细页、企业主页
	# Author: Solomon Xie
	# Usage : A practise with python: 
				get job information from a chinese job seeking web Zhilian.com.
				This little project is auctually a web crawler, 
				which uses some techniques such as BeautifulSoup and urllib2 and so on.
	# Notes : 切记：全文操作除了输出外,所有和BeautifulSoup相关的变量存储和被操作的全是Unicode格式！否则绝对出问题
	# Update: v1.0 已经能够准确获取智联招聘搜索结果列表的职位信息了
'''
# === 必备基础模块 ===
import urllib2, urllib, re
from bs4 import BeautifulSoup
# === 自制工具模块 ===
from WebspiderToolbox import webPageSourceCode,bsGet,txtLog,urlAnalyse,timeup
from DBProcessor import sqlInsert

def ZhilianSearchList(keyword='数据', assignPage=1, totalPages=1, scope=0, nextUrl=''):
	'''
	# Function: 向智联招聘提交搜索信息,并获取智联搜索页的所有职位信息
	# Params : keyword=搜索关键词,assignPage=页码
	'''
	if   scope==0 : print 'Tring processing General  Search List Page %d ==========='%assignPage
	elif scope==1 : print 'Tring processing Company  Search List Page %d -----------'%assignPage
	elif scope==2 : print 'Tring processing Position Search List Page %d -----------'%assignPage
	# === 编制URL参数 ===
	urlParams = {
		'kw' : keyword, # 搜索关键词
		'sm' : 0, # 显示方式代码： 列表是'0',详细是'1'。显示不同源码也不同,尽量选列表模式,源码更好解析。
		'jl' : '北京', # 搜索城市：'北京',多项用'+'连接(URL编码为%2B)
		#'bj' : '', # 职位类别代码：互联网产品/运营管理 的代码为 '160200',多项用'%3B'连接(URL编码的%)
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
		# 'pd' : -1, # 发布时间(天数)：一周是'7',一个月是'30',不限是'-1'
		'p' : assignPage, # 页码,超出总页码时,则会显示最后一页
		#'gr' : '', # 
		# 're' : '2015', # 这个限制了搜素数量,但是其实也不是按年份搜索
		'sg' : '', # 即全网唯一标示符——GUID
		#'' : '' #
	}
	# === 获取网页源码 ===
	'''
	# 其实在这里应该加一个计时器,如果时间超长都不返回结果,那么就伪装IP再来一次。
	# 或者如果获取源码失败,也伪装IP等再来一次。
	'''
	if nextUrl : webTarget = webPageSourceCode(nextUrl)
	else:        webTarget = webPageSourceCode('http://sou.zhaopin.com/jobs/searchresult.ashx', urlParams)
	if not webTarget : return '' # 如果没有获取到网络信息 则退出 # 不过目前这一句的逻辑是否正确还没想通-_-!
	# === BeautifulSoup解析源码,也是最花时间的,解析器不对则会造成7秒/页面 ===
	soup = BeautifulSoup(webTarget['html'], 'html5lib')
	# === 获取搜索结果的数量,并进行相应处理 ===
	total_results = bsGet(soup, css='[class$=search_yx_tj] em')
	print 'There are %s results found as total.' %total_results
	if total_results == '0': return '' # 如果当前页面没有结果,则不进行处理了。
	'''
	# === 获取全网唯一ID,即url中的sg参数 ===
	tags = soup.select('#guid')
	guid = tags[0]['value'] if len(tags)  else ''
	print 'The "guid" is %s.' %guid
	'''
	# === 获取真实页码 ===
	truePage = bsGet(soup, css='[class*="pagesDown"] a[class*="current"]')
	truePage = int(truePage) if truePage else 1 # 如果结果少于1页,则不会有任何结果
	# === 获取下一页链接 ===
	try: nextUrl = soup.select('a[class*=next-page]')[0]['href']
	except: print 'No link of next-page found.'
	# === 获取信息条目 ===
	blocks = soup.select('[class$=newlist]')
	print '=== Detected %d Job Information in this page.' %len(blocks)
	if len(blocks):
		titles = 'jobName,cmpName,feedback,workingAge,eduReq,cmpType,cmpSize,jobDescri,jobLink,cmpLink,payMonthly,cmpLoc,jobUpdate'
		values = []
		for row in blocks:
			values.append([
				bsGet(row, css='[class$=zwmc]'),  # 职位名称
				bsGet(row, css='[class$=gsmc]'),  # 公司名称
				bsGet(row, css='[class$=fk_lv]'), # 反馈比率
				bsGet(row, withTxt='经验：'),     # 工作经验
				bsGet(row, withTxt='学历：'),     # 学历背景
				bsGet(row, withTxt='公司性质：'), # 公司性质
				bsGet(row, withTxt='公司规模：'), # 公司规模
				bsGet(row, withTxt='岗位职责：'), # 岗位职责
				bsGet(row, css='[class$=zwmc] a[href^="http"]', attri='href'), # 招聘网址
				bsGet(row, css='[class$=gsmc] a[href^="http"]', attri='href'), # 企业网址
				bsGet(row, css='[class$=zwyx]', withTxt='职位月薪：'),         # 职位月薪
				bsGet(row, css='[class$=gzdd]', withTxt='地点：'),             # 工作地点
				bsGet(row, css=['[class$=gxsj]', 'dl p']),                     # 更新时间
			])
			# print 'withTxt is an unicode string:',type(values[0][4]) == type(u'') # True
			# print 'attri is an unicode string:', type(values[0][8]) == type(u'') # True
			# print 'multi-search got an unicode string:', type(values[0][8]) == type(u'') # True
			'''	
			# === 子链接抓取：新式方案 ===
			# 不在这里进行解析以免一个地方出错导致全程失败,
			# 应当先获取全部搜索结果,再本函数外对本次获取的子链接进行抓取。
				# === 跳转并解析职位信息页面 ===
				# jobUrl = bsGet(row,css='[class$=zwmc] a[href^="http"]', attri='href')
				# if jobUrl : ZhilianJobPage(jobUrl)
				# else      : print 'Failed on retrieving URL of the job: %s' %values[0]
				# === 跳转并解析企业信息页面 ===
				# 方法1
				# 但是会有问题就是,如果`识别重复`方面没有做好,这里就会形成无限循环。
				# 可以想到的笨方法就是,先取得所有相关的企业名称和链接,然后再用函数把它读取出来,循环生成。
				# publicJobs = ZhilianFirmPage(values[-1])
				# print 'This company is recruiting %d jobs now.' %len(publicJobs)
				# 方法2
				# 递归本函数,用企业名搜索其下所有招聘信息。
				# ZhilianSearchList(values[1].encode('utf-8'), 1, scope=3) 
			'''
		# 输出结果：MySQL的sql文件输出
		sqlfile = './data/INSERT_INTO_TEMP_SEARCHRESULTS_ZHILIAN.sql'
		fback = sqlInsert('TEMP_SEARCHRESULTS_ZHILIAN', titles, values, sqlfile=sqlfile)
		# print fback
		# 输出结果：txt文件输出
		# fback = txtLog(data,'./data/ZhilianSearch-%s-scope%d-p%d.txt' %(soup.title.get_text(), scope, truePage))
		# print fback
	'''
		# === 递归调用函数自身,循环读取下一页 ===
		# 循环读取每一页的信息
		# 智联招聘一般全网同时会有100,000个职位
		# 但是都不超过90个页面,一页有40个,所以顶多只能获取3600个
		# 另外,如果页码超过现有的,则会仍显示一些招聘信息,但是都是重复的。
		# 唯一不同是,上方会显示“共0个职位满足条件”
		# 如果真实的页码并没有指定页码那么多,就代表搜索到头了。
		# >>>
	'''
	if truePage < totalPages:
		if not nextUrl and truePage < assignPage: ZhilianSearchList(keyword, assignPage=truePage+1, totalPages=totalPages)
		else: ZhilianSearchList(keyword, assignPage=truePage+1, nextUrl=nextUrl, totalPages=totalPages)
	else: print '-'*50 + 'Reached the end of records. truePage[%d], assignPage[%d], totalPages[%d].' %(truePage,assignPage,totalPages)

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

def ZhilianFirmPage(firmUrl=''):
	'''	
	# Function: 获取智联招聘的企业详细信息页面里面的企业基本信息及招聘列表。
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
			ZhilianFirmPage(standardUrl) # 以标准页面重新加载此函
			return ''		
	# === 在标准页面中获取该公司所有招聘信息的链接 ===
	# ===>>> 不过有一点：页面只会显示一个城市的招聘，其他城市的信息则是Javascript动态加载的。
	# 		 也就是说，还不如直接在搜索主页按照企业名搜索的强。
	resu = soup.select('[class=positionListContent1] [class*=jobName] a[href]')
	data = [t['href'] for t in resu ]
	print 'Done of retrieving %d job links of this company.' %len(resu)
	return data # 返回所有正在招聘的职位链接


# ===============================================================================================
if __name__ == '__main__':
	timeup(ZhilianSearchList, '数据', 1, 1) # 在线解析3秒,本地解析2秒	
	# ZhilianJobPage('')
	# ZhilianFirmPage('http://special.zhaopin.com/pagepublish/25244851/index.html')