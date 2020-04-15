"""
    自定义线程类
"""
import os
import sys
from socket import socket
from threading import Thread
from time import sleep
from typing import List

sys.path.append("/home/tarena/pyworkspace/FTPProject/")
from common.file_tools import MyFileTools as FT


class FTPThread(Thread):

    def __init__(self, c_socket: socket, c_address):
        super().__init__()
        self.__PATH = "/home/tarena/pyworkspace/FTPProject/files/"
        self.__c_socket = c_socket
        self.__c_address = c_address

    def run(self):
        """
            1. 接收并解析客户端请求
        """
        while True:
            data = self.__c_socket.recv(1024)
            print(self.__c_address, data.decode())
            list_data = data.decode().split(" ", 1)
            protocol = list_data[0]
            print(protocol)  # debug
            if not data or protocol == "Q":
                print(self.__c_address, "已经退出")
                self.__c_socket.close()
                return
            if protocol == "L":
                self.__show_file()
            elif protocol == "U":
                self.__upload_file(list_data[1])
            elif protocol == "D":
                self.__download_file(list_data[1])
            else:
                print("未知请求")

    def __show_file(self):
        """
            1. 查看文件库,并向客户端反馈 Y/N
                Y 允许请求,向客户端发送文件信息
                N 拒绝请求,文件库没有文件
        """
        list_file_name = self.__get_file_name()
        data = "\n".join(list_file_name)
        if data:
            self.__c_socket.send(b"Y")
            sleep(0.1)  # 确保客户端已经准备好接收文件信息
            self.__c_socket.send(data.encode())
            return
        self.__c_socket.send(b"N")

    def __upload_file(self, file_name: str):
        """
            1. 查看文件库,并向客户单反馈 Y/N
                Y 允许请求,接收客户端文件 ## 代表对方发送完毕
                N 拒绝请求,文件库有重名文件
            2. 向客户端发送消息 $$ 表示接收完毕
        :param file_path: 接收的文件路径
        """
        if os.path.exists(self.__PATH + file_name):
            self.__c_socket.send(b"N")
            return
        self.__c_socket.send(b"Y")
        file = open(self.__PATH + file_name, "wb")
        while True:
            data = self.__c_socket.recv(1024)
            if data == b"##":
                break
            file.write(data)
        file.close()
        self.__c_socket.send(b"$$")

    def __download_file(self, file_name: str):
        """
            1. 查看文件库,并向客户单反馈 Y/N
                Y 允许请求,向客户端发送文件 "##" 代表发送完毕
                N 拒绝请求,文件不存在
            2. 接收客户端反馈 "$$" 表示接收完毕
        """
        list_file_name = self.__get_file_name()
        if file_name not in list_file_name:
            self.__c_socket.send(b"N")
            return
        self.__c_socket.send(b"Y")
        sleep(0.1)
        FT.send_file_tcp(self.__c_socket, self.__PATH + file_name)

        data = self.__c_socket.recv(128)
        if not data:
            print("对方掉线")
        elif data == b"$$":
            print("发送完毕")

    def __get_file_name(self) -> List[str]:

        return os.listdir(self.__PATH)
