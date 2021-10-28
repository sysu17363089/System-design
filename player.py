import time
import numpy as np
import open3d as o3d
import threading

class PointCloudAttri():
    def __init__(self, points, colors):
        self.points = points
        self.colors = colors

class Player(threading.Thread):
    def __init__(self, queue):
        super(Player, self).__init__()
        self.queue = queue

    def run(self):
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.pointCloud = o3d.geometry.PointCloud()
        to_reset = True
        self.vis.add_geometry(self.pointCloud)
        while True:
            attri = self.queue.get()
            if isinstance(attri,str) and str(attri) == 'quit':
                break

            begin = time.time()
            self.pointCloud.points = attri.points
            self.pointCloud.colors = attri.colors
            self.vis.update_geometry(self.pointCloud)
            if to_reset:
                self.vis.reset_view_point(True)
                to_reset = False
            self.vis.poll_events()
            self.vis.update_renderer()
            end = time.time()
            print("draw cost:", end-begin)

