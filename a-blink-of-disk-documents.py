# coding:utf-8
'''
	# 快速把本文件夹（或指定文件夹）的所有文件夹及其中所有文件的镜像
	# 而镜像就是：文件夹还是文件夹，文件则只以文件名创建txt文件
	# 这样的备份其实比较划算：什么都可以从网上下载，不用非得源文件保存
	# txt文件不光保留文件名 内容中还可以记录文件属性信息
'''
import os
# base = os.getcwd()
base = 'D:\\TDownload' # 此根目录不支持中文
for root, subdir, files in os.walk(base, topdown=True):
	mir = root.replace(base, base+'-Mirror')
	if not os.path.exists(mir): os.mkdir(mir) # 创建镜像文件夹
	for name in files:
		ori = root+'\\'+name
		new = mir+'\\'+name+'.txt'
		try:
			info  = str( os.stat(ori) )
			with open(new,'w') as f:
				f.write(ori+'\n'+info)
		except Exception as e:
			print e
			with open(base+'\\errors.txt', 'a') as f:
				f.write('\n'+str(e)+'\n')
			continue