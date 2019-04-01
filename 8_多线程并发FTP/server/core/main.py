#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _author_ = "Raina"
# Date: 2019/1/14

from conf.settings import *
import struct
from core.my_modules import *
# import subprocess
from core.myThreadPool import ThreadPool


class FTPServer:

    socket_family = SOCKET_FAMILY
    socket_type = SOCKET_TYPE
    bind_and_listen = True
    allow_reuse_address = False
    backlog = BACKLOG
    buffersize = BUFFER_SIZE
    encoding = ENCODING

    def __init__(self, server_address):
        self.server_address = server_address
        self.socket = socket.socket(self.socket_family,
                                    self.socket_type)
        # self.conn = None
        # self.client_addr = None
        self.home_path = os.path.join(BASE_DIR, 'home')
        self.user_dir = None
        self.user_disk_size = 0

        if self.bind_and_listen:
            try:
                self.server_bind()
                self.server_listen()
            except Exception:
                self.server_close()
                raise

    def server_bind(self):
        if self.allow_reuse_address:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def server_listen(self):
        self.socket.listen(self.backlog)

    def server_close(self):
        self.socket.close()

    def get_request(self):
        return self.socket.accept()

    @staticmethod
    def close_request(request):
        request.close()

    def send_msg(self, conn, msg, is_byte=False):
        if is_byte:
            msg_bytes = msg
        else:
            msg_bytes = bytes(json.dumps(msg), encoding='utf-8')
        headers = {'data_size': len(msg_bytes)}
        head_json = json.dumps(headers)
        head_json_bytes = bytes(head_json, encoding='utf-8')

        conn.send(struct.pack('i', len(head_json_bytes)))  # 先发报头的长度
        conn.send(head_json_bytes)  # 再发报头
        conn.sendall(msg_bytes)  # 再发真实的内容

    def recv_msg(self, conn, is_byte=False):
        head = conn.recv(4)  # 先收4个bytes，这里4个bytes里包含了报头的长度
        if not head:
            return
        head_json_len = struct.unpack('i', head)[0]  # 解出报头的长度
        head_json = json.loads(conn.recv(head_json_len).decode('utf-8'))  # 拿到报头
        data_len = head_json['data_size']  # 取出报头内包含的信息

        # 开始收数据
        recv_size = 0
        recv_data = b''
        while recv_size < data_len-1024:
            recv_data += conn.recv(1024)
            recv_size += 1024
        recv_data += conn.recv(data_len-recv_size)
        if is_byte:
            msg = recv_data
        else:
            msg = json.loads(recv_data.decode('utf-8'))
        return msg

    def handle_msg(self, conn, cmd):
        if hasattr(self, cmd[0]):
            func = getattr(self, cmd[0])
            func(conn, cmd)

    def create_user(self, conn, cmd):
        user_dict = self.recv_msg(conn, )
        username = user_dict['username']
        if username in ACCOUNTS_DICT:
            self.send_msg(conn, STATUS_CODE[101])
        else:
            user_dict['password'] = hex_md5(user_dict['password'])
            ACCOUNTS_DICT[username] = user_dict
            save_db(ACCOUNTS_DICT, ACCOUNTS_PATH)
            self.send_msg(conn, STATUS_CODE[100])

    def login(self, conn, cmd):
        user_dict = self.recv_msg(conn, )
        print(user_dict)
        username = user_dict['username']
        password = user_dict['password']
        if username not in ACCOUNTS_DICT:
            self.send_msg(conn, STATUS_CODE[201])
        else:
            account_info = ACCOUNTS_DICT[username]
            if username == account_info['username'] and hex_md5(password) == account_info['password']:
                self.user_dir = os.path.join(self.home_path, username)
                if not os.path.exists(self.user_dir):
                    os.mkdir(self.user_dir)  # 创建用户家目录
                os.chdir(self.user_dir)
                self.user_disk_size = float(account_info['disk_size'])
                self.send_msg(conn, STATUS_CODE[200])
            else:
                self.send_msg(conn, STATUS_CODE[201])

    def get(self, conn, cmd):
        filename = cmd[1]
        send_size = cmd[2]
        file_path = os.path.join(os.getcwd(), filename)
        if os.path.isfile(file_path):
            self.send_msg(conn, STATUS_CODE[301])
            with open(file_path, 'rb') as f:
                file_size = os.path.getsize(file_path)
                self.send_msg(conn, file_size)
                f.seek(send_size)
                while send_size < file_size:
                    data = f.read(1024)
                    self.send_msg(conn, data, is_byte=True)
                    send_size += len(data)
        else:
            self.send_msg(conn, STATUS_CODE[300])
            return

    def put(self, conn, cmd):
        filename = cmd[1]
        file_size = cmd[2]
        if get_file_size(self.user_dir, MB, file_size) > self.user_disk_size:
            self.send_msg(conn, STATUS_CODE[302])
            return
        else:
            self.send_msg(conn, STATUS_CODE[303])
        file_path = os.path.join(os.getcwd(), filename+'.upload')  # 文件保存路径
        if os.path.isfile(file_path):  # .download文件存在, 文件需断点续传
            recv_size = os.path.getsize(file_path)
        else:  # 从头下载
            recv_size = 0
        self.send_msg(conn, recv_size)
        with open(file_path, 'wb') as f:
            while recv_size < file_size:
                part = self.recv_msg(conn, is_byte=True)
                f.write(part)
                recv_size += len(part)
        rename_file(os.getcwd(), filename+'.upload', filename)

    def cd(self, conn, cmd):
        cd_path = os.path.join(os.getcwd(), cmd[1])
        previous_path = os.getcwd()
        if os.path.isdir(cd_path):
            os.chdir(cd_path)
            now_path = os.getcwd()
            if now_path.startswith(self.user_dir):
                self.send_msg(conn, STATUS_CODE[600])
                self.send_msg(conn, now_path[len(self.home_path):])
                return
            else:
                os.chdir(previous_path)
        self.send_msg(conn, STATUS_CODE[601])

    def dir(self, conn, cmd):
        # sub_pro = subprocess.Popen('dir', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # stdout = sub_pro.stdout.read()
        # stderr = sub_pro.stderr.read()
        # self.send_msg(conn, (stdout+stderr).decode('gbk'))
        dir_type = []
        dir_list = os.listdir()
        for i in dir_list:
            if os.path.isfile(i):
                dir_type.append([i, "<FILE>"])
            elif os.path.isdir(i):
                dir_type.append([i, "<DIR>"])
            else:
                dir_type.append([i, "<UNKNOWN>"])
        self.send_msg(conn, dir_type)

    def mkdir(self, conn, cmd):
        mkdir_path = os.path.join(os.getcwd(), cmd[1])
        if os.path.exists(mkdir_path):
            self.send_msg(conn, STATUS_CODE[401])
        else:
            os.mkdir(mkdir_path)
            self.send_msg(conn, STATUS_CODE[400])

    def rm(self, conn, cmd):
        rm_path = os.path.join(os.getcwd(), cmd[1])
        if os.path.isfile(rm_path):
            os.remove(rm_path)
        elif os.path.isdir(rm_path) and (len(os.listdir(rm_path)) == 0):
            os.removedirs(rm_path)
        else:
            self.send_msg(conn, STATUS_CODE[501])
            return
        self.send_msg(conn, STATUS_CODE[500])

    def task(self, conn, pool):
        self.send_msg(conn, STATUS_CODE[000])
        while True:
            try:
                cmd = self.recv_msg(conn)
                if not cmd:
                    print_log(WARNING, "Error happened with client, close connection.")
                    pool.task_down()
                    break
                print(">>>", cmd)
                self.handle_msg(conn, cmd)
            except ConnectionResetError as e:
                print("Error happened with client, close connection.\n", e)
                self.close_request(conn)
                pool.task_down()
                break

    def run(self):
        pool = ThreadPool(MAX_THREAD)
        print_log(INFO, 'Starting FTP server on %s: %s'.center(45, '-') % (BIND_HOST, BIND_PORT))
        while True:
            # print_log(INFO, "等待连接...")
            conn, client_addr = self.get_request()
            thread = pool.get_thread()
            print_log(INFO, "连接成功!")
            p = thread(target=self.task, args=(conn, pool))
            p.start()


def run():
    server = FTPServer(SERVER_ADDRESS)
    server.run()
