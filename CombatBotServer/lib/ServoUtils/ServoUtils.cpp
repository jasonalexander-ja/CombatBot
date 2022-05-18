#include <Arduino.h>
#include <ESP32Servo.h>


void SetupServos(const int servoPinList[8], Servo* servoList[8])
{
	for (int i = 0; i <= 3; ++i)
		ESP32PWM::allocateTimer(i);

	for (int i = 0; i <= 7; i = i + 1)
	{
		auto s = servoList[i];
		s->setPeriodHertz(50);
		s->attach(servoPinList[i], 500, 2400);
	}
}

void WriteToServos(const uint8_t positions[8], Servo* servoList[8])
{
	for (int i = 0; i <= 7; i++)
	{
		int pos = positions[i];
		Servo* s = servoList[i];
		if (pos == -1) continue;
		if (pos >= 180)
			s->write(180);
		else if(pos <= 0)
			s->write(0);
		else if(pos < 180 && pos > 0)
			s->write(pos);
	}
}
