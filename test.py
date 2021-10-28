import open3d
name = "down8_1054"
ply = name + '.ply'
xyz = name + '.xyz'

test = "from_ply.xyz"


source = open3d.io.read_point_cloud(ply)
print(source.points)
# source.paint_uniform_color([1, 0.706, 0])
# open3d.visualization.draw_geometries([source])

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
        
