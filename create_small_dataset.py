import open3d
import numpy as np
import os

dir = "models"
files = os.listdir(dir)
for index, file in enumerate(files):
    source = open3d.io.read_point_cloud(dir + '/' + file)
    low_res = source.uniform_down_sample(10)
    new_pcd = open3d.geometry.PointCloud()
    new_pcd.points = low_res.points
    open3d.io.write_point_cloud("small_dateset/"+str(index)+'.ply', new_pcd)
