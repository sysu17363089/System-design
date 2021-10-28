import json
import open3d as o3d
import numpy as np
import os 
from player import Player, PointCloudAttri
import queue, time
from  decode import Decoder

def show_video():
    dir = "D:/Download/8iVFBv2/longdress/Ply"
    files = os.listdir(dir)
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    pointCloud = o3d.geometry.PointCloud()
    to_reset = False
    vis.add_geometry(pointCloud)


    for f in files:
        # pointCloud.clear()
        vis.remove_geometry(pointCloud)
        pointCloud = o3d.io.read_point_cloud(dir + '/' + f)
        # pointCloud.__iadd__(ply)
        # ply = np.asarray(ply.points).reshape((-1, 3))
        vis.add_geometry(pointCloud)
        
        # vis.update_geometry(pointCloud)
        # if to_reset:
        #     vis.reset_view_point(True)
        #     to_reset = False
        
        vis.poll_events()
        vis.update_renderer()

def show_pic():
    pcd = o3d.io.read_point_cloud("D:/Download/8iVFBv2/longdress/Ply/longdress_vox10_1051.ply")
    
    o3d.visualization.draw_geometries([pcd])
                                    

def test_player():
    q = queue.Queue()
    video_player = Player(q)
    video_player.start()
    dir = "D:/Download/8iVFBv2/longdress/Ply"
    begin = time.time()
    files = os.listdir(dir)
    for f in files[:20]:
        pointCloud = o3d.io.read_point_cloud(dir + '/' + f)
        q.put(pointCloud)
    q.put('quit')
    end = time.time()
    print('test:', end-begin)
    video_player.join()

def test_player2():
    q = queue.Queue()
    video_player = Player(q)
    video_player.start()
    dir = "D:/Download/8iVFBv2/longdress/Ply"
    begin = time.time()
    files = os.listdir(dir)
    for f in files[:20]:
        with open(dir + '/' + f, 'rb') as f:
            msg = f.read()
        # decoder = Decoder(msg)
        # attri = PointCloudAttri(decoder.get_points(), decoder.get_colors())
        string = msg.decode()
        lines = string.splitlines(keepends=False)
        data = lines[14:]
        # points, colors = loop(data)
        # attri = PointCloudAttri(o3d.utility.Vector3dVector(points), o3d.utility.Vector3dVector(colors))
        # q.put(attri)
    q.put('quit')
    end = time.time()
    print('test2:', end-begin)
    video_player.join()

def test_player3():
    q = queue.Queue()
    video_player = Player(q)
    video_player.start()
    dir = "D:/Download/8iVFBv2/longdress/Ply"
    begin = time.time()
    files = os.listdir(dir)
    for f in files[:20]:
        pointCloud = o3d.io.read_point_cloud(dir + '/' + f)
        dic = {'points': np.asarray(pointCloud.points).tolist(), 'colors': np.asarray(pointCloud.colors).tolist()}
        encode = json.dumps(dic)
        decode = json.loads(encode)
        attri = PointCloudAttri(o3d.utility.Vector3dVector(decode['points']), o3d.utility.Vector3dVector(decode['colors']))
        q.put(attri)
    q.put('quit')
    end = time.time()
    print('test:', end-begin)
    video_player.join()

# test_player()
# test_player2()
test_player3()

# # file = "C:/Users/cak/Desktop/paper/open3d/models/b.ply"
# def return_list():
#     with open(file, 'rb') as f:
#         msg = f.read()
#         yield msg if msg != b'' else b' '
# for msg in return_list():
#     # print(msg)
#     # print(msg.encode())
#     decode = msg.decode()
# # print(len(decode))
# # print(decode[0:10])
# ans = decode.splitlines(keepends=False)
# # 该ply文件前14行为解释信息, end header为结束符
# print(ans[13])
# print(ans[14])
# nums = ans[14].split()
# print(nums)

