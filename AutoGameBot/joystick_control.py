import pygame as pgame
from pygame.locals import *
import time
from multiprocessing import Queue
import global_val as glb

class joystick_control():
    def __init__(self):
        self.span_time = 1/glb.frame_num

    def init(self):
        pgame.joystick.init()
        self.joystick0 = pgame.joystick.Joystick(0)
        self.joystick0.init()
        pgame.init()

    def get_joycon(self,input_queue,serial_queue) :
        self.init()
        frame_count = 0
        get_data = {}
        get_data["press_button"] = []
        get_data["l_x"] = 0
        get_data["l_y"] = 0
        get_data["r_x"] = 0
        get_data["r_y"] = 0
        while True:
            s_time = time.time()
            eventlist = pgame.event.get()
            for e in eventlist:
                if e.type == pgame.locals.JOYAXISMOTION:
                    get_data["l_x"] = self.joystick0.get_axis(0)
                    get_data["l_y"] = self.joystick0.get_axis(1)
                    get_data["r_x"] = self.joystick0.get_axis(2)
                    get_data["r_y"] = self.joystick0.get_axis(3)
                elif e.type == pgame.locals.JOYBUTTONDOWN:
                    btn = [k for k, v in glb.joystick_button_dict.items() if v == e.button][0]
                    get_data["press_button"].append(btn)
                elif e.type == pgame.locals.JOYBUTTONUP:
                    btn = [k for k, v in glb.joystick_button_dict.items() if v == e.button][0]
                    get_data["press_button"].remove(btn)
            frame_count +=1
            input_queue.put(get_data)
            serial_queue.put(get_data)
            #print("get_data:",get_data)
            sleep_time = self.span_time - (time.time() - s_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
                

if __name__ == '__main__':
    input_queue = Queue()
    serial_queue = Queue()
    joystick = joystick_control(10)
    joystick.get_joycon(input_queue,serial_queue)


