'''
	# Title: 千里码测试题
'''

def quiz1():
	'''
	# task1 码之初
	# 第2333个能被2或者被3整除的正整数是…?请把答案填入答题框内…如果有问题请查看右侧的学习资料。
	# 举例:(被2或者被3整除的正整数依次是：2,3,4,6,8,9,10,12,14,15,16,18…)
	'''
	index = 0
	i = 1
	while not index == 2333:
	    if i%2==0 or i%3==0:
	        index += 1
	        print 'No.%d number can mod 2 or 3 is : %d' %(index, i)
	    i += 1

def quiz2():


if __name__ == '__main__':
	quiz2()