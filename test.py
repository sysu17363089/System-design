import open3d
import numpy as np
import time

name = "models/longdress_vox10_1051.ply"


source = open3d.io.read_point_cloud(name)
low_res = source.uniform_down_sample(10)
high_res = open3d.geometry.PointCloud()
high_res.points = source.points

begin = time.time()
low_tree = open3d.geometry.Octree(max_depth=8)
low_tree.convert_from_point_cloud(low_res)

high_tree = open3d.geometry.Octree(max_depth=7)
high_tree.convert_from_point_cloud(high_res, size_expand=0)
high_points = np.asarray(high_res.points)
high_colors = np.zeros(high_points.shape)
# count = 10
# for point in high_points:
#     node = low_tree.locate_leaf_node(point)
#     print(node)
#     if node == None:
#         break
count = 0
def print_node(node,info):
    if type(node) == open3d.geometry.OctreePointColorLeafNode:
        indices = node.indices
        color_container = []
        uncolored_points = []
        for i in indices:
            point = high_points[i]
            leaf_node, node_info = low_tree.locate_leaf_node(point)
            if type(leaf_node) == open3d.geometry.OctreePointColorLeafNode:
                color_container.append(list(leaf_node.color))
                high_colors[i, :] = leaf_node.color
            else:
                if len(color_container) > 0:
                    container_array = np.asarray(color_container)
                    high_colors[i, :] = [np.mean(container_array[:,0]), 
                                        np.mean(container_array[:,1]),
                                        np.mean(container_array[:,2])]
                else:
                    uncolored_points.append(i)
        for point in uncolored_points:
            if len(color_container) > 0:
                container_array = np.asarray(color_container)
                high_colors[point, :] = [np.mean(container_array[:,0]), 
                                    np.mean(container_array[:,1]),
                                    np.mean(container_array[:,2])]
            else:
                global count
                count += 1

    # print("info",info)
high_tree.traverse(print_node)
high_res.colors = open3d.utility.Vector3dVector(high_colors)
end = time.time()
print("Time cost: ", end-begin)
print(count, high_res.points)
# print(high_colors)





# source.paint_uniform_color([1, 0.706, 0])
open3d.visualization.draw_geometries([high_res])
open3d.visualization.draw_geometries([low_res])

# open3d.io.write_point_cloud("from_ply.xyz", source)
# # 
# import numpy as np
# import pandas as pd
# import h5py
# import cv2

# # def show_img(img):
# #     cv2.imshow('img', img)
# #     cv2.waitKey(0)
# #     cv2.destroyAllWindows()

# file = 'D:/paper_about/PUGAN_poisson_256_poisson_1024.h5'
# f = h5py.File(file, 'r')
# for key in f.keys():
#     print(f[key].name)
#     print(f[key].shape)
#     # print(f[key])
#     # for i in range(len(f[key])):
#     #     pic = f[key][i, :, :]
#     #     print(pic)
        
