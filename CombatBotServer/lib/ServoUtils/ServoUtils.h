#include <Arduino.h>
#include <ESP32Servo.h>


void SetupServos(const int servoPinList[8], Servo* servoList[8]);

void WriteToServos(const uint8_t positions[8], Servo* servoList[8]);
