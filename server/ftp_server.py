"""
    服务端
"""
import sys
from socket import socket

sys.path.append("/home/tarena/pyworkspace/FTPProject/")
from server.ftp_thread import FTPThread


class FTPServer:

    def __init__(self):
        """
            初始化服务器
        """
        __HOST = "0.0.0.0"
        __PORT = 6489
        __ADDRESS = (__HOST, __PORT)
        self.__s_socket = socket()
        self.__s_socket.bind(__ADDRESS)
        self.__s_socket.listen(10)

    def __connection(self):
        """
            等待客户端连接
        :return: None
        """
        while True:
            try:
                c_socket, c_address = self.__s_socket.accept()
            except KeyboardInterrupt:
                sys.exit("服务器退出")

            print(c_address, "已经连接")
            new_thread = FTPThread(c_socket, c_address)
            new_thread.setDaemon(True)  # 线程随着主进程退出而退出
            new_thread.start()

    def main(self):
        self.__connection()


if __name__ == '__main__':
    s = FTPServer()
    s.main()
