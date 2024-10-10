#define M11_A 3
#define M11_B 4
#define M11_EN 5
#define M11_in1 6
#define M11_in2 7

#define M12_A 8
#define M12_B 9
#define M12_EN 10
#define M12_in1 11
#define M12_in2 12

// #define M21_A 14
// #define M21_B 15
// #define M21_EN 16
// #define M21_in1 17
// #define M21_in2 18

// #define M22_A 20
// #define M22_B 21
// #define M22_EN 22
// #define M22_in1 26
// #define M22_in2 27

#include "MotorController.h"
#include "Encoders.h"

// MotorController_c motorController21;
// MotorController_c motorController22;

int revs = 10;
float target_counts = revs*2096;

void setup() {
  Serial.begin(9600);
  motorController11 = MotorController_c();
  motorController11.SetupMotorController(M11_EN,M11_in1,M11_in2);
  pinMode(M11_A, INPUT);
  pinMode(M11_B, INPUT);
  attachInterrupt(digitalPinToInterrupt(M11_A), ENC_A_Interrupt_Motor11, RISING);

  motorController12 = MotorController_c();
  motorController12.SetupMotorController(M12_EN,M12_in1,M12_in2);
  pinMode(M12_A, INPUT);
  pinMode(M12_B, INPUT);
  attachInterrupt(digitalPinToInterrupt(M12_A), ENC_A_Interrupt_Motor12, RISING);

  // motorController21 = MotorController_c();
  // motorController21.SetupMotorController(M21_EN,M21_in1,M21_in2);
  // pinMode(M21_A, INPUT);
  // pinMode(M21_B, INPUT);
  // attachInterrupt(digitalPinToInterrupt(M21_A), ENC_A_Interrupt_Motor21, RISING);

  // motorController22 = MotorController_c();
  // motorController22.SetupMotorController(M22_EN,M22_in1,M22_in2);
  // pinMode(M22_A, INPUT);
  // pinMode(M22_B, INPUT);
  // attachInterrupt(digitalPinToInterrupt(M22_A), ENC_A_Interrupt_Motor22, RISING);
}

void loop() {
  motorController11.ControlLoop(encoder_count_volatile_motor11);
  motorController12.ControlLoop(encoder_count_volatile_motor12);
  // motorController21.ControlLoop(encoder_count_volatile_motor21);
  // motorController22.ControlLoop(encoder_count_volatile_motor22);
  motorController11.SetTargetCounts(2096*revs);
  motorController12.SetTargetCounts(-(2096*revs));
  // motorController21.SetTargetCounts(2096*revs);
  // motorController22.SetTargetCounts(2096*revs);
  Serial.print("target_counts:");
  Serial.print(target_counts);
  Serial.print(",");
  Serial.print("enc 11:");
  Serial.print(encoder_count_volatile_motor11);
  Serial.print(",");
  Serial.print("enc 12:");
  Serial.print(encoder_count_volatile_motor12);
  Serial.print(",");
  // Serial.print("enc 21:");
  // Serial.print(encoder_count_volatile_motor21);
  // Serial.print(",");
  // Serial.print("enc 22:");
  // Serial.print(encoder_count_volatile_motor22);
  // Serial.print(",");
  Serial.println();

}
