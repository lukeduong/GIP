#include <SoftwareSerial.h>

#define DE 2
#define RE 3

SoftwareSerial mod(6,5);

void setup() 
{
  Serial.begin(9600);                   // initialize serial at baudrate 9600:
  mod.begin(4800);
  delay(1000);
  pinMode(RE, OUTPUT);
  pinMode(DE, OUTPUT);
  delay(10);
      //  (Pin 8 always LOW to receive value from Master)
}


void loop() 
{              
  char values[8]; // Make sure this matches the size sent by master
  int index = 0;
  
  delay(100);
  digitalWrite(DE,LOW);
  digitalWrite(RE,LOW);
  delay(10);
  while (mod.available() > 0 && index < sizeof(values) - 1) {
    values[index++] = mod.read();
    delay(10); // Give a little time for bytes to arrive
  }
  values[index] = '\0'; // Null-terminate the string

  Serial.println(values);

  delay(3000);
} 