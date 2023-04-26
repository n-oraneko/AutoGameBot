
import sys
import yaml
import time
from multiprocessing import Process,Value,Queue,Manager

import global_val as glb
import capture_frame
import analyze_frame
import collect_dataset
import serial_control
import joystick_control
import argparse

parser = argparse.ArgumentParser(description="自動操作AI Bot")
parser.add_argument('--training',help="学習モード",action='store_true')

with open('./conf/conf.yml' ,'r', encoding="utf-8") as file:
    conf = yaml.safe_load(file)

def operation_start():
    capture = capture_frame.capture_frame(conf["capture"],False)
    analyze = analyze_frame.analyze_frame(conf["button_threshold"],conf["stick_bias"])
    serial = serial_control.serial_control(conf["baudrate"],conf["serial_port"],conf["mapping"])

    frame_queue = Queue()
    serial_queue = Queue()
    glb.processes = []
    glb.processes.append(Process(target=capture.capture_start,args=(frame_queue,)))
    glb.processes.append(Process(target=analyze.analyze,args=(frame_queue,serial_queue)))
    glb.processes.append(Process(target=serial.control,args=(serial_queue,)))
    for i in range(len(glb.processes)):
        glb.processes[i].start()
    for i in range(len(glb.processes)):
        glb.processes[i].join()

def collect_data_start():
    capture = capture_frame.capture_frame(conf["capture"],True)
    joystick = joystick_control.joystick_control()
    collect = collect_dataset.collect_dataset(conf["stick_thresholed"])
    serial = serial_control.serial_control(conf["baudrate"],conf["serial_port"],conf["mapping"])

    frame_queue = Queue()
    input_queue = Queue()
    serial_queue = Queue()
    glb.processes = []
    glb.processes.append(Process(target=capture.capture_start,args=(frame_queue,)))
    glb.processes.append(Process(target=joystick.get_joycon,args=(input_queue,serial_queue)))
    glb.processes.append(Process(target=collect.collect_data,args=(frame_queue,input_queue)))
    glb.processes.append(Process(target=serial.control,args=(serial_queue,)))

    for i in range(len(glb.processes)):
        glb.processes[i].start()
    for i in range(len(glb.processes)):
        glb.processes[i].join()

if __name__ == "__main__":
    args = parser.parse_args()
    if args.training:
        collect_data_start()
    else:
        operation_start()

