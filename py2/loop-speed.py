# coding:utf-8
import timeit
import time

def while_one(i=0):
	while (1):
		i += 1
		if i == 100000:
			break

def while_true(i=0):
	while True:
		i += 1
		if i == 100000:
			break

def sumit():
	x = sum([100000])

if __name__ == '__main__':
        start = time.clock()
        while_one()
        end = time.clock()
        print str(end-start)

        start = time.clock()
        while_true()
        end = time.clock()
        print str(end-start)
        
        start = time.clock()
        x1 = sum([100000])
        end = time.clock()
        print str(end-start)

        start = time.clock()
        x2 = range(100000)
        end = time.clock()
        print str(end-start)
