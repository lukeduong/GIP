class MotorController_c {
  public: 

    MotorController_c() {
      
    }

  int EN = 0;
  int in1 = 0;
  int in2 = 0;

  int u = 0;
  int u_amplitude = 0;
  int u_sign = 0;

  float target_counts = 0;

  int e = 0;

  long current_T = 0;
  long previous_T = 0;
  int print_interval = 100;
  int interval_count = 0;
  float average_delta_T = 0;
  int interval_start = 0;
  float delta_T = 0;

  void SetupMotorController(int EN_val, int in1_val, int in2_val) {
    EN = EN_val;
    in1 = in1_val;
    in2 = in2_val;

    pinMode(EN, OUTPUT);
    pinMode(in1, OUTPUT);
    pinMode(in2, OUTPUT);
  }

  void SetMotorPower(int dir,int pwmVal){
    analogWrite(EN,pwmVal);
    if (dir == 1) {
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
    } else if (dir == -1) {
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
    } else {
      digitalWrite(in1, LOW);
      digitalWrite(in2, LOW);
    }
  }

  void ControlLoop(int encoder_count) {
    e = target_counts - encoder_count;

    if (e > 0) {
      u =200;
    } else if (e < 0) {
      u = -200;
    } else {
      u = 0;
    }

    u_amplitude = abs(u);
    if (u > 0) {
      u_sign = 1;
    } else if (u < 0) {
      u_sign = -1;
    } else {
      u_sign = 0;
    }

    SetMotorPower(u_sign,u_amplitude);

    // current_T = micros();
    // delta_T = (current_T - previous_T) / 1e6;
    // previous_T = current_T;
    // interval_count = interval_count + 1;
    // if (interval_count >= print_interval) {
    //   interval_count = 0;
    //   average_delta_T = (micros()-interval_start)/(1e6*print_interval);
    //   interval_start = micros();
    //   Serial.print("target_counts:");
    //   Serial.print(target_counts);
    //   Serial.print(",");
    //   Serial.print("enc:");
    //   Serial.print(encoder_count);
    //   Serial.print(",");
    //   Serial.println();
    // }
  }

  void SetTargetCounts(int counts) {
    target_counts = counts;
  }

};