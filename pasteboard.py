# -*- coding: utf-8 -*-

import os

# 从PyObjC库的AppKit模块引用NSPasteboard主类，和PNG、TIFF的格式类
from AppKit import NSPasteboard, NSPasteboardTypePNG, NSPasteboardTypeTIFF


def main():
    print get_paste_img_file()


def get_paste_img_file():
    """
    将剪切板数据保存到本地文件并返回文件路径
    """
    pb = NSPasteboard.generalPasteboard()  # 获取当前系统剪切板数据
    data_type = pb.types()  # 获取剪切板数据的格式类型

    # 根据剪切板数据类型进行处理
    if NSPasteboardTypePNG in data_type:          # PNG处理
        data = pb.dataForType_(NSPasteboardTypePNG)
        filename = 'HELLO_PNG.png'
        filepath = '/tmp/%s' % filename            # 保存文件的路径
        ret = data.writeToFile_atomically_(filepath, False)    # 将剪切板数据保存为文件
        if ret:   # 判断文件写入是否成功
            return filepath
    elif NSPasteboardTypeTIFF in data_type:         #TIFF处理： 一般剪切板里都是这种
        # tiff
        data = pb.dataForType_(NSPasteboardTypeTIFF)
        filename = 'HELLO_TIFF.tiff'
        filepath = '/tmp/%s' % filename
        ret = data.writeToFile_atomically_(filepath, False)
        if ret:
            return filepath
    elif NSPasteboardTypeString in data_type:
        # string todo, recognise url of png & jpg
        pass

if __name__ == '__main__':
    main()
