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

// IMU
LSM6 imu; // Internal Measurement Unit
LIS3MDL mag; // Compass
char imu_report[80];
char mag_report[80];
bool imu_en = 1;
bool mag_en = 1;

// Interrupts
volatile int L_encoderCnts = 0;
volatile int R_encoderCnts = 0;
volatile long L_counted = 0;
volatile long R_counted = 0;
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
boolean stringComplete = false;  // whether the string is complete

/*----------------------------------------------------------------------------------------------------------------------------*/
void setup() {
  Serial.begin (9600);
  Serial.println("\t\tLow level communication");
  Serial.println(" --------------------------------------------------------------");
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
    Serial.println(F("Failed to detect and initialize IMU!"));
    imu_en = 0;
  }
  else
  {
    imu.enableDefault();
    Serial.println(F("IMU detected and initialized!"));
  }
  if (!mag.init())
  {
    Serial.println(F("Failed to detect and initialize magnetometer!"));
    mag_en = 0;
  }
  else
  {
    mag.enableDefault();
    Serial.println(F("Magnetometer detected and initialized!"));
  }
  // Ready
  Serial.println(F(" ---------------------------------------------------------------"));
  Serial.println(F("| Sent 'MoSp:L_speed,R_speed'   Move in constant speed (mm/s).  |"));
  Serial.println(F("| Sent 'MoDt:Distance'          Move for specific distance (mm).|"));
  Serial.println(F("| Sent 'St:'                    For emergence stop.             |"));
  Serial.println(F("| Sent 'ECD:'                   Read counted encoders.          |"));
  Serial.println(F("| Sent 'IMU:'                   Read IMU data.                  |"));
  Serial.println(F("| Sent 'MAG:'                   Read compass data.              |"));
  Serial.println(F(" ---------------------------------------------------------------"));
  Serial.println(F("|                Low level communication start!!                |"));
  Serial.println(F(" ---------------------------------------------------------------"));
  delay(2000);
}

/*----------------------------------------------------------------------------------------------------------------------------*/
void loop()
{
  if (stringComplete)
  {
    Communication_Handler();
  }
  switch (motor_mode) {
    case 0:
      Stop_all_motors();
      break;
    case 1:
      Constant_speed_mode();
      break;
    case 2:
      Move_distance_mode();
      break;
    default:
      // statements
      break;
  }
}

/*----------------------------------------------------------------------------------------------------------------------------*/
void Communication_Handler() {
  // Split the command in two values
  //  Serial.print(F("Arduino received data: "));
  //  Serial.println(inputString);
  String command = getValue(inputString, ':', 0);
  // Do something with data
  if (command != 0)
  {
    //      Serial.print(F("Arduino received command: "));
    //      Serial.println(command);
    if (command == "St") // Emergency Stop
    {
      Serial.println(F("Emergency Stop!!!"));
      L_required_speed = 0;
      R_required_speed = 0;
      motor_mode = 0;
    }
    else if (command == "MoSp")
    {
      String values = getValue(inputString, ':', 1);
      String L_speed = getValue(values, ',', 0);
      String R_speed = getValue(values, ',', 1);
      //      Serial.print("Speed values: ");
      //      Serial.print(values);
      //      Serial.print("Left Speed: ");
      //      Serial.print(L_speed);
      //      Serial.print("; Right Speed: ");
      //      Serial.print(R_speed);
      if ((L_speed.toInt() == 0) && (R_speed.toInt() == 0))
      {
        Serial.println(F("Motor Stopped."));
        L_required_speed = 0;
        R_required_speed = 0;
        motor_mode = 0;
      }
      else if ((abs(L_speed.toInt()) <= 140) && (abs(R_speed.toInt()) <= 140))
      {
        L_required_speed = L_speed.toInt();
        R_required_speed = R_speed.toInt();
        motor_mode = 1;
        //          Serial.print("Motor is turning at: Left Speed: ");
        //          Serial.print(L_required_speed);
        //          Serial.print(" mm/s, Right Speed: ");
        //          Serial.print(R_required_speed);
        //          Serial.println(" mm/s.");
      }
      else
      {
        Serial.println(F("Max speed is 140 mm/s! Please consider lower the speed."));
      }
    }
    else if (command == "MoDt")
    {
      String distance = getValue(inputString, ':', 1);
      //        Serial.print("Distance values: ");
      //        Serial.print(values);
      int distance_int = distance.toInt();
      if (distance_int == 0)
      {
        Serial.println(F("Motor Stopped."));
        L_required_speed = 0;
        R_required_speed = 0;
        motor_mode = 0;
      }
      else
      {
        required_distance = distance_int;
        L_LastCnts = L_encoderCnts;
        R_LastCnts = R_encoderCnts;
        motor_mode = 2;
        speed_is_set = 0;
        Serial.print(F("Robot moves for: "));
        Serial.print(distance_int);
        Serial.println(F(" mm."));
      }
    }
    else if (command == "ECD")
    {
      Serial.print(F("Current encoders counted: "));
      Serial.print(L_counted);
      Serial.print(F(", "));
      Serial.println(R_counted);
    }
    else if (command == "IMU")
    {
      if (imu_en) {
        imu.read();
        snprintf(imu_report, sizeof(imu_report),"A: %6d %6d %6d  G: %6d %6d %6d",
                 imu.a.x, imu.a.y, imu.a.z,
                 imu.g.x, imu.g.y, imu.g.z);
        Serial.println(imu_report);
      }
      else {
        Serial.println(F("Failed to detect and initialize IMU!"));
      }
    }
    else if (command == "MAG")
    {
      if (imu_en) {
        mag.read();
        snprintf(mag_report, sizeof(mag_report), "M: %6d %6d %6d",
                 mag.m.x, mag.m.y, mag.m.z);
        Serial.println(mag_report);
      }
      else {
        Serial.println(F("Failed to detect and initialize magnetometer!"));
      }
    }
    else
    {
      Serial.println(F("Arduino received unknown command!"));
    }
  }
  else
  {
    Serial.println(F("Arduino received invalid command! Please make sure your command in this format: command:value"));
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
  //    Serial.print(F("L_required_rpm: "));
  //    Serial.print(L_required_rpm);
  //    Serial.print(F("\tR_required_rpm: "));
  //    Serial.println(R_required_rpm);
  //    Serial.print(F("L_required_Fre: "));
  //    Serial.print(L_required_Fre);
  //    Serial.print(F("\tR_required_Fre: "));
  //    Serial.println(R_required_Fre);
  if (millis() - lastmillis >= PID_loop_time)
  {
    // PID control for left wheel
    float error = L_required_Fre - abs(L_encoderCnts); //P control
    //    Serial.print(F("L_error: "));
    //    Serial.println(error);
    //        Serial.print(F("\tL_encoder: "));
    //        Serial.print(L_encoderCnts);
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
      //          Serial.print(F("\tL_M_speed: "));
      //          Serial.println(L_M_speed);
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
    //    Serial.print(F("R_error: "));
    //    Serial.println(error);
    //        Serial.print(F("\tR_encoder: "));
    //        Serial.print(R_encoderCnts);
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
      //          Serial.print(F("\tR_M_speed: "));
      //          Serial.println(R_M_speed);
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
void Move_distance_mode() {
  float required_Fre = abs(required_distance) * counts_per_mm;
  int current_counts = abs(((L_encoderCnts - L_LastCnts) + (R_encoderCnts - R_LastCnts)) / 2);
  //  Serial.print(F("Robot move for: "));
  //  Serial.print(required_Fre);
  //  Serial.print(F(" counts, current counts: "));
  //  Serial.println(current_counts);
  if (current_counts < required_Fre)
  {
    if (!speed_is_set)
    {
      if (required_distance > 0)
      {
        analogWrite(LmotorFW, 120);
        analogWrite(LmotorBW, 0);
        analogWrite(RmotorFW, 120);
        analogWrite(RmotorBW, 0);
        speed_is_set = 1;
      }
      else
      {
        analogWrite(LmotorFW, 0);
        analogWrite(LmotorBW, 120);
        analogWrite(RmotorFW, 0);
        analogWrite(RmotorBW, 120);
        speed_is_set = 1;
      }
    }
  }
  else
  {
    speed_is_set = 0;
    motor_mode = 0;
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
/*
  SerialEvent occurs whenever a new data comes in the
  hardware serial RX.  This routine is run between each
  time loop() runs, so using delay inside loop can delay
  response.  Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
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

