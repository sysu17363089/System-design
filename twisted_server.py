import time, datetime, os
from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import pickle
import open3d as o3d
import numpy as np

BEGIN = b'BEGIN' * 3
END = b'END' * 3
INTER = b'INTER' * 3
END_CONNETION = b'LOST' * 3



class TcpServer(Protocol):
    CLIENT_MAP = {}  # 用于保存客户端的连接信息

    def connectionMade(self):
        addr = self.transport.client  # 获取客户端的连接信息
        print("connected", self.transport.socket)
        TcpServer.CLIENT_MAP[addr] = self

    def connectionLost(self, reason):
        addr = self.transport.client  # 获取客户端的连接信息
        if addr in TcpServer.CLIENT_MAP:
            print(addr, "Lost Connection from Tcp Server", 'Reason:', reason)
            del TcpServer.CLIENT_MAP[addr]

    def dataReceived(self, tcp_data):
        addr = self.transport.client  # 获取客户端的连接信息
        print("server receive data")
        
        msg = tcp_data.decode("utf-8")
        print("Received msg", msg, "from Tcp Client", addr)
        self.sendFiles(msg)
        

    # def sendFiles(self, dir):
    #     files = os.listdir(dir)
    #     for file in files:
    #         with open(dir + '/' + file, 'rb') as f:
    #             msg = f.read()
    #             msg = BEGIN + msg + END
    #             self.transport.write(msg)
    #     self.transport.write(END_CONNETION)

    def sendFiles(self, dir):
        files = os.listdir(dir)
        for index, file in enumerate(files):
            begin = time.time()
            pointCloud = o3d.io.read_point_cloud(dir + '/' + file)
            pointCloud = pointCloud.uniform_down_sample(4)
            points = pickle.dumps(np.asarray(pointCloud.points))
            colors = pickle.dumps(np.asarray(pointCloud.colors))
            msg = BEGIN + points + INTER + colors + END
            print("send ", index," : ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.transport.write(msg)
            end = time.time()
            print("deal file cost:", end-begin)
        print("end")
        self.transport.write(END_CONNETION)

port = 9527
serverFactory = Factory.forProtocol(TcpServer)
reactor.listenTCP(port, serverFactory)
print("#####", "Starting TCP Server on", port, "#####")
reactor.run()