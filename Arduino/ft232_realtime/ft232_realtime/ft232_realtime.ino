#include <NintendoSwitchControlLibrary.h>

void setup() {
  Serial1.begin(115200);
    //pushButton(Button::HOME, 500, 4);
  SwitchControlLibrary();
  for (int i = 0; i < 3; ++i) {
    pushButton(Button::HOME);
    delay(200);
    pushUpButton(Button::HOME);
    delay(200);
  }
}

int get_byte(){
  while(true){
    if(Serial1.available()) {
      int c = Serial1.read();
      return c;
    }
  }
}

void loop() {
  /* When received signals */
  if(Serial1.available()) {
    int c = Serial1.read();
    if (c == 0xff){
      resetData();
      int high_bit_button = get_byte();
      int low_bit_button = get_byte();
      int hats = get_byte();
      int lx = get_byte();
      int ly = get_byte();
      int rx = get_byte();
      int ry = get_byte();
      int delayTime = get_byte();
      setButton(high_bit_button,low_bit_button);
      setHat(hats);
      setLeftStick(lx,ly) ;
      setRightStick(rx,ry);
      sendSetSwitch(delayTime);
      Serial1.write("Command Start");
      Serial1.write(high_bit_button);
      Serial1.write(low_bit_button);
      Serial1.write(hats);
      Serial1.write(lx);
      Serial1.write(ly);
      Serial1.write(rx);
      Serial1.write(ry);
      Serial1.write(delayTime);
      Serial1.println("Command End");
    }
  }
  else{
    //delay(10);
    //Serial1.println("Command Not Commin");
  }
}
