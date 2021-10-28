import trimesh
import pyrender
import time
import numpy as np



fuze_trimesh = trimesh.load('obj/Handgun_obj.obj')
# fuze_trimesh = trimesh.load("Handgun_ply.ply")

fuze_trimesh = trimesh.load("pyrender/examples/models/fuze.obj")
wood_trimesh = trimesh.load("pyrender/examples/models/wood.obj")

mesh = pyrender.Mesh.from_trimesh(fuze_trimesh)
wood_mesh = pyrender.Mesh.from_trimesh(wood_trimesh)

scene = pyrender.Scene()

viewer = pyrender.Viewer(scene, use_raymond_lighting=True, run_in_thread=True)

meshes = [mesh, wood_mesh]*100

i = 0
# while True:
#     viewer.render_lock.acquire()
#     # scene.set_pose(fuze_node, pose)
#     # scene.add_node(wood_node)
#     # scene.clear()
#     scene.remove_node(fuze_node)
#     scene.add_node(wood_node)
#     viewer.render_lock.release()
#     time.sleep(10)
#     i += 1
#     if i==10:
#         break

node = pyrender.Node()
scene.add_node(node)
for m in meshes:
    
    viewer.render_lock.acquire()
    scene.remove_node(node)
    node = pyrender.Node(mesh=m, translation=np.array([0.1, 0.15, i]))
    scene.add_node(node)
    viewer.render_lock.release()
    i+=0.1
    if len(scene.nodes) == 0:
        break
    time.sleep(1)


