#include <Arduino.h>
#include <WiFi.h>
#include <Preferences.h>

bool WifiStatusOk()
{
    switch (WiFi.status())
    {
        case WL_NO_SHIELD:
            return false;
        case WL_NO_SSID_AVAIL:
            return false;
        case WL_CONNECT_FAILED:
            return false;
        case WL_CONNECTION_LOST:
            return false;
        default:
            return true;
    }
}

String ReadLineBlocking()
{
    while (Serial.available() == 0);
    return Serial.readStringUntil('\n');
}

bool Connect(Preferences prefs)
{
    char ssid[51];
    char password[51];

    prefs.getString("SSID", "").toCharArray(ssid, 50);
    prefs.getString("PSWD", "").toCharArray(password, 50);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        if (!WifiStatusOk())
            return false;
    }
    return true;
}

bool ProcessMessage(Preferences prefs, String command)
{
	prefs.begin("bot-app", false);
    if (command == "STAT")
        Serial.println("SETUP");
    
    else if (command == "SET_SSID")
        prefs.putString("SSID", ReadLineBlocking());
    else if (command == "SET_PSWD")
        prefs.putString("PSWD", ReadLineBlocking());
    
    else if (command == "GET_SSID")
        Serial.println(prefs.getString("SSID", ""));

    else if (command == "GET_PSWD")
        Serial.println(prefs.getString("PSWD", ""));
    
    else if (command == "CONNECT")
    {
        if(Connect(prefs))
        {
            prefs.end();
            return true;
        }
        Serial.println("FAILED");
    }
    prefs.end();
    return false;
}

WiFiServer SetupWifi(Preferences preferences)
{
    while (true)
    {
        String command = ReadLineBlocking();
        if (ProcessMessage(preferences, command))
            break;
    }

    Serial.println("CONNECTED");
    Serial.println(WiFi.localIP());
    WiFiServer server(8088);
	server.begin();
    return server;
}

