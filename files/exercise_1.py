"""
1. 将一个文件拆分为两个小文件,按照字节数平均拆分, 使用父进程和子进程同时进行
一个进程获取半部分,换一个进程获取下半部分

提示 :  os.path.getsize()
"""

from multiprocessing import Process
import os

filename = "./timg.jpg"
size = os.path.getsize(filename)

# 复制上半部分
def top():
    fr = open(filename,'rb')
    fw = open('top.jpg','wb')
    n = size // 2  # 要复制n个字节
    # 拷贝文件
    while n > 1024:
        data = fr.read(1024)
        fw.write(data)
        n -= 1024
    fw.write(fr.read(n))

    fr.close()
    fw.close()

# 复制后半部分
def bot():
    fr = open(filename, 'rb')
    fw = open('bot.jpg', 'wb')

    fr.seek(size//2,0) # 将文件偏移量置为中间位置

    while True:
        data = fr.read(1024)
        if not data:
            break
        fw.write(data)
    fr.close()
    fw.close()


# 创建进程
p = Process(target = top)
p.start()   # 子进程执行

bot() # 父进程执行

p.join()









