#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2018/7/16


from conf.settings import *
from core.my_modules import *
import struct
import json


class FTPClient:

    socket_family = SOCKET_FAMILY
    socket_type = SOCKET_TYPE
    allow_reuse_address = False
    backlog = BACKLOG
    buffer_size = BUFFER_SIZE
    encoding = ENCODING

    def __init__(self, server_address, connect=True):
        self.is_login = False
        self.server_address = server_address
        self.socket = socket.socket(self.socket_family,
                                    self.socket_type)
        if connect:
            try:
                self.client_connect()
            except Exception:
                self.client_close()
                raise

    def client_connect(self):
        try:
            self.socket.connect(self.server_address)
        except ConnectionRefusedError as e:
            print_log(ERROR, "Error:%s" % e)
            exit()

    def client_close(self):
        self.socket.close()

    def login(self):
        self.send_msg(["login"])
        username = input("用户名: ").strip()
        password = input("密码: ").strip()
        user_dic = {
            'username': username,
            'password': password
        }
        self.send_msg(user_dic)
        status = self.recv_msg()
        if status == STATUS_CODE[200]:
            print_log(INFO, status)
            self.is_login = True
        else:
            print_log(WARNING, status)
            self.is_login = False

    def create_user(self):
        self.send_msg(["create_user"])
        while True:
            username = input("用户名: ").strip()
            if not username:
                continue
            password = input("密码: ").strip()
            disk_size = input("所需磁盘空间大小(MB): ").strip()
            if not disk_size.isdigit():
                print_log(WARNING, "磁盘空间大小必须为数字!")
                continue
            user_dic = {
                'username': username,
                'password': password,
                'disk_size': disk_size
            }
            self.send_msg(user_dic)
            status = self.recv_msg()
            if status == STATUS_CODE[100]:
                print_log(INFO, status)
            else:
                print_log(ERROR, status)
            return

    def get(self, cmd):
        if len(cmd) != 2:  # 判断指令格式是否正确
            print_log(WARNING, "输入的指令有误!")
            return
        filename = cmd[1]  # 获取文件名
        file_path = os.path.join(DOWNLOAD_PATH, filename+'.download')  # 文件保存路径
        if os.path.isfile(file_path):  # .download文件存在, 文件需断点续传
            recv_size = os.path.getsize(file_path)
        else:  # 从头下载
            recv_size = 0
        cmd.append(recv_size)
        self.send_msg(cmd)
        file_status = self.recv_msg()  # 文件是否存在
        if file_status == STATUS_CODE[300]:  # 文件不存在
            print_log(WARNING, file_status)
            return
        else:  # STATUS_CODE[301] 文件存在
            with open(file_path, 'wb') as f:
                file_size = self.recv_msg()
                while recv_size < file_size:
                    part = self.recv_msg(is_byte=True)
                    f.write(part)
                    recv_size += len(part)
                    bar_print(recv_size, file_size)  # 打印进度条
            print()
            rename_file(DOWNLOAD_PATH, filename+'.download', filename)

    def put(self, cmd):
        if len(cmd) != 2:
            print_log(WARNING, "输入的指令有误!")
            return
        filename = cmd[1]  # 获取文件名
        file_path = os.path.join(UPLOAD_PATH, filename)  # 文件路径
        if not os.path.isfile(file_path):
            print(WARNING, "文件不存在!")
            return
        else:
            file_size = os.path.getsize(file_path)
            cmd.append(file_size)
            self.send_msg(cmd)
            status = self.recv_msg()
            if status == STATUS_CODE[302]:
                print_log(WARNING, status)
                return
            send_size = self.recv_msg()
            with open(file_path, 'rb') as f:
                f.seek(send_size)
                while send_size < file_size:
                    data = f.read(1024)
                    self.send_msg(data, is_byte=True)
                    send_size += len(data)
                    bar_print(send_size, file_size, mode='u')  # 打印进度条
            print()

    def cd(self, cmd):
        if len(cmd) != 2:
            print_log(WARNING, "输入的指令有误!")
            return
        self.send_msg(cmd)
        res = self.recv_msg()
        if res == STATUS_CODE[600]:
            print_log(INFO, res)
            current_path = self.recv_msg()
            print_log(INFO, "当前路径为: "+current_path)
        else:
            print_log(WARNING, res)

    def dir(self, cmd):
        self.send_msg(cmd)
        res = self.recv_msg()
        # print(res)
        print_table(["文件名", "文件类型"], res)

    def mkdir(self, cmd):
        if len(cmd) != 2:
            print_log(WARNING, "输入的指令有误!")
            return
        self.send_msg(cmd)
        res = self.recv_msg()
        if res == STATUS_CODE[400]:
            print_log(INFO, res)
        else:
            print_log(WARNING, res)

    def rm(self, cmd):  # 删除文件
        if len(cmd) != 2:
            print_log(WARNING, "输入的指令有误!")
            return
        self.send_msg(cmd)
        res = self.recv_msg()
        if res == STATUS_CODE[500]:
            print_log(INFO, res)
        else:
            print_log(WARNING, res)

    def exit_client(self, *args):  # 退出
        self.client_close()
        sys.exit()

    @staticmethod
    def help_info():
        head = ["格式", "功能"]
        row = [
            ["get + (文件名)", "下载文件"],
            ["put + (文件名)", "上传文件"],
            ["cd + (路径)", "切换目录"],
            ["dir", "查询当前目录下的文件列表"],
            ["mkdir + (文件夹名)", "创建文件夹"],
            ["rm + (文件名)", "删除文件或空文件夹"],
            ["exit_client", "退出"]
        ]
        print_table(head, row)

    def send_msg(self, msg, is_byte=False):
        if is_byte:
            msg_bytes = msg
        else:  # 若msg不是byte类型, 转换为byte
            msg_bytes = bytes(json.dumps(msg), encoding='utf-8')

        # 制作报头
        headers = {'data_size': len(msg_bytes)}
        head_json = json.dumps(headers)
        head_json_bytes = bytes(head_json, encoding='utf-8')

        self.socket.send(struct.pack('i', len(head_json_bytes)))  # 先发报头的长度
        self.socket.send(head_json_bytes)  # 再发报头
        self.socket.sendall(msg_bytes)  # 再发真实的内容

    def recv_msg(self, is_byte=False):
        head = self.socket.recv(4)  # 先收4个bytes，这里4个bytes里包含了报头的长度
        head_json_len = struct.unpack('i', head)[0]  # 解出报头的长度
        head_json = json.loads(self.socket.recv(head_json_len).decode('utf-8'))  # 拿到报头
        data_len = head_json['data_size']  # 取出报头内包含的信息

        # 开始收数据
        recv_size = 0
        recv_data = b''
        while recv_size < data_len-1024:
            recv_data += self.socket.recv(1024)
            recv_size += 1024
        recv_data += self.socket.recv(data_len-recv_size)
        if is_byte:
            msg = recv_data
        else:
            msg = json.loads(recv_data.decode('utf-8'))
        return msg

    def run_client(self):
        cmd = input(">>> ").strip().split()
        if hasattr(self, cmd[0]):
            func = getattr(self, cmd[0])
            func(cmd)
        else:
            print_log(WARNING, "输入的指令有误")
            self.help_info()


def run():
    client = FTPClient(SERVER_ADDRESS)
    print_log(INFO, "Waiting...")
    while True:  # 接收服务端确认信息, 开始通信
        res = client.recv_msg()
        if res == STATUS_CODE[000]:
            print_log(INFO, res)
            break

    while not client.is_login:  # 如未登陆成功
        menu = {
            '0': ['登录', client.login],
            '1': ['注册', client.create_user],
            '2': ['退出', client.exit_client],
        }
        print_menu(menu)
        print("请输入选项: ")
        choice = check_choice(3)
        menu[choice][1]()

    client.help_info()
    while True:
        client.run_client()
