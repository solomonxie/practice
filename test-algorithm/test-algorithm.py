# coding: utf-8

def test_loop_speed():
	# 目的：如果直接把一个动态函数而不是静态数据放在for循环中，会降低效率吗？
	# NO -------速度不变。动态的函数只会运行一遍，并不是每次循环都重新运行一遍
	retr = []
	for i in range(10):
		retr += [i]
		print str(i)
	return retr
	# 调用方法：
	# for sub in test_loop_speed(): print 'counting...'

def test_if_in_loop():
	# 测试可不可以在for循环中嵌套if语句
	# OK ----测试通过
	arr = [1,2,3,4,5] # 可能性1
	# arr = '' # 可能性2
	for i in arr if isinstance(arr, list) else [arr]:
		print i

# ========================================================================
if __name__ == '__main__':
	test_if_in_loop()