# from twisted.protocols.basic import  LineReceiver
# from twisted.internet.protocol import Factory
# # from twisted.internet.protocol import ClientFactory
# from  twisted.internet import  reactor
# import os

# class TcpServer(LineReceiver):
#     def connectionMade(self):
#         print("connnet")

#     def connectionLost(self, reason):
#         print("connnet lost", reason)
#         return super().connectionLost(reason=reason)

#     def lineReceived(self, line):
#         msg = line.decode("utf-8")
        
#         self.sendFiles(msg)
    
#     def sendFiles(self, dir):
#         files = os.listdir(dir)
#         for file in files:
#             # self.sendLine((dir + '/' + file).encode("utf-8"))
#             # time.sleep(5)
#             with open(dir + '/' + file, 'rb') as f:
#                 msg = f.read()
#                 # self.sendLine(msg)
#                 # print(msg)
#                 self.sendLine(str(len(msg)).encode("utf-8"))
#                 self.transport.write(msg)
#                 break

#     def dataReceived(self, data):
#         print("receive data:",len(data))
                

# port = 9527
# serverFactory = Factory.forProtocol(TcpServer)
# reactor.listenTCP(port, serverFactory)
# print("#####", "Starting TCP Server on", port, "#####")
# reactor.run()

import pickle
import time
import open3d as o3d
import numpy as np

begin = time.time()
# pointCloud = o3d.io.read_point_cloud("D:/Download/8iVFBv2/longdress/Ply/longdress_vox10_1051.ply")
with open("D:/Download/8iVFBv2/longdress/Ply/longdress_vox10_1051.ply") as f:
    msg = f.read()
    print(len(msg) / 1024)
# p = pickle.dumps(pointCloud)
# l = pickle.loads(p)
# print(pointCloud.points)
# points = np.asarray(pointCloud.points)
# colors = np.asarray(pointCloud.colors)
# end = time.time()
# print ("io cost:",end-begin)

# begin = time.time()
# p_points = pickle.dumps(points)
# p_colors = pickle.dumps(colors)
# print(isinstance(p_colors,bytes))
# end = time.time()
# print("encode cost:", end-begin)

# begin = time.time()
# l_points = pickle.loads(p_points)
# l_colors = pickle.loads(p_colors)
# end = time.time()
# print("decode cost:", end-begin)
# print(l_points[0])

