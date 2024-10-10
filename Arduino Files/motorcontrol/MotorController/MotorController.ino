// Motor 1
#define ENC_A_PIN_M1 1
#define ENC_B_PIN_M1 2
#define PWM_PIN_M1 3
#define IN_1_PIN_M1 4
#define IN_2_PIN_M1 5
// Motor 2
#define ENC_A_PIN_M2 1
#define ENC_B_PIN_M2 2
#define PWM_PIN_M2 3
#define IN_1_PIN_M2 4
#define IN_2_PIN_M2 5

#include "MotorController.h"
#include "counts.h"
#include "gains.h"

MotorController_c motorController1;
MotorController_c motorController2;

bool looper = true;
int counter = 0;
int loopstart;

void setup() {
  Serial.begin(230400);

  // Setup Motor 1
  motorController1 = MotorController_c();
  motorController1.SetupMotorController(PWM_PIN_M1, IN_1_PIN_M1, IN_2_PIN_M1);

  pinMode(ENC_A_PIN_M1, INPUT);
  pinMode(ENC_B_PIN_M1, INPUT);

  attachInterrupt(digitalPinToInterrupt(ENC_A_PIN_M1), ENC_A_Interrupt_Motor1, RISING);

  motorController1.SetGains(K_p, K_i, K_d);

  // Setup Motor 2
  motorController2 = MotorController_c();
  motorController2.SetupMotorController(PWM_PIN_M2, IN_1_PIN_M2, IN_2_PIN_M2);

  pinMode(ENC_A_PIN_M2, INPUT);
  pinMode(ENC_B_PIN_M2, INPUT);

  attachInterrupt(digitalPinToInterrupt(ENC_A_PIN_M2), ENC_A_Interrupt_Motor2, RISING);

  motorController2.SetGains(K_p, K_i, K_d);

  delay(3000);

  loopstart = micros();
}

void loop() {
  if (micros() - loopstart > 1e6 / sample_rate) {
    counter++;
    loopstart = micros();
  }

  if (looper == true) {
    //Serial.println(encoder_count_volatile_motor1);

    // assign target counts
    int target_theta = counts[counter][0];
    int target_phi = counts[counter][1];

    // pause 10 seconds to lower pen
    if (counter == sample_rate * time_to_start) {
      motorController1.SetMotorPower(0, 0);
      motorController2.SetMotorPower(0, 0);
      // Serial.println("LOWER PEN");
      for (int i = 10; i >= 0; i--) {
        Serial.println(i);
        delay(1000);
      }
      loopstart = micros();
      encoder_count_volatile_motor1 = target_theta;
      encoder_count_volatile_motor2 = target_phi;
    }

    if (counter == 1200 - sample_rate * time_to_start) {
      motorController1.SetMotorPower(0, 0);
      motorController2.SetMotorPower(0, 0);
      // Serial.println("RAISE PEN");
      for (int i=10;i>=0;i--){
        // Serial.println(i);
        delay(1000);
      }
      loopstart = micros();
    }
    if (counter == 1199) {
      motorController1.SetMotorPower(0, 0);
      motorController2.SetMotorPower(0, 0);
      delay(3000);
      loopstart = micros();
      encoder_count_volatile_motor1 = target_theta;
      // encoder_count_volatile_motor2 = target_phi;
    }
    if (counter == 1199 + sample_rate * time_to_start) {
      motorController1.SetMotorPower(0, 0);
      // motorController2.SetMotorPower(0, 0);
      // Serial.println("LOWER PEN");
      for (int i=10;i>=0;i--){
        // Serial.println(i);
        delay(1000);
      }
      loopstart = micros();
      encoder_count_volatile_motor1 = target_theta;
      // encoder_count_volatile_motor2 = target_phi;
    }
    if (counter == 2399 - sample_rate * time_to_start) {
      motorController1.SetMotorPower(0, 0);
      // motorController2.SetMotorPower(0, 0);
      // Serial.println("RAISE PEN");
      for (int i=10;i>=0;i--){
        // Serial.println(i);
        delay(1000);
      }
      loopstart = micros();
    }
    if (counter == 2398) {
      motorController1.SetMotorPower(0, 0);
      // motorController2.SetMotorPower(0, 0);
      delay(3000);
      loopstart = micros();
      encoder_count_volatile_motor1 = target_theta;
      encoder_count_volatile_motor2 = target_phi;
    }
    if (counter == 2398 + sample_rate * time_to_start) {
      motorController1.SetMotorPower(0, 0);
      // motorController2.SetMotorPower(0, 0);
      // Serial.println("LOWER PEN");
      for (int i=10;i>=0;i--){
        // Serial.println(i);
        delay(1000);
      }
      loopstart = micros();
      encoder_count_volatile_motor1 = target_theta;
      // encoder_count_volatile_motor2 = target_phi;
    }


    // pause 10 seconds to raise pen
    if (counter == counts_size - sample_rate * time_to_start) {
      motorController1.SetMotorPower(0, 0);
      // motorController2.SetMotorPower(0, 0);
      // Serial.println("RAISE PEN");
      for (int i = 10; i >= 0; i--) {
        Serial.println(i);
        delay(1000);
      }
      loopstart = micros();
    }
    // break condition
    if (counter == counts_size) {
      motorController1.SetMotorPower(0, 0);
      // motorController2.SetMotorPower(0, 0);
      looper = false;  // exit loop function
      delay(2000);
      return;
    }

    // Motor 1
    motorController1.ControlLoop(encoder_count_volatile_motor1);
    motorController1.SetTargetCounts(target_theta);

    // Motor 2
    motorController2.ControlLoop(encoder_count_volatile_motor2);
    motorController2.SetTargetCounts(target_phi);

    // Print and plot data
    // Serial.print("Timestep:");
    // Serial.print(counter);
    // Serial.print("\tr_theta:");
    // Serial.print(target_theta);
    // Serial.print("\tz_theta:");
    // Serial.print(encoder_count_volatile_motor1);
    // Serial.print("\tr_phi:");
    // Serial.print(target_phi);
    // Serial.print("\tz_phi:");
    // Serial.println(encoder_count_volatile_motor2);
    // Serial.println("Timestep, r_theta, z_theta, r_phi, z_phi");

    //csv output
    Serial.print(counter);                          // Timestep
    Serial.print(",");                              // Comma to separate the next value
    Serial.print(target_theta);                     // r_theta
    Serial.print(",");                              // Comma to separate the next value
    Serial.print(encoder_count_volatile_motor1);    // z_theta
    Serial.print(",");                              // Comma to separate the next value
    Serial.print(target_phi);                       // r_phi
    Serial.print(",");                              // Comma to separate the next value
    Serial.println(encoder_count_volatile_motor2);  // z_phi - println for new line

    delay(1000 / sample_rate);
  } else {
    motorController1.SetMotorPower(0, 0);
    motorController2.SetMotorPower(0, 0);
  }
}
