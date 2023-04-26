import sys
import os
import cv2
import pyocr
import numpy as np
from PIL import Image
import sys
import time
from multiprocessing import Process,Value,Queue,Manager
import global_val as glb

class capture_frame:
    def __init__(self, conf,is_training):
        self.device_num = conf["capture_borad"]
        self.quality = conf["capture_image_quality"]
        self.waste_frame_num  = conf["training_frame_num"] if is_training else conf["waste_frame_num"]

    def __del__(self):
        pass
        #self.capture.release()
        #cv2.destroyAllWindows()

    def connection_display(self):
        self.capture = cv2.VideoCapture(self.device_num)
        if not self.capture.isOpened():
            print("No Capture board found")
            sys.exit(1)
        self.capture.set(3, glb.origin_width//self.quality)
        self.capture.set(4, glb.origin_heigt//self.quality)
        
    def read_frame(self,frame_queue):
        frame_count = 0
        while True:
            ret, frame = self.capture.read()
            if ret is False:
                continue
            frame_count +=1
            if frame_count == self.waste_frame_num:
                frame_queue.put(frame)
                frame_count = 0
                cv2.imshow('temp',frame)
                cv2.waitKey(1)


    def capture_start(self,frame_queue):
        self.connection_display()
        self.read_frame(frame_queue)