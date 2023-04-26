/*
Copyright (c) 2023 noraneko
released under the MIT license
https://opensource.org/licenses/mit-license.php
*/

#pragma once

#include "./SwitchControlLibrary/SwitchControlLibrary.h"

void resetData();
void setButton(uint16_t high_bit_button,int16_t low_bit_button);
void setHat(uint8_t hat) ;
void setLeftStick(uint8_t lx, uint8_t ly);
void setRightStick(uint8_t rx, uint8_t ry);
void sendSetSwitch(uint16_t delayTime);