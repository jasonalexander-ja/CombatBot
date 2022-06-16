#include <Arduino.h>

#include <WiFi.h>
#include <ESP32Servo.h>
#include <Preferences.h>

#include <ServoUtils.h>
#include <WifiUtils.h>


Servo servo0, servo1, servo2, servo3,
	servo4, servo5, servo6, servo7;

Servo* servoList[8]{
	&servo0, &servo1, &servo2, &servo3,
	&servo4, &servo5, &servo6, &servo7
};

int servoPinList[8]{
	13, 12, 14, 27,
	26, 25, 15, 2
};

Preferences preferences;

void MainLoop(WiFiClient server);
void SetupPrefs();

void setup() 
{
	Serial.begin(115200);
	SetupServos(servoPinList, servoList);
	SetupPrefs();
}

void SetupPrefs()
{
	preferences.begin("bot-app", false);
	String ssid = preferences.getString("SSID", "");
	String pswd = preferences.getString("PSWD", "");
	if (ssid == "") preferences.putString("SSID", " ");
	if (pswd == "") preferences.putString("PSWD", " ");
	preferences.end();
}

void loop() 
{
	WiFiServer server = SetupWifi(preferences);
	while(true)
	{
		WiFiClient client = server.available();
		if (client)
		{
			MainLoop(client);
		}
	}
}

void MainLoop(WiFiClient client)
{
	while (client.connected())
	{
		uint8_t data[8]{ 0, 0, 0, 0, 0, 0, 0, 0 };
		if (client.available())
		{
			client.read(data, 8);
			WriteToServos(data, servoList);
		}
	}
}
