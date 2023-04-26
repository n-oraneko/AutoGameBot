import pygame as pgame
from pygame.locals import *
import time
import cv2
import global_val as glb
import json
import os

class collect_dataset():
    def __init__(self,stick_thresholed):
        self.l_stick_thresholed = stick_thresholed['l_stick']
        self.r_stick_thresholed = stick_thresholed['r_stick']
        os.makedirs('dataset', exist_ok=True)
        os.makedirs('dataset/images', exist_ok=True)
        os.makedirs('dataset/labels', exist_ok=True)

    def collect_data(self,frame_queue,input_queue) :
        ##èâä˙ílÇì«Çﬁ
        frame = frame_queue.get()
        control = input_queue.get()

        while True:
            try:
                frame = frame_queue.get()
                while not input_queue.qsize() == 0:
                    control = input_queue.get()
                file_name = str(time.time())
                cv2.imwrite('dataset/images/'+file_name+'.jpg', frame)
                label = {}
                for button in glb.joystick_button_dict:
                    label[button] = 0 
                    if button in control["press_button"]:
                        label[button] = 1
                label["l_x_u"] = 1 if control["l_x"] < -self.l_stick_thresholed else 0
                label["l_y_u"] = 1 if control["l_y"] < -self.l_stick_thresholed else 0
                label["r_x_u"] = 1 if control["l_x"] < -self.r_stick_thresholed else 0
                label["r_y_u"] = 1 if control["l_y"] < -self.r_stick_thresholed else 0
                
                label["l_x_d"] = 1 if control["l_x"] > self.l_stick_thresholed else 0
                label["l_y_d"] = 1 if control["l_y"] > self.l_stick_thresholed else 0
                label["r_x_d"] = 1 if control["l_x"] > self.r_stick_thresholed else 0
                label["r_y_d"] = 1 if control["l_y"] > self.r_stick_thresholed else 0

                with open('dataset/labels/'+file_name+'.json', mode="wt", encoding="utf-8") as f:
	                json.dump(label, f, ensure_ascii=False)
                while not frame_queue.qsize() == 0:
                    frame_queue.get()
                

            except Exception as e:
                print('err collect:',e)
                pass


