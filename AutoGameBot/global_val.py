
frame_num = 30
origin_width = 1920
origin_heigt = 1080
image_quality = 2

arduino_low_button= {
    'Y' : 0x0001,
    'B' : 0x0002,
    'A' : 0x0004,
    'X' : 0x0008,
    'L' : 0x0010,
    'R' : 0x0020,
    'ZL' : 0x0040,
    'ZR' : 0x0080,
}
arduino_high_button={
    'MINUS' : 0x01,#0x0100,
    'PLUS' : 0x02,#0x0200,
    'LCLICK' : 0x04,#0x0400
    'RCLICK' : 0x08,#0x0800
    'HOME' : 0x10,#0x1000
    'CAPTURE' : 0x20,#0x2000
}

arduino_hat = {
    'UP' : 0x00,
    'UP_RIGHT' : 0x01,
    'RIGHT' : 0x02,
    'DOWN_RIGHT' : 0x03,
    'DOWN' : 0x04,
    'DOWN_LEFT' : 0x05,
    'LEFT' : 0x06,
    'UP_LEFT' : 0x07,
    'NEUTRAL' : 0x08,
}

joystick_button_dict={
    'Y' : 3,
    'B' : 1,
    'A' : 0,
    'X' : 2,
    'L' : 9,
    'R' : 10,
    'ZL' : -1,
    'ZR' : -1,
    'MINUS': 4, 
    'PLUS': 6 ,
    'LCLICK': 7, 
    'RCLICK': 8,
    'HOME' :5 ,
    'CAPTURE': 15, 

    'UP': 11 ,
    'RIGHT':14 ,
    'DOWN': 12 ,
    'LEFT': 13 ,
    
}

#weight 
model_classes_list={
    'Y' : 1,
    'B' : 1,
    'A' : 1,
    'X' : 1,
    'L' : 1,
    'R' : 1,
    'ZL' : 1,
    'ZR' : 1,
    'MINUS': 1, 
    'PLUS': 1 ,
    'LCLICK': 1, 
    'RCLICK': 1,
    'HOME' :1 ,
    'CAPTURE': 1, 

    'UP': 1 ,
    'RIGHT':1 ,
    'DOWN': 1 ,
    'LEFT': 1,
    "l_x_u": 1,
    "l_y_u": 1,
    "r_x_u": 1,
    "r_y_u": 1,
    "l_x_d": 1,
    "l_y_d": 1,
    "r_x_d": 1,
    "r_y_d": 1
}
