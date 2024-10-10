#include <SoftwareSerial.h>
#include "Adafruit_SI1145.h"
#include "Adafruit_LTR390.h"
#include <Adafruit_AHTX0.h>

#define RE 9  //pin RE 8 
#define DE 10  //pin DE 7 

#define DE_2 5
#define RE_2 6

const byte query[] = {0x01,0x03,0x00,0x00,0x00,0x07,0x04,0x08};
const byte_2 query[] = {0x01,0x03,0x00,0x00,0x00,0x07,0x04,0x08};
byte values[19];
byte values[19];

SoftwareSerial mod(8, 11);  //pin RO 10 DI 11
SoftwareSerial mod(4, 7);  //pin RO 10 DI 11

Adafruit_SI1145 uv = Adafruit_SI1145();
Adafruit_LTR390 ltr = Adafruit_LTR390();
Adafruit_AHTX0 aht;

void setup() {
  Serial.begin(9600);
  mod.begin(4800);
  uv.begin();
  delay(10);
  ltr.begin();
  delay(10);
  aht.begin();
  delay(1000);
  pinMode(RE, OUTPUT);
  pinMode(DE, OUTPUT);
  ltr.setGain(LTR390_GAIN_6);
  ltr.setResolution(LTR390_RESOLUTION_18BIT);
  ltr.setThresholds(100, 1000);
}

void loop() {

  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);
  delay(10);
  if (mod.write(query, sizeof(query)) == 8) {
    mod.flush();
    digitalWrite(DE, LOW);
    digitalWrite(RE, LOW);
    delay(10);
    for (byte i = 0; i < 19; i++) {
      values[i] = mod.read();
    }
  }
  delay(1000);
  float VIS = uv.readVisible();
  delay(10);
  float IR = uv.readIR();
  delay(10);
  float UV = uv.readUV() / 100.0;
  delay(10);
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);

  ltr.configInterrupt(true, LTR390_MODE_UVS);
  ltr.setMode(LTR390_MODE_UVS);
  float UVS = ltr.readUVS();

  delay(500);

  ltr.configInterrupt(true, LTR390_MODE_ALS);
  ltr.setMode(LTR390_MODE_ALS);
  float ALS = ltr.readALS();

  // Serial.print("Soil Moisture: ");
  Serial.print(((values[3] << 8) | values[4]) / 10.0);
  Serial.print(",");
  // Serial.print("Soil Temperature: ");
  Serial.print(((values[5] << 8) | values[6]) / 10.0);
  Serial.print(",");
  // Serial.print("Soil Conductivity: ");
  Serial.print((values[7] << 8) | values[8]);
  Serial.print(",");
  // Serial.print("Soil PH: ");
  Serial.print(((values[9] << 8) | values[10]) / 10.0 );
  Serial.print(",");
  // Serial.print("Soil N: ");
  Serial.print((values[11] << 8) | values[12]);
  Serial.print(",");
  // Serial.print("Soil P: ");
  Serial.print((values[13] << 8) | values[14]);
  Serial.print(",");
  // Serial.print("Soil K: ");
  Serial.print((values[15] << 8) | values[16]);
  Serial.print(",");
  
  // NEW DATA FOR LUKE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  // Serial.print("Room Visibile: ");
  Serial.print(VIS);
  Serial.print(",");
  // Serial.print("Room IR: ");
  Serial.print(IR);
  Serial.print(",");
  // Serial.print("Room UV: ");
  Serial.print(UV);
  Serial.print(",");
  // Serial.print("Room Temp: ");
  Serial.print(temp.temperature);
  Serial.print(",");
  // Serial.print("Room Humidity: ");
  Serial.print(humidity.relative_humidity);
  // Serial.print(",");
  // Serial.print("Room UVS: ");
  // Serial.print(UVS);
  // Serial.print(",");
  // Serial.print("Room ALS: ");
  // Serial.print(ALS);

  Serial.println();
  
  //error checks
  // Serial.print("Address: ");
  // Serial.print(values[0]);
  // Serial.println();
  // Serial.print("Function code: ");
  // Serial.print(values[1]);
  // Serial.println();
  // Serial.print("Number of data bytes: ");
  // Serial.print(values[2]);
  // Serial.println();
  // Serial.print("Error Check (Lo): ");
  // Serial.print(values[17]);
  // Serial.println();
  // Serial.print("Error Check (Hi): ");
  // Serial.print(values[18]);
  // Serial.println();

  delay(3000);
}