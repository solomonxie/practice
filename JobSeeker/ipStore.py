# coding:utf-8
'''
	# Title : 在线爬取IP工具
	# Author: Solomon Xie
	# Usage : 
	# Notes : 
	# Update: 
'''
# === 必备模块 ===
import urllib2, urllib, re, random, datetime
import requests # 第三方
from bs4 import BeautifulSoup # 第三方
import os
# === 自制模块 ===
from WebspiderToolbox import *

def myIP(WAN=False):
	'''
		# 获取本机的公网IP或局域网IP
		# 目前不知道别的办法，就通过和本机命令行交互'nslookup'命令来获取公网IP吧
	'''
	# 获取公网IP
	cmd  = os.popen('nslookup')
	for line in cmd.readlines():
		if 'Address:' in line: 
			print line
			wanip = line.replace('Address:  ','')
			print wanip
			return wanip

def getIP(ipformat='', more=False):
	'''
	# Function: 从且只从本地IP仓库文件中提取1个或所有ip地址。
	# Notes   : 如果 ipformat='PROXY'，则只返回'1.1.1.1:80'这样的格式
				如果 ipformat='IP'，则返回字典形式的{'http':'http://1.1.1.1:80'}
	'''
	# 直接从IP仓库文件中读取所有的IP地址
	lines = []
	with open('./data/ips/ip_20151222.txt', 'r') as f:
		lines = f.read().split('\n')
	if   ipformat == 'IP':
		ips = [s.split('//')[-1] for s in lines]
		return ips if more else ips[random.randint(0,len(lines)-1)] if ips else ''
	elif ipformat == 'PROXY':
		proxies = []
		for s in lines:
			resu = s.split('://')
			if len(resu)==2: proxies.append( {resu[0]:s} )
		return proxies if more else proxies[random.randint(0,len(lines)-1)] if proxies else ''
	else: 
		return lines if more else lines[random.randint(0,len(lines)-1)] if lines else ''

def updateIPs(online=False):
	'''
	# Function: 自动在线爬取ip，更新本地IP地址库。【如非必要，此函数尽量手动调用】
	# Notes   : 1. 相当于一个独立的爬虫，爬取多个在线网站的ip数据。快速灵活很重要，因为代理ip失效很快。
				2. 为了避免频繁读取被屏蔽，可以同时爬多个网站，每次只爬其1个页面，循环一圈后再爬第2个页面
	'''
	for i in range(1,10): ip_on_kuaidaili_com(pn=i, online=online)
	# saveIPs( ip_on_ipcn_org(online=online) )
	print 'Done updated IP addresses.'
def saveIPs(proxies=[]):
	'''
	Function: 将ip保存为标准文件，在代码逻辑的便利性上考虑，本函数只能被updateIPs()调用。
	Notes   : 
	'''	
	# 将ip保存为标准文件，在代码逻辑的便利性上考虑，本函数只能被updateIPs()调用。
	now = datetime.datetime.now()
	with open('./data/ips/ip_%s.txt'%now.strftime('%Y%m%d'), 'a') as f:
		f.write('\n'.join(proxies)+'\n' )

def verifyIP(ip=''):
	'''
	Function: 在线或在本地服务器网站（为了快速），检验IP是否可用、是否统一、是否高匿等
	Notes   : 先到网站上获取本机真实IP再做对比
			  验证通过返回True，失败则返回False。
	'''
	url = 'http://www.ip.cn'
	webTarget = {}
	try:
		webTarget = webPageSourceCode( url, proxy={'http':'http://%s'%ip} ) # 用代理IP打开网页
	except Exception as e:
		# print 'Error on using this proxy [%s] to connect the verification site.'%ip
		return False
	html = webTarget.get('html') if webTarget else ''
	# resu = re.findall(re.compile('<code>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</code>'), html)
	if html.find( '<code>%s</code>'%ip.split(':')[0] ) > 0:
		# print 'Using IP [%s], and the IP [%s] is detected.'%(ip, str(resu))
		return True
	else: return False
def TEST_verifyIP():
	# print verifyIP('117.136.234.7:843')
	proxies = getIP(more=True)
	for ip in proxies:
		if verifyIP(ip): print '======================Use this proxy[%s]======================'%ip
		else: print 'False'

def ip_on_kuaidaili_com(pn, online=False):
	'''
	Function: 解析kuaidaili.com的在线或本地网页中的IP地址。本函数只有在UpdateIPs()时才会被用到。
	Notes   : 为了避免过分嵌套，函数一次只获取一页函数。因此页码是必要参数。
	'''
	# === 以在线或是本地方式获取网页源码 ===
	if not online: # 如果是本地解析
		with open('./data/ips/src/kuaidaili_com_pn_%d.html'%pn, 'r') as f:
			html = f.read()
	else:          # 如果是在线解析
		webTarget = webPageSourceCode('http://www.kuaidaili.com/free/outha/%d/'%pn, local=False)
		if not webTarget: return ''
		html = webTarget['html']
		# 将网页保存到本地
		with open('./data/ips/src/kuaidaili_com_pn_%d.html'%pn, 'w') as f:
			f.write(html.encode('utf-8'))
	# === 将源码中IP提取出来 === 
	soup = BeautifulSoup(html, 'html5lib')
	resu = soup.select('#list table[class^=table] tbody tr')
	ips = []
	for row in resu:
		c = row.select('td')
		# 组装成[0.0.0.0:8080]格式的IP
		oip = '%s:%s'%( c[0].get_text(),c[1].get_text() )
		if oip: ips.append(oip)
	print len(ips)
	# 将ip保存为标准文件，在代码逻辑的便利性上考虑，本函数只能被updateIPs()调用。
	now = datetime.datetime.now()
	with open('./data/ips/ip_%s.txt'%now.strftime('%Y%m%d'), 'a') as f:
		f.write('\n'.join(ips)+'\n' )
	# 返回值
	return ips if ips else []

def ip_on_ipcn_org(online=False, anotherUrl=''):
	if not online:
		with open('./data/ips/src/ipcn_org_2_20151218.html', 'r') as f:
			html = f.read()
	else:
		url = 'http://proxy.ipcn.org/proxylist2.html' if not anotherUrl else anotherUrl
		webTarget = webPageSourceCode(url)
		html = webTarget['html'].encode('utf-8')
		with open('./data/ips/src/ipcn_org_1_20151218.html') as f:
			f.writelines(html)
	# Start to analyse local html files
	# resu = re.findall(re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$'), html)
	resu = re.findall(re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}'), html)
	ips = [ip for ip in resu] if len(resu) else []
	txtLog( len(ips) )
	return ips if ips else []


# ---------------------------------------------------------------------------------
if __name__ == '__main__':
	# for i in range(2): print repr( getIP(ipformat='PROXY') )
	# updateIPs() # 更新在线的IP库
	myIP()
