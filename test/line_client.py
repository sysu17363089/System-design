from twisted.protocols.basic import  LineReceiver
# from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from  twisted.internet import  reactor

class TcpClient(LineReceiver):
    def connectionMade(self):
        print("connnet")
        str = "C:/Users/cak/Desktop/paper/open3d/models"
        self.sendLine(str.encode("utf-8"))

    def connectionLost(self, reason):
        print("connnet lost")
        return super().connectionLost(reason=reason)

    def lineReceived(self, line):
        msg = line.decode("utf-8")
        print("###", msg)
    
    def dataReceived(self, data):
        print("receive data:",len(data))

class TcpClientFactory(ClientFactory):
    def buildProtocol(self, addr):
        print("Connected To Tcp Server", addr)
        self.protocol = TcpClient()
        return self.protocol

host = "127.0.0.1"
port = 9527
reactor.connectTCP(host, port, TcpClientFactory())
reactor.run()