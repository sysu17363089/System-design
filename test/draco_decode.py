import DracoPy
import os
import json
import numpy as np

# with open("drc/out.drc", "rb") as draco_file:
#     file_content = draco_file.read()
#     point_cloud_object = DracoPy.decode_point_cloud_buffer(file_content)
#     points = point_cloud_object.points
#     # colors = point_cloud_object.colors
#     print(point_cloud_object.encoding_options)


news = {'points': np.array([123,123,123]).tolist(),
        'colors': [123,123,123]
       }
# print(list(np.array([123,123,123])))
 
json_encode = json.dumps(news)
 
json_decode = json.loads(json_encode)
print (json_decode)
print(json_decode['points'][0])


