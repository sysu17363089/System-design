import open3d as o3d
import trimesh
import numpy as np

pcd = o3d.io.read_point_cloud("models/longdress_vox10_1054.ply")
# print(len(pcd.points))
pcd = pcd.uniform_down_sample(8)

# pcd.estimate_normals()

# # # estimate radius for rolling ball
# distances = pcd.compute_nearest_neighbor_distance()
# avg_dist = np.mean(distances)

# dist = 1.5   
# radius = dist * avg_dist
# mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
#         pcd,
#         o3d.utility.DoubleVector([radius, radius * 2]))
# print("dist: ", dist, " radius: ", radius, "mesh: ", mesh)

# o3d.visualization.draw_geometries([mesh])
o3d.io.write_point_cloud("down8_1054.ply", pcd)

# tri_mesh = trimesh.Trimesh(np.asarray(mesh.vertices), np.asarray(mesh.triangles),
#                           vertex_normals=np.asarray(mesh.vertex_normals))

# print(trimesh.convex.is_convex(tri_mesh))