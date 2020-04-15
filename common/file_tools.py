"""
    文件操作工具
"""
from socket import socket
from time import sleep


class MyFileTools:

    @staticmethod
    def send_file_tcp(c_socket: socket, file_path: str):
        file = open(file_path, "rb")
        while True:
            data = file.read(1024)
            if not data:
                sleep(0.1)
                c_socket.send(b"##")
                break
            c_socket.send(data)
        file.close()
