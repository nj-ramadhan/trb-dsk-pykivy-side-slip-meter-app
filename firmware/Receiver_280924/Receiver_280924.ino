#include "BluetoothSerial.h"
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

const int maxExpectedBytes = 29;
byte receivedData[maxExpectedBytes];
bool newDataAvailable = false;
uint64_t combinedValue = 0;

void setup() 
{
  SerialBT.begin("receiver");
  Serial.begin(115200);
  pinMode(15, OUTPUT);
}

void loop() 
{  
  digitalWrite(15, LOW);  
  if (SerialBT.available()) 
  {
    memset(receivedData, 0, sizeof(receivedData));

    int byteCounter = 0;
    unsigned long startTime = millis();
    const unsigned long timeout = 1000;

    while (byteCounter < maxExpectedBytes && (millis() - startTime) < timeout) 
    {
      if (SerialBT.available()) 
      {
        byte receivedByte = SerialBT.read();
        receivedData[byteCounter] = receivedByte;
        byteCounter++;
      }
    }

    newDataAvailable = (byteCounter > 0);
  }

  if (newDataAvailable) 
  {
    for (int i = 4; i < 25; i++) 
    {
      Serial.print(receivedData[i], HEX);
      Serial.print(" ");
    }
    Serial.println();
    newDataAvailable = false;
    combinedValue = 0;
    digitalWrite(15, HIGH);
    delay(300);
    while (SerialBT.available()) 
    {
      SerialBT.read();
    }
  }
}