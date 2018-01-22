# coding:utf-8
# Tkinter是Python自带的一个GUI开发库，包含一大堆相关模块
import Tkinter

# 最简单的GUI界面，一个Helloworld的小标签
def test():
	root = Tkinter.Tk() #创建一个根部件，及根窗口，大平板
	word = Tkinter.Label(root, text='hello world!') #创建一个label标签
	word.pack() #把标签加到根部件上
	root.mainloop() #显示窗口

if __name__ == '__main__':
	test()