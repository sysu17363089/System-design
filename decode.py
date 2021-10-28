import os
import open3d as o3d
import time, pickle
from multiprocessing.pool import ThreadPool
import numpy as np
from numba import jit

INTER = b'INTER' * 3

class Decoder():
    # def decode(self, binary):
    # # 该ply文件前14行为解释信息, end header为结束符
    #     string = binary.decode()
    #     lines = string.splitlines(keepends=False)
    #     self.data = lines[14:]
    #     begin = time.time()
    #     self.generate()
    #     end = time.time()
    #     print("decode cost:", end-begin)

    def generate(self):
        self.points = []
        self.colors = []
        # print("data:",self.data[:20])
        for index, line in enumerate(self.data) :
            nums = line.split()
            if len(nums) != 6:
                print("abnormal data:",index, 'whole length:', len(self.data))
                # print("nums:", nums)
                continue
            self.points.append([float(nums[0]), float(nums[1]), float(nums[2])])
            self.colors.append([float(nums[3])/255.0, float(nums[4])/255.0, float(nums[5])/255.0])

    def decode(self, binary):
        if not INTER in binary:
            print("Wrong")
            return
        begin = time.time()
        point_end = binary.find(INTER)
        color_begin = point_end + len(INTER)
        self.points = pickle.loads(binary[: point_end])
        self.colors = pickle.loads(binary[color_begin:])
        end = time.time()
        print("pickle decode cost:",end-begin)

    def get_colors(self):
        return o3d.utility.Vector3dVector(self.colors)

    def get_points(self):
        return o3d.utility.Vector3dVector(self.points)


class Decoder_old():
    def __init__(self, binary):
    # 该ply文件前14行为解释信息, end header为结束符
        string = binary.decode()
        lines = string.splitlines(keepends=False)
        self.string = string
        self.data = lines[14:]
        print("lines:",lines[:14])
        begin = time.time()
        self.generate()
        end = time.time()
        print("decode cost:", end-begin)

    def generate(self):
        self.points = []
        self.colors = []
        for line in self.data:
            nums = line.split()
            if len(nums) != 6:
                # print(self.string)
                # print("nums:", nums)
                continue
            self.points.append([float(nums[0]), float(nums[1]), float(nums[2])])
            self.colors.append([float(nums[3])/255.0, float(nums[4])/255.0, float(nums[5])/255.0])

    def get_colors(self):
        return o3d.utility.Vector3dVector(self.colors)

    def get_points(self):
        return o3d.utility.Vector3dVector(self.points)
    

# @jit(nopython=True)
# def loop(data):
#     points = []
#     colors = []
#     for line in data:
#         nums = line.split()
#         if len(nums) != 6:
#             continue
#         points.append([float(nums[0]), float(nums[1]), float(nums[2])])
#         colors.append([float(nums[3])/255.0, float(nums[4])/255.0, float(nums[5])/255.0])
#     return points, colors

# @jit(nopython=True)
# def loop(data):
#     length = len(data)
#     points = np.zeros((length,3), dtype=float)
#     colors = np.zeros((length,3), dtype=float)
#     for row, line in enumerate(data):
#         nums = line.split()
#         for i in range(3):
#             points[row][i] = nums[i]
#             colors[row][i] = nums[i+3]
#     return points, colors

# file = "D:/Download/8iVFBv2/longdress/Ply/longdress_vox10_1054.ply"
# with open(file, 'rb') as f:
#     msg = f.read()

# pc = o3d.io.read_point_cloud("D:/Download/8iVFBv2/longdress/Ply/longdress_vox10_1051.ply")
# decode = Decoder(msg)
# vis = o3d.visualization.Visualizer()
# vis.create_window()
# pointCloud = o3d.geometry.PointCloud()

# pointCloud.colors = decode.get_colors()
# pointCloud.points = decode.get_points()

# # pointCloud.colors = pc.colors
# # pointCloud.points = pc.points
# vis.add_geometry(pointCloud)
# vis.poll_events()
# vis.update_renderer()








# def generate(line):
#     points = []
#     colors = []
#     nums = line.split()
#     if len(nums) != 6:
#         # print(self.string)
#         print(nums)
        
#     points.append([float(nums[0]), float(nums[1]), float(nums[2])])
#     colors.append([float(nums[3])/255.0, float(nums[4])/255.0, float(nums[5])/255.0])

# dir = "D:/Download/8iVFBv2/longdress/Ply"
# begin = time.time()
# files = os.listdir(dir)
# pool = ThreadPool(4)  # 创建一个线程池
# for file in files:
#     with open(dir + '/' + file, 'rb') as f:
#         msg = f.read()
#     msg = msg.decode()
#     # decode_time = time.time()
#     # print('decode_time:',decode_time)
#     lines = msg.splitlines(keepends=False)
#     lines = lines[14:]
    
#     pool.map(generate, lines)  # 往线程池中填线程
#     # pool.close()  # 关闭线程池，不再接受线程
    

# # for line in lines:
# #     generate(line)

# pool.join() 
# end = time.time()
# # print("deal points time: ", end - decode_time)
# print("whole time:", end - begin)