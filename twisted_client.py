import time, datetime, queue
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
from buffer_controller import BufferController

BEGIN = b'BEGIN' * 3
END = b'END' * 3
END_CONNETION = b'LOST' * 3

class TcpClient(Protocol):
    SERVER_MAP = {}
    def connectionMade(self):
        self.buffer = queue.Queue()
        self.bufferController = BufferController(self.buffer)
        self.bufferController.start()

        addr = self.transport.addr  # 获取服务器端的连接信息
        print("connected", self.transport.socket)
        client_ip = addr[0]
        TcpClient.SERVER_MAP[client_ip] = self
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        str = "C:/Users/cak/Desktop/paper/open3d/models"
        # str = "D:/Download/8iVFBv2/longdress/Ply"
        self.transport.write(str.encode("utf-8"))  # 向服务器文件夹

    def connectionLost(self, reason):
        addr = self.transport.addr  # 获取服务器端的连接信息
        client_ip = addr[0]
        if client_ip in TcpClient.SERVER_MAP:
            del TcpClient.SERVER_MAP[client_ip]

    def dataReceived(self, tcp_data):
        addr = self.transport.addr  # 获取服务器端的连接信息
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            # print("receive: ", nowTime, ", size: ", len(tcp_data))
            self.buffer.put(tcp_data)
            if END_CONNETION in tcp_data:
                print("close")
                self.connectionLost("close")

        except BaseException as e:
            print("Comd Execute Error from", addr, "data:", tcp_data)
            str = "客户端发生异常 " + nowTime
            self.transport.write(str.encode("utf-8"))

class TcpClientFactory(ClientFactory):
    def buildProtocol(self, addr):
        print("Connected To Tcp Server", addr)
        self.protocol = TcpClient()
        return self.protocol

host = "127.0.0.1"
port = 9527
reactor.connectTCP(host, port, TcpClientFactory())
reactor.run()