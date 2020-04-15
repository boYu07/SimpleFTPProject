"""
    客户端
"""

import sys
from socket import socket

sys.path.append("/home/tarena/pyworkspace/FTPProject/")
from client.client_controller import ClientController


class FTPClient:

    def __init__(self):
        __ADDRESS = ("localhost", 6489)
        self.__c_socket = socket()
        self.__c_socket.connect(__ADDRESS)
        self.__controller = ClientController(self.__c_socket)

    def main(self):
        while True:
            self.__show_menu()
            try:
                cmd = input(">>")
                if not cmd:
                    print("不能发送空字符串")
                    continue
            except:
                cmd = "quit"
            list_data = cmd.split(" ", 2)
            cmd = list_data[0]
            # print(cmd)  # debug
            if cmd == "list":
                self.__controller.show_file_name()
            elif cmd == "upload":
                self.__controller.upload_file(list_data[1])
            elif cmd == "download":
                self.__controller.download_file(list_data[1])
            elif cmd == "quit":
                self.__controller.quit()
            else:
                print("%s 无效的命令" % cmd)

    @staticmethod
    def __show_menu():
        print("+-----------------------+---------------+")
        print("|  命令\t\t\t|    命令提示\t|")
        print("+-----------------------+---------------+")
        print("|  list\t\t\t|    查看文件\t|")
        print("|  upload 文件路径\t|    上传文件\t|")
        print("|  download 文件名\t|    下载文件\t|")
        print("|  quit\t\t\t|    退出\t|")
        print("+-----------------------+---------------+")


if __name__ == '__main__':
    c1 = FTPClient()
    c1.main()
