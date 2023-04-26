import yaml
import time
import serial
import global_val as glb
from multiprocessing import Queue

class serial_control:
    def __init__(self, baudrate,port,mapping):
        self.port = port
        self.baudrate = baudrate
        self.span_time = int(1/glb.frame_num *1000) #ms
        self.mapping = mapping

    def __del__(self):
        self.ser.close()

    def connection_fat32(self,port,baudrate):
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate
        self.ser.port = port
        self.ser.setDTR(False) 
        self.ser.open()
        
    def control(self,serial_queue):
        self.connection_fat32(self.port,self.baudrate)
        while True:
            try:
                control = serial_queue.get()
                #print("serial_control:",control)
                low_btn,high_btn,hat = self.set_button(control["press_button"])
                l_x,l_y,r_x,r_y = self.lean_stick(control["l_x"],control["l_y"],control["r_x"],control["r_y"])
                send_bytes = bytes([0xff,high_btn,low_btn,hat,l_x,l_y,r_x,r_y,self.span_time])
                self.ser.write(send_bytes)
                self.ser.flush()
                #print("send:",send_bytes)
                while True:
                    if self.ser.in_waiting > 0:
                        data = self.ser.read_all()
                        print("back:",data)
                        break
                    else: break
            except Exception as e:
                print('err serial:',e)
                pass

    def set_button(self,buttons):
        low_btn = 0
        high_btn = 0
        hat = 0x08
        for button in  buttons:
            if not button in self.mapping["control"]:
                continue
            b = self.mapping["control"][button]
            if b in glb.arduino_low_button:
                low_btn |= glb.arduino_low_button[b]
            if b in glb.arduino_high_button:
                high_btn |= glb.arduino_high_button[b]
            if b in glb.arduino_hat:
                hat = glb.arduino_hat[b]
        return low_btn,high_btn,hat

    def lean_stick(self,l_x,l_y,r_x,r_y):
        if not self.mapping["stick"]["l_stick"]:
            l_x = 0
            l_y = 0
        if not self.mapping["stick"]["r_stick"]:
            r_x = 0
            r_y = 0

        try:
            l_x = (int)((l_x+1) * 128)
            l_y = (int)((l_y+1) * 128)
            r_x = (int)((r_x+1) * 128)
            r_y = (int)((r_y+1) * 128)
            if l_x <0:
                l_x = 0
            if l_x >254:
                l_x = 254
            if l_y <0:
                l_y = 0
            if l_y >254:
                l_y = 254
            if r_x <0:
                r_x = 0
            if r_x >254:
                r_x = 254
            if r_y <0:
                r_y = 0
            if r_y >254:
                r_y = 254
            return  l_x,l_y,r_x,r_y
        except:
            print(l_x,l_y,r_x,r_y)


