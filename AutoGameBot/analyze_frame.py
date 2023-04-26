
from multiprocessing import Process,Value,Queue,Manager
import predict_model
import global_val as glb

import numpy as np
import cv2
from PIL import Image

class analyze_frame(object):
    def __init__(self,button_threshold,stick_bias):
        self.button_threshold = button_threshold
        self.stick_bias = stick_bias
    def __del__(self):
        pass

    def analyze(self,frame_queue,serial_queue):
        prediction = predict_model.prediction_model()
        prediction.training_init()
        while True:
            try:
                frame = frame_queue.get()
                color_converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image=Image.fromarray(color_converted)
                predict_res = prediction.predict(pil_image)
                print('analyze_frame:',predict_res)
                get_data = {}
                get_data["press_button"] = []
                for button in glb.joystick_button_dict:
                    if predict_res[button] > self.button_threshold[button]:
                        get_data["press_button"].append(button)
                get_data["l_x"] = (-predict_res["l_x_u"] + predict_res["l_x_d"]) * self.stick_bias
                get_data["l_y"] = (-predict_res["l_y_u"] + predict_res["l_y_d"]) * self.stick_bias
                get_data["r_x"] = (-predict_res["r_x_u"] + predict_res["r_x_d"]) * self.stick_bias
                get_data["r_y"] = (-predict_res["r_y_u"] + predict_res["r_y_d"]) * self.stick_bias
                serial_queue.put(get_data)
                print(get_data)
                while not frame_queue.qsize() == 0:
                    frame_queue.get()

            except frame_queue.Empty:
                print('analyze:not yet reach frame')
                pass
            except Exception as e:
                print('analyze:',e)
                pass
                

    def check_color(self,frame,conf):
        for c in conf:
            color = c["color_value"]
            reliability = c["reliability"]
            trim = c["image"]
            y_start = int(trim[0] * len(frame) /  self.orign_height)
            y_end = int(trim[1] * len(frame) /  self.orign_height)
            x_start = int(trim[2] * len(frame[0]) /  self.orign_width)
            x_end = int(trim[3] * len(frame[0]) /  self.orign_width)
            if y_start >= y_end or x_start >= x_end:
                return False
            tmp_frame = frame[y_start:y_end,x_start:x_end]
            average_color_row = np.average(tmp_frame, axis=0)
            average_color = np.average(average_color_row, axis=0)

            if (average_color[0]-reliability < color[0] and 
                color[0] < average_color[0]+reliability and
                average_color[1]-reliability < color[1] and 
                color[1] < average_color[1]+reliability and
                average_color[2]-reliability < color[2] and 
                color[2] < average_color[2]+reliability ):
                    continue
            return False
        return True
