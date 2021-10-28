import os
import socket
import time


# 定义允许传输的文件大小
RECVSIZE = 1024 * 1024 * 500
# 定义标签，用于标记文件夹名字与文件名字
label = '#97'*100


def dirwalker(foldername):
    """
    此方法用于遍历目标文件夹
    :param foldername:
    :return: 一个生成器
    """
    # 遍历文件夹，返回生成器
    walkers = os.walk(foldername)
    for walker in walkers:
        dirname = walker[0]
        files = walker[2]
        print("files:", files)

        # 返回标记后文件夹的名称
        # yield dirname + label

        for file in files:
            with open(dirname + '/' + file, 'rb') as f:
                msg = f.read()
                # 返回文件内容
                yield msg if msg != b'' else b' '


def dirwalkermsg(foldername, source='sources/'):
    """
    用于生产字节流信息
    :param foldername: 客户端要copy的文件夹名称
    :param source: 服务端数据源
    :return: 返回一个字节流生成器
    """

    foldername = source + foldername
    if not os.path.isdir(foldername):
        print(f"{foldername}不存在！")
        yield b'None!'
    else:
        for msg in dirwalker(foldername):
            if isinstance(msg, bytes):
                yield msg
            else:
                yield msg.encode()

    # 返回结束信号
    print("end")
    yield 'end!'.encode()


def send_file_client(dir_socket):
    """
    向客户端发送字节流
    :param dir_socket:
    :return:
    """
    # 　接受客户端消息
    dir_name = dir_socket.recv(RECVSIZE).decode()
    print(dir_name)
    # 根据客户端请求下载的内容， 调用函数， 生成字节流
    msg = dirwalkermsg(dir_name, source="")
    try:
        while True:
            context = next(msg)
            dir_socket.send(context)
            # 强制等待，等待数据传输完成，具体等待参数有待考虑
            time.sleep(1)
    except Exception as e:
        print(e)


def main():
    # 创建套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 固定端口号
    server_socket.bind(("127.0.0.1", 2813))
    while True:
        # 被动套接字转换为主动套接字
        server_socket.listen(128)
        # 生成一个面向请求客户端的套接字
        dir_socket, client_ip = server_socket.accept()
        # 调用发送数据函数
        send_file_client(dir_socket)
        # 关闭套接字
        dir_socket.close()
    # server_socket.close()


if __name__ == '__main__':
    main()

