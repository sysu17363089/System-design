
import socket
import os, struct
import numpy as np
from decode import Decoder, Decoder_old
from player import Player, PointCloudAttri
import queue
import time

# 定义服务端的数据源， 用于处理文件夹与文件名称
source = 'sources/'
# 定义标签，必须与服务端一致
LABEL = b'#97' * 100
# 定义允许传输的文件大小
RECVSIZE = 1024 * 1024 * 500

QUEUE = queue.Queue()
DECODER = Decoder()


def recv_file_server(client_socket):
    """
    向服务端请求要下载的文件夹，
    处理服务端返回的数据，完成下载
    """
    # 向服务器请求要拷贝的文件夹
    # dir_name = input("请输入要拷贝的文件夹:")
    dir_name = "C:/Users/cak/Desktop/paper/open3d/models"
    # dir_name = "D:/system/open3d/open3d/models"
    client_socket.send(dir_name.encode())
    try:
        while True:
            # 服务端信息接收器：甲
            head_data = client_socket.recv(4)
            print('get')
            # if head_data == b'end!':
            #     print("end!")
            #     break
            recv_size = struct.unpack('i',head_data)[0]
            print("size:", recv_size)
            recv_data = bytes()
            while recv_size > 0:
                # print('while', recv_size)
                recv_data += client_socket.recv(recv_size)
                recv_size -= len(recv_data)
            print("recive data:",len(recv_data))
            
            # deal_Bfile(msg)
            continue
            # print('msg',msg.decode()[:20])
            # 判断服务端信息是否被标记, 如果被标记， 判断被标记几次， 一次是文件夹， 二次是文件
            if LABEL in msg:
                print("have label")
                msg = msg.decode()
                # 如果被标记一次， 则根据字节流信息建立文件夹
                # if status(msg) == 1:
                #     # mkdir(msg)
                #     print("First time")
                # # 如果被标记二次， 则说明该字节流存储文件名字，需要继续等待服务端的传来文件内容的字节流
                # # 激活接收器： 乙
                # # elif status(msg) == 2:
                # else:
                #     # 服务端信息接收器：乙
                #     context = client_socket.recv(RECVSIZE)
                #     print("get message")
                #     # print("recv time:",time.time())
                #     deal_Bfile(context)
                #     # 接收到结束信息， 退出while True
                #     if context == b'end!':
                #         break
               
            # 如果服务端返回b'None'， 则说明请求的文件夹不存在
            elif msg == b'None!':
                print('请求文件夹不存在！')
                break
            # 接收到结束信息， 退出while True
            elif msg == b'end!':
                print('下载完成！')
                QUEUE.put('quit')
                break
            else:
               context = client_socket.recv(RECVSIZE)
               deal_Bfile(context) 
    except Exception as e:
        print(e)


# def status(msg):
#     """
#     :param msg: 服务端发来的字节流
#     :return: msg中含有标签的数目
#     """
#     return (len(msg) - len(msg.replace(LABEL.decode(), ""))) // len(LABEL.decode())

def deal_Bfile(context):
    begin = time.time()
    DECODER.decode(context)
    
    attri = PointCloudAttri(DECODER.get_points(), DECODER.get_colors())
    end = time.time()
    print("Binary to num: ", end-begin)
    QUEUE.put(attri)


def main():
    # 创建套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接服务器
    # client_socket.connect(("127.0.0.1", 2813))
    client_socket.connect(("127.0.0.1", 9527))
    # client_socket.connect(('172.18.166.178', 2813))
    # 调用接收函数
    recv_file_server(client_socket)
    # 关闭套接字
    client_socket.close()


if __name__ == '__main__':
    video_player = Player(QUEUE)
    # video_player.start()
    main()
    # video_player.join()
