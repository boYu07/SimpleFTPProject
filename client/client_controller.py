"""
    客户端处理模块
"""
import os
import re
import sys
from socket import socket

sys.path.append("/home/tarena/pyworkspace/FTPProject/")
from common.file_tools import MyFileTools as FT


class ClientController:

    def __init__(self, c_socket: socket):
        self.__c_socket = c_socket
        self.__DEFAULT_PATH = "/home/tarena/pyworkspace/FTPProject/test_files/"

    def show_file_name(self):
        """
            1. 向服务端发送请求 L
            2. 接收服务端反馈 Y/N
                Y 从服务端接收文件信息
                N 结束
        """
        self.__c_socket.send(b"L")
        data = self.__c_socket.recv(128)
        if data == b"N":
            print("获取文件列表失败")
            return
        if data == b"Y":
            data = self.__c_socket.recv(10240)
            print(data.decode())
            return
        raise exit("未知错误")

    def upload_file(self, file_path: str):
        """
            1. 检查文件是否存在
                不存在 返回
                存在 继续
            2. 向服务端发送请求 U file_name
            3. 接受服务端反馈 Y/N
                Y 向服务端传送文件 ## 代表发送完毕
                N 结束
            4. 接收服务端反馈 $$ 表示接收完毕
        """
        if not os.path.exists(file_path):
            print("文件不存在")
            return
        file_name = file_path.split("/")[-1]
        data = "U " + file_name
        self.__c_socket.send(data.encode())
        data = self.__c_socket.recv(128)
        if data == b"N":
            print("上传失败,已有相同名称文件")
            return
        if data == b"Y":
            FT.send_file_tcp(self.__c_socket, file_path)
            data = self.__c_socket.recv(128)
            if data == b"$$":
                print("上传完毕")
            return
        raise exit("未知错误")

    def download_file(self, file_name: str):
        """
            1. 向服务端发送请求 D file_name
            2. 接受服务端反馈 Y/N
                Y 从服务端接收文件 ## 代表对方发送完毕 文件存在则重新命名
                N 结束
            3. 向服务端发送新消息 "$$" 表示接收完毕
        """
        data = "D " + file_name
        self.__c_socket.send(data.encode())
        data = self.__c_socket.recv(128)
        if data == b"N":
            print("获取文件失败")
            return
        if data == b"Y":
            print("开始下载")
            f_name = self.__format_file_name(file_name)
            file = open(self.__DEFAULT_PATH + f_name, "wb")
            while True:
                data = self.__c_socket.recv(1024)
                if data == b"##":
                    self.__c_socket.send(b"$$")
                    print("下载完成")
                    break
                file.write(data)
            file.close()
            return
        raise exit("未知错误")

    def quit(self):
        """
            1. 向服务端发送请求
            2. 退出程序
        """
        self.__c_socket.send(b"Q")
        self.__c_socket.close()
        sys.exit("客户端退出")

    def __format_file_name(self, file_name: str) -> str:
        count = 1
        list_f_name = list(re.findall(r"(.+)(\..*)", file_name)[0])
        list_f_name.insert(-1, "")
        while True:
            if "".join(list_f_name) not in os.listdir(self.__DEFAULT_PATH):
                return "".join(list_f_name)
            list_f_name[1] = " (%s)" % count
            count += 1
