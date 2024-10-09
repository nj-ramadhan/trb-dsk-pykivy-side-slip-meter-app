#include "BluetoothSerial.h"
#include <HardwareSerial.h>
#include <cstring>

BluetoothSerial SerialBT;
uint8_t address[7]  = {0x40, 0x91, 0x51, 0xFC, 0xCC, 0x36};
HardwareSerial mySerial(1);
byte receivedByte;

const int maxExpectedBytes = 29;
byte receivedData[maxExpectedBytes];
bool newDataAvailable = false;
uint64_t combinedValue = 0;
bool connected;

void setup() 
{
  pinMode(23, OUTPUT);
  Serial.begin(115200);
  mySerial.begin(9600, SERIAL_8N1, 16, 17);
}

void loop() 
{
  SerialBT.begin("ESP32test", true);
  connected = SerialBT.connect(address);
  digitalWrite(23, LOW);

  if(connected) 
  {
    digitalWrite(23, HIGH);
    if (mySerial.available()) 
    {
      memset(receivedData, 0, sizeof(receivedData));
      int byteCounter = 0;
      unsigned long startTime = millis();
      const unsigned long timeout = 1000;

      while (byteCounter < maxExpectedBytes && (millis() - startTime) < timeout) 
      {
        if (mySerial.available()) 
        {
          receivedByte = mySerial.read();
          receivedData[byteCounter] = receivedByte;
          byteCounter++;
        }
      }

      newDataAvailable = (byteCounter > 0);
    }

    if (newDataAvailable) 
    {
      // Print the data in hexadecimal format
      Serial.print("Received Data: ");
      for (int i = 0; i < maxExpectedBytes; i++)
      {
        Serial.print(receivedData[i], HEX);
        Serial.print(" ");
      }
      SerialBT.write(receivedData, maxExpectedBytes);
      Serial.println(" ");
      newDataAvailable = false;
      combinedValue = 0;
      while (mySerial.available()) 
      {
        mySerial.read();
      }
    }
  } 
  else 
  {
    while(!SerialBT.connected(10000)) 
    {
      Serial.println("disconnected");
      ESP.restart();
    }
  }
}