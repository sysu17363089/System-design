import numpy as np
import threading, time
from player import Player, PointCloudAttri
import queue
from decode import Decoder

BEGIN = b'BEGIN' * 3
END = b'END' * 3
END_CONNETION = b'LOST' * 3

class BufferController(threading.Thread):
    def __init__(self, queue_):
        super(BufferController, self).__init__()
        self.queue = queue_
        self.decoder = Decoder()
        self.frame_queue = queue.Queue()
        self.buffer = bytes()
        self.video_player = Player(self.frame_queue)
        self.video_player.start()
        self.time = time.time()

    def run(self):
        while True:
            data = self.queue.get()
            self.buffer += data
            if BEGIN in self.buffer and END in self.buffer:
                curr = time.time()
                print("get msg:", curr-self.time)
                self.time = curr
                
                begin_index = self.buffer.find(BEGIN) + len(BEGIN)
                end_index = self.buffer.find(END)
                content = self.buffer[begin_index: end_index]

                curr = time.time()
                print("deal msg:", curr-self.time)
                self.time = curr

                self.decoder.decode(content)
                attri = PointCloudAttri(self.decoder.get_points(), self.decoder.get_colors()) 
                self.frame_queue.put(attri)
                self.buffer = self.buffer[end_index + len(END):]
        
            

