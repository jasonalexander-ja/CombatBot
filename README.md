## Combat Bot

This is the codebase intended for use with 8 servo ultralight walking 
combat bot. 

The code is seperated into 2 applications, the bot and the client,
the bot being an ESP32 based on the Espressif ESP32 Dev board,
the client is a cross platform Python desktop application.

The client acts as a controller for the bot, initially syncing 
via USB serial and then communicating wirelessy over a WiFi
connection. 


## Hardware 

The bot consists of 8 servos, nominally these are attached to GPIO 
pins `13, 12, 14, 27, 26, 25, 15, 2` on the ESP32. 

The design is to have 4 of these servos attached together in 
a rectangle, with the armatures facing the opposite ends, 
this forms the up and down movements of the legs, with the body of 
the joined servos acting as a chassis for the ESP32 and batteries.

Attached to the armatures of these servos are 4 more servos 
controlling forwards and backwards movements of the legs. 

The bot is running a thin server, once it has synced up,
it will listen over TCP for 8 numbers between 0 and 180 for the
positions of each servo repectively. 

### Hardware syncing 

On power on or on reset, the bot will enter setup state, this will
listen to commands over a serial USB connection, commands should be 
new line separated, `\n`, with setting commands should be a new line
between the command and the data. 

#### Setting WiFi SSID
```
SET_SSID\n
your_networks_ssid\n
```

#### Setting WiFi password
```
SET_PSWD\n
your_networks_password\n
```

#### Getting WiFi SSID
```
GET_SSID\n
```
Bot response
```
stored_network_ssid\n
```

#### Getting WiFi password
```
GET_PSWD\n
```
Bot response
```
stored_network_password\n
```

#### Connect to WiFi with provided details 
```
CONNECT\n
```
Bot response(s)
```
CONNECTED\n
ip.address\n
```
Or
```
FAILED\n
```
