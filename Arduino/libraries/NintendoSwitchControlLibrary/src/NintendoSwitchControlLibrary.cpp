/*
Copyright (c) 2023 noraneko
released under the MIT license
https://opensource.org/licenses/mit-license.php
*/


void resetData(){
    SwitchControlLibrary().clearButton();
    SwitchControlLibrary().moveLeftStick(Stick::NEUTRAL, Stick::NEUTRAL);
    SwitchControlLibrary().moveRightStick(Stick::NEUTRAL, Stick::NEUTRAL);
}

void setButton(uint16_t high_bit_button,int16_t low_bit_button) {
    SwitchControlLibrary().pressButton(high_bit_button<<8);
    SwitchControlLibrary().pressButton(low_bit_button);
}
void setHat(uint8_t hat) {
    SwitchControlLibrary().pressHatButton(hat);
}
void setLeftStick(uint8_t lx, uint8_t ly) {
    SwitchControlLibrary().moveLeftStick(lx, ly);
}

void setRightStick(uint8_t rx, uint8_t ry) {
    SwitchControlLibrary().moveRightStick(rx, ry);
}

void sendSetSwitch(uint16_t delayTime){
    SwitchControlLibrary().sendReport();
    delay(delayTime);
}