/* Low level communication - Hoa Tran */

/*
  For IMU
  The sensor outputs provided by the library are the raw
  16-bit values obtained by concatenating the 8-bit high and
  low accelerometer and gyro data registers. They can be
  converted to units of g and dps (degrees per second) using
  the conversion factors specified in the datasheet for your
  particular device and full scale setting (gain).

  Example: An LSM6DS33 gives an accelerometer Z axis reading
  of 16276 with its default full scale setting of +/- 2 g. The
  LA_So specification in the LSM6DS33 datasheet (page 15)
  states a conversion factor of 0.061 mg/LSB (least
  significant bit) at this FS setting, so the raw reading of
  16276 corresponds to 16276 * 0.061 = 992.8 mg = 0.9928 g.

  G_So specification in the LSM6DS33 datasheet (page 15)
  states a conversion factor of 4.375 mdps/LSB (least
  significant bit) at this FS setting, so the DELTA raw reading of
  800 corresponds to 800 * 4.375 = 3500 mdps = 3.5 dps.
  -------------------------------------------------------------------------------
  For Compass
  The sensor outputs provided by the library are the raw 16-bit values
  obtained by concatenating the 8-bit high and low magnetometer data registers.
  They can be converted to units of gauss using the
  conversion factors specified in the datasheet for your particular
  device and full scale setting (gain).

  Example: An LIS3MDL gives a magnetometer X axis reading of 1292 with its
  default full scale setting of +/- 4 gauss. The GN specification
  in the LIS3MDL datasheet (page 8) states a conversion factor of 6842
  LSB/gauss (where LSB means least significant bit) at this FS setting, so the raw
  reading of 1292 corresponds to 1292 / 6842 = 0.1888 gauss.
  -------------------------------------------------------------------------------
  The IMU codes are based on the LSM6 and LIS3MDL library of Pololu
*/

#include <Wire.h>
#include <LSM6.h>
#include <LIS3MDL.h>

#define L_encoderPinA 3 //Interrupt 1
#define L_encoderPinB 7
#define R_encoderPinA 2 //Interrupt 0
#define R_encoderPinB 4
#define counts_per_revolution 12
#define Wheel_R 35 // mm
#define Wheel_circumference 219.91 // C = 2piR
#define Gear_ratio 100.0 // mm
#define counts_per_mm 5.457 // counts_per_revolution*Gear_ratio/Wheel_circumference
#define PID_loop_time 250 //ms
#define Calibration_time 2000

// IMU
LSM6 imu; // Internal Measurement Unit
LIS3MDL mag; // Compass
bool imu_en = 1;
bool mag_en = 1;
int SS_update_rate = 5; //5ms
unsigned long SS_last_update = 0;
long ACC_X = 0;
long ACC_Y = 0;
long GYR_Z = 0;
int IMU_read_counts = 0;
long MAG_X = 0;
long MAG_Y = 0;
long MAG_Z = 0;
int MAG_read_counts = 0;

// Interrupts
volatile int L_encoderCnts = 0;
volatile int R_encoderCnts = 0;
long L_counted = 0;
long R_counted = 0;
long L_last_counted = 0;
long R_last_counted = 0;
int L_LastCnts = 0;
int R_LastCnts = 0;

unsigned long this_L_interrupt = 0;
unsigned long last_L_interrupt = 0;
unsigned long this_R_interrupt = 0;
unsigned long last_R_interrupt = 0;
int bouncing_time = 1;

// Motor
const int RmotorFW  = 9;  // Pin 15 of L293
const int RmotorBW  = 10;  // Pin 10 of L293
float R_M_speed = 50.0;

const int LmotorFW  = 5; // Pin  2 of L293
const int LmotorBW  = 6;  // Pin  7 of L293
float L_M_speed = 50.0;

int motor_mode = 0;
bool speed_is_set = 0;

// PID
unsigned long lastmillis = 0;
int required_distance = 0;

float L_last_error = 0;
int L_required_speed = 0;
long L_integral = 0;
long L_derivative = 0;

float R_last_error = 0;
int R_required_speed = 0;
long R_integral = 0;
long R_derivative = 0;

float Kp = 0.4;
float Ki = 0.04;
float Kd = 0.01;

// Serial Communication
String inputString = "";         // a string to hold incoming data
String outputString = "";         // a string to hold output data
boolean stringComplete = false;  // whether the string is complete
boolean readInProgress = false;
const char startMarker = '<';
const char endMarker = '>';
int in_checksum_value;
int in_sum_value;
int out_checksum_value;
int out_sum_value;
bool readChecksum = false;
bool CS_calc_done = false;

/*----------------------------------------------------------------------------------------------------------------------------*/
void setup() {
  Serial.begin (9600);
  //Set pins as inputs for encoders
  pinMode(L_encoderPinA, INPUT);
  pinMode(L_encoderPinB, INPUT);
  pinMode(R_encoderPinA, INPUT);
  pinMode(R_encoderPinB, INPUT);

  //Set pins as outputs for motors
  pinMode(LmotorFW, OUTPUT);
  pinMode(LmotorBW, OUTPUT);
  pinMode(RmotorFW, OUTPUT);
  pinMode(RmotorBW, OUTPUT);

  // Create interrupts
  attachInterrupt(1, L_Encoder_Int, RISING);
  attachInterrupt(0, R_Encoder_Int, RISING);

  // Initialize IMU and Compass
  Wire.begin();
  if (!imu.init())
  {
    SerialReply2Pi("<Failed to detect and initialize IMU!>");
    imu_en = 0;
  }
  else
  {
    imu.enableDefault();
    SerialReply2Pi("<IMU detected and initialized!>");
  }
  if (!mag.init())
  {
    SerialReply2Pi("<Failed to detect and initialize magnetometer!>");
    mag_en = 0;
  }
  else
  {
    mag.enableDefault();
    SerialReply2Pi("<Magnetometer detected and initialized!>");
  }
//  if (imu_en||mag_en)
//  {
//    
//    unsigned long start_calibrate = millis;
//    long read_count;
//    while (millis-start_calibrate)<Calibration_time
//    delay(2000);
//  }
  delay(1000);
  SerialReply2Pi("<Arduino is ready>");
}

/*----------------------------------------------------------------------------------------------------------------------------*/
void loop()
{
  if (stringComplete)
  {
    Communication_Handler();
  }
  else
  {
    Read_sensor_continuously();
  }
  switch (motor_mode) {
    case 0:
      Stop_all_motors();
      break;
    case 1:
      Constant_speed_mode();
      break;
    default:
      // statements
      break;
  }
}

/*----------------------------------------------------------------------------------------------------------------------------*/
void Communication_Handler() {
  // Split the command in two values
  String command = getValue(inputString, ':', 0);
  // Do something with data
  if (((int)in_checksum_value - (int)in_sum_value % 128) != 0)
  {
    SerialReply2Pi("<Er>");
  }
  else if (command != 0)
  {
    if (command == "MoSp")
    {
      String values = getValue(inputString, ':', 1);
      String L_speed = getValue(values, ',', 0);
      String R_speed = getValue(values, ',', 1);
      if ((L_speed.toInt() == 0) && (R_speed.toInt() == 0))
      {
        SerialReply2Pi("<Motor Stopped.>");
        L_required_speed = 0;
        R_required_speed = 0;
        motor_mode = 0;
      }
      else if ((abs(L_speed.toInt()) <= 140) && (abs(R_speed.toInt()) <= 140))
      {
        L_required_speed = L_speed.toInt();
        R_required_speed = R_speed.toInt();
        motor_mode = 1;
        SerialReply2Pi("<Speed set done.>");
      }
    }
    else if (command == "ECD")
    {
      char message[80];
      snprintf(message, sizeof(message), "<%ld %ld>", L_counted - L_last_counted, R_counted - R_last_counted);
      SerialReply2Pi(message);
      L_last_counted = L_counted;
      R_last_counted = R_counted;
    }
    else if (command == "IMU")
    {
      if (imu_en) {
        char imu_report[80];
        long ave_acc_x = ACC_X/IMU_read_counts;
        long ave_acc_y = ACC_Y/IMU_read_counts;
        long ave_gyr_z = GYR_Z/IMU_read_counts;
        // Reset value after read
        ACC_X = 0;
        ACC_Y = 0;
        GYR_Z = 0;
        IMU_read_counts = 0;
        snprintf(imu_report, sizeof(imu_report), "<%ld %ld %ld>",
                 ave_acc_x, ave_acc_y, ave_gyr_z);
        SerialReply2Pi(imu_report);
      }
      else {
        SerialReply2Pi("<Failed to detect and initialize IMU!>");
      }
    }
    else if (command == "MAG")
    {
      if (imu_en) {
        mag.read();
        char mag_report[80];
        long ave_mag_x = MAG_X/MAG_read_counts;
        long ave_mag_y = MAG_Y/MAG_read_counts;
        long ave_mag_z = MAG_Z/MAG_read_counts;
        // Reset value after read
        MAG_X = 0;
        MAG_Y = 0;
        MAG_Z = 0;
        MAG_read_counts = 0;
        snprintf(mag_report, sizeof(mag_report), "<%ld %ld %ld>",
                 ave_mag_x, ave_mag_y, ave_mag_z);
        SerialReply2Pi(mag_report);
      }
      else {
        SerialReply2Pi("<Arduino failed to detect and initialize magnetometer!>");
      }
    }
    else
    {
      SerialReply2Pi("<Arduino received unknown command!>");
    }
  }
  else
  {
    SerialReply2Pi("<Arduino received invalid command!>");
  }
  // clear the string:
  inputString = "";
  stringComplete = false;
}

/*----------------------------------------------------------------------------------------------------------------------------*/
void Stop_all_motors() {
  L_encoderCnts = 0;
  R_encoderCnts = 0;
  analogWrite(LmotorFW, 0);
  analogWrite(LmotorBW, 0);
  analogWrite(RmotorFW, 0);
  analogWrite(RmotorBW, 0);
}

/*----------------------------------------------------------------------------------------------------------------------------*/
void Constant_speed_mode() {
  float L_required_rpm = ((L_required_speed / 1000.0) / ((Wheel_R / 1000.0) * 0.10472)) * Gear_ratio; // v = r × RPM × 0.10472
  float R_required_rpm = (R_required_speed / 1000.0) / ((Wheel_R / 1000.0) * 0.10472) * Gear_ratio; // v = r × RPM × 0.10472
  float L_required_Fre = (abs(L_required_rpm) * counts_per_revolution * 1.0) / (60 * (1000.0 / PID_loop_time)); //L_required_Fre = counts/loop
  float R_required_Fre = (abs(R_required_rpm) * counts_per_revolution * 1.0) / (60 * (1000.0 / PID_loop_time)); //R_required_Fre = counts/loop
  if (millis() - lastmillis >= PID_loop_time)
  {
    // PID control for left wheel
    float error = L_required_Fre - abs(L_encoderCnts); //P control
    if (abs(error) > 0.5)
    {
      L_derivative = error - L_last_error;// D control
      if ((L_last_error < 0 && error >= 0)) // I control
      {
        L_integral = 0;
        L_derivative = abs(L_last_error) + error;
      }
      else if (L_last_error >= 0 && error < 0)
      {
        L_integral = 0;
        L_derivative = -(L_last_error + abs(error));
      }
      L_integral = L_integral + error;
      float New_speed = L_M_speed + error * Kp + L_integral * Ki + L_derivative * Kd;
      if (New_speed > 250)
      {
        L_M_speed = 250;
      }
      else if (New_speed < 0)
      {
        L_M_speed = 0;
      }
      else
      {
        L_M_speed = New_speed;
      }
      if (L_required_speed > 0)
      {
        analogWrite(LmotorFW, L_M_speed);
        analogWrite(LmotorBW, 0);
      }
      else if (L_required_speed < 0)
      {
        analogWrite(LmotorFW, 0);
        analogWrite(LmotorBW, L_M_speed);
      }
      else
      {
        analogWrite(LmotorFW, 0);
        analogWrite(LmotorBW, 0);
      }
      L_last_error = error;
    }
    // PID control for right wheel
    error = R_required_Fre - abs(R_encoderCnts); //P control
    if (abs(error) > 0.5)
    {
      R_derivative = error - R_last_error;// D control
      if ((R_last_error < 0 && error >= 0)) // I control
      {
        R_integral = 0;
        R_derivative = abs(R_last_error) + error;
      }
      else if (R_last_error >= 0 && error < 0)
      {
        R_integral = 0;
        R_derivative = -(R_last_error + abs(error));
      }
      R_integral = R_integral + error;
      float New_speed = R_M_speed + error * Kp + R_integral * Ki + R_derivative * Kd;
      if (New_speed > 250)
      {
        R_M_speed = 250;
      }
      else if (New_speed < 0)
      {
        R_M_speed = 0;
      }
      else
      {
        R_M_speed = New_speed;
      }
      if (R_required_speed > 0)
      {
        analogWrite(RmotorFW, R_M_speed);
        analogWrite(RmotorBW, 0);
      }
      else if (R_required_speed < 0)
      {
        analogWrite(RmotorFW, 0);
        analogWrite(RmotorBW, R_M_speed);
      }
      else
      {
        analogWrite(RmotorFW, 0);
        analogWrite(RmotorBW, 0);
      }
      R_last_error = error;
    }
    // Reset for next loop
    L_encoderCnts = 0; // Restart the encoder counter
    R_encoderCnts = 0; // Restart the encoder counter
    lastmillis = millis(); // Uptade lasmillis
  }
}
/*----------------------------------------------------------------------------------------------------------------------------*/
void Read_sensor_continuously()
{
  if ((millis() - SS_last_update)>SS_update_rate)
  {
    if (imu_en)
    {
      imu.read();
      ACC_X = ACC_X + imu.a.x;
      ACC_Y = ACC_Y + imu.a.y;
      GYR_Z = GYR_Z + imu.g.z;
//      Serial.print("IMU: ");
//      Serial.print(ACC_X);
//      Serial.print(", ");
//      Serial.print(ACC_Y);
//      Serial.print(", ");
//      Serial.println(GYR_Z);
//      
      IMU_read_counts++;
    }
    if (mag_en)
    {
      mag.read();
      MAG_X = MAG_X + mag.m.x;
      MAG_Y = MAG_Y + mag.m.y;
      MAG_Z = MAG_Z + mag.m.z;
      MAG_read_counts++;
    }
    SS_last_update = millis();
  }
 
}
/*----------------------------------------------------------------------------------------------------------------------------*/
void L_Encoder_Int() {
  this_L_interrupt = millis();
  if ((this_L_interrupt - last_L_interrupt) >= bouncing_time)
  {
    if (digitalRead(L_encoderPinB)) {
      L_encoderCnts++;
      L_counted++;
    }
    else {
      L_encoderCnts--;
      L_counted--;
    }
    last_L_interrupt = this_L_interrupt;
  }
}

/*----------------------------------------------------------------------------------------------------------------------------*/
void R_Encoder_Int() {
  this_R_interrupt = millis();
  if ((this_R_interrupt - last_R_interrupt) >= bouncing_time)
  {
    if (digitalRead(R_encoderPinB)) {
      R_encoderCnts++;
      R_counted++;
    }
    else {
      R_encoderCnts--;
      R_counted--;
    }
    last_R_interrupt = this_R_interrupt;
  }
}

/*----------------------------------------------------------------------------------------------------------------------------*/
void SerialReply2Pi(String mesg) {
  for (int i = 0; i < mesg.length(); i++)
  {
    char x = mesg[i];

    // Check if that byte is the end of command
    if (x == endMarker)
    {
      readInProgress = false;
      CS_calc_done = true;
    }
    // Check if currently reading data
    if (readInProgress) {
      out_sum_value += (int) x;
      // add it to the inputString:
      outputString += x;
    }
    // Check if that byte is start of command
    if (x == startMarker) {
      out_sum_value = 0;
      readInProgress = true;
      outputString = "";
      CS_calc_done = false;
    }

    if (CS_calc_done)
    {
      char checksum_c = out_sum_value % 128;
      mesg = mesg + checksum_c;
      Serial.println(mesg);
      CS_calc_done = false;
      break;
    }
  }
}
/*----------------------------------------------------------------------------------------------------------------------------*/
/*
  SerialEvent occurs whenever a new data comes in the
  hardware serial RX.  This routine is run between each
  time loop() runs, so using delay inside loop can delay
  response.  Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {

    // get the new byte:
    char x = (char)Serial.read();
    // Check if that byte is checksum value from sender
    if (readChecksum) {
      in_checksum_value = x; // Read one more time to collect checksum value
      stringComplete = true;
      readChecksum = false;
    }
    // Check if that byte is the end of command
    if (x == endMarker)
    {
      inputString += '\n';
      readInProgress = false;
      readChecksum = true;
    }
    // Check if currently reading data
    if (readInProgress) {
      in_sum_value += (int) x;
      // add it to the inputString:
      inputString += x;
    }
    // Check if that byte is start of command
    if (x == startMarker) {
      in_sum_value = 0;
      in_checksum_value = 0;
      readInProgress = true;
    }
  }
}

/*----------------------------------------------------------------------------------------------------------------------------*/
String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = { 0, -1 };
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }
  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

