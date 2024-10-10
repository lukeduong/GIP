volatile int encoder_count_volatile_motor11 = 0;
void ENC_A_Interrupt_Motor11() {
  int b_state = digitalRead(M11_B);
  if (b_state == 1) {
    encoder_count_volatile_motor11++;
  } else {
    encoder_count_volatile_motor11--;
  }
}
volatile int encoder_count_volatile_motor12 = 0;
void ENC_A_Interrupt_Motor12() {
  int b_state = digitalRead(M12_B);
  if (b_state == 1) {
    encoder_count_volatile_motor12++;
  } else {
    encoder_count_volatile_motor12--;
  }
}
// volatile int encoder_count_volatile_motor21= 0;
// void ENC_A_Interrupt_Motor21() {
//   int b_state = digitalRead(M21_B);
//   if (b_state == 1) {
//     encoder_count_volatile_motor21++;
//   } else {
//     encoder_count_volatile_motor21--;
//   }
// }
// volatile int encoder_count_volatile_motor22 = 0;
// void ENC_A_Interrupt_Motor22() {
//   int b_state = digitalRead(M22_B);
//   if (b_state == 1) {
//     encoder_count_volatile_motor22++;
//   } else {
//     encoder_count_volatile_motor22--;
//   }
// }
