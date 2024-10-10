class MotorController_c {
public:
  MotorController_c() {}

  // Pins
  int PWM_PIN = 0;
  int IN_1_PIN = 0;
  int IN_2_PIN = 0;

  // PWM specs
  int u = 0;
  int u_amplitude = 0;
  int u_sign = 0;
  float target_counts = 0;

  // Telemetry
  long current_T = 0;
  long previous_T = 0;
  int print_interval = 100;
  int interval_count = 0;
  float average_delta_T = 0;
  int interval_start = 0;
  float delta_T = 0;

  // Error
  int e = 0;
  int previous_e = 0;
  float cumulative_e = 0;
  float rate_e = 0;

  // Gains
  float K_p = 0;
  float K_i = 0;
  float K_d = 0;

  // Low-pass filter
  int sample_rate = 200;
  int break_frequency = 50;
  float alpha = 1 - (break_frequency)/sample_rate ;
  int u_f;
  int previous_u_f = 0;

  // Lead control
  float u_lead;
  float K_lead = 40;
  float T_lead = 0.1;
  float a_lead = 0.8;

  void SetupMotorController(int pwm_pin, int in_1, int in_2) {
    PWM_PIN = pwm_pin;
    IN_1_PIN = in_1;
    IN_2_PIN = in_2;

    pinMode(PWM_PIN, OUTPUT);
    pinMode(IN_1_PIN, OUTPUT);
    pinMode(IN_2_PIN, OUTPUT);
  }

  void SetMotorPower(int dir, int pwmval) {
    analogWrite(PWM_PIN, pwmval);

    switch (dir) {
      case 0:  // stopped
        digitalWrite(IN_1_PIN, LOW);
        digitalWrite(IN_2_PIN, LOW);
      case 1:  // CW
        digitalWrite(IN_1_PIN, HIGH);
        digitalWrite(IN_2_PIN, LOW);
        break;
      case -1:  // CCW
        digitalWrite(IN_1_PIN, LOW);
        digitalWrite(IN_2_PIN, HIGH);
        break;
      default:  // stopped
        digitalWrite(IN_1_PIN, LOW);
        digitalWrite(IN_2_PIN, LOW);
    }
  }

  void ControlLoop(int encoder_count) {

    // BANG-BANG CONTROL
    
    // if (e < 0) {
    //   u = -100;
    // } else {
    //   u = 100;
    // }
    

    // PID CONTROL

    // calculate d_time
    current_T = millis();                      // returns simulation time in ms
    delta_T = (current_T - previous_T) / 1E3;  // elapsed time since last loop iteration in s

    // calculate errors
    e = target_counts - encoder_count;    // update error (used for P control)
    cumulative_e += (delta_T * e);        // update cumulative error (used for I control)
    rate_e = (e - previous_e) / delta_T;  // update rate error (used for D control)

    // calculate input u
    if (K_p * abs(e) > 255) {
      cumulative_e = 0;
    }
    u = (K_p * e) + (K_i * cumulative_e) + (K_d * rate_e);
    // u_lead = K_lead*((1+(T_lead*rate_e))/(1+(a_lead * T_lead * rate_e)));
    // u_f = u * u_lead;
    u_f = u;
    // implement low-pass filter
    // u_f = alpha*previous_u_f + (1-alpha)*u;
    

    // U MAGNITUDE MUST BE BETWEEN 0 AND 255
    if (u_f > 255) {
      u_f = 255;
    } else if (u_f < -255) {
      u_f = -255;
    }

    // split u into power and directions and set motor power
    u_amplitude = abs(u_f);
    u_sign = u_f / u_amplitude;
    SetMotorPower(u_sign, u_amplitude);


    // set previous values
    previous_e = e;
    previous_T = current_T;
    previous_u_f = u_f;
  }

  void SetTargetCounts(int counts) {
    target_counts = counts;
  }

  void SetGains(float p, float i, float d) {
    K_p = p;
    K_i = i;
    K_d = d;
  }
};