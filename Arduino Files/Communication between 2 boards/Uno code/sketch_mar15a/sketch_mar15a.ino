/*************************************************** 
  This is a library for the Si1145 UV/IR/Visible Light Sensor

  Designed specifically to work with the Si1145 sensor in the
  adafruit shop
  ----> https://www.adafruit.com/products/1777

  These sensors use I2C to communicate, 2 pins are required to  
  interface
  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <SoftwareSerial.h>
#include "Adafruit_SI1145.h"


#define RE 8  
#define DE 7  
Adafruit_SI1145 uv = Adafruit_SI1145();

byte values[19];
SoftwareSerial mod(11, 10);

void setup() {
  Serial.begin(9600);
  mod.begin(4800);
  delay(1000);
  pinMode(RE, OUTPUT);
  pinMode(DE, OUTPUT);
  uv.begin();
}

void loop() {

  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);
  delay(10);

  long number = uv.readVisible();
  // Convert the number to a string
  char numberStr[8]; // 7 digits + null terminator
  snprintf(numberStr, sizeof(numberStr), "%ld", number);
  Serial.println(numberStr);
  // Send the number over RS485
  if (mod.write((uint8_t*)numberStr, sizeof(numberStr)-1) == sizeof(numberStr)-1) {
  }
  delay(500);
}