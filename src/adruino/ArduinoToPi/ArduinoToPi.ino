String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

int motor = 9;           // the PWM pin the LED is attached to
bool motor_on = 0;
// read RPM
volatile long half_revolutions = 0;
long encoder_ticks = 0;
long rpm = 0;
unsigned long lastmillis = 0;
volatile unsigned long last_int_micros = 0;
long design_rpm = 0;
float error = 0;
float last_error = 0;
float M_speed = 50;
float New_speed = 0;
float Kp = 0.4;
float Ki = 0.04;
float Kd = 0.01;
long integral = 0;
long derivative = 0;
void setup(){
   Serial.begin(9600); 
//   Serial.println("Motor test!");
   // declare pin 9 to be an output:
   pinMode(motor, OUTPUT);
   analogWrite(motor, 255-M_speed);
   // reserve 200 bytes for the inputString:
   inputString.reserve(200);
   
   delay(2000);
   analogWrite(motor, 255);
   attachInterrupt(0, rpm_encoder, RISING); // Interupt 0 on Pin D2
 }
void loop(){
 // print the string when a newline arrives:
   if (stringComplete) {
   // Split the command in two values
   String command = getValue(inputString, ':', 0);
   String value = getValue(inputString, ':', 1);
   // Do something with data
   if (command != 0)
   {
//      Serial.print("Arduino received command: ");
//      Serial.print(command);
//      Serial.print(", with value: ");
     long value_Int = value.toInt();
//     Serial.println(value_Int);
     if (command == "rpm")
     {
       if (value_Int == 0)
       {
         Serial.print("Motor Stopped.");
         design_rpm = 0;
         motor_on = 0;
       }
       else if (value_Int <= 15000)
       {
         design_rpm = value_Int;
         motor_on = 1;
         Serial.print("Motor is turning at: ");
         Serial.print(value_Int);
         Serial.println(" RPM");
         // Change RPM
       }
       else
       {
         Serial.println("Arduino received set RPM command but that RPM value is higher than limit! Please consider using lower RPM");
       }
     }
     else if (command == "encoder")
     {
       Serial.print("Current counted encoder: ");
       Serial.println(encoder_ticks);
     }
     else
     {
       Serial.println("Arduino received unknown command!");
     }
   }
   else
   {
     Serial.println("Arduino received invalid command! Please make sure your command in this format: command:value");
   }
   // clear the string:
   inputString = "";
   stringComplete = false;
   }

  if (motor_on == 1)
  {
     float design_Fre = design_rpm/120.0;
     if (millis() - lastmillis >= 250){ //Uptade every one second, this will be equal to reading frecuency (Hz).
     rpm = half_revolutions * 120; // Convert frecuency to RPM, note: this works for one interruption per full rotation. For two interrups per full rotation use half_revolutions * 30.
    // Serial.print("RPM =\t"); //print the word "RPM" and tab.
    // Serial.print(rpm); // print the rpm value.
    // Serial.print("\tHz=\t"); //print the word "Hz".
    // Serial.println(4*half_revolutions); //print revolutions per second or Hz. And print new line or enter.
    
     if (half_revolutions > 0)
     {
       error = design_Fre - half_revolutions; //P control
    //   Serial.print("\t error=\t");
    //   Serial.println(error);  
         
         if (abs(error) > 0.5)
         {
         derivative = error - last_error;// D control
         if ((last_error<0 && error >= 0))  // I control
         {
            integral = 0; 
            derivative = abs(last_error) + error;
         }
         else if (last_error>=0 && error < 0)
         {
            integral = 0; 
            derivative = -(last_error + abs(error));
         }
         integral = integral + error;
         New_speed = M_speed + error*Kp + integral*Ki + derivative*Kd;
    //     Serial.print("\t New speed=\t");
    //     Serial.println(255-New_speed);
         if (New_speed > 250)
         {
            M_speed = 250;
         }
         else if (New_speed < 0)
         {
            M_speed = 0;
         }
         else
         {
            M_speed = New_speed;
         }
    //     Serial.print("\t Motor speed=\t");
    //     Serial.println(255-M_speed);
         analogWrite(motor, 255-M_speed);
         last_error = error;
         }
       }
      half_revolutions = 0; // Restart the RPM counter
      lastmillis = millis(); // Uptade lasmillis
      }
  }
  else
  {
    analogWrite(motor, 255); // Dont run the motor
  }
}
 
// this code will be executed every time the interrupt 0 (pin2) gets low.
void rpm_encoder()
{
  if (micros() - last_int_micros > 2000)  
  {
    half_revolutions++;
    encoder_ticks++;
    last_int_micros = micros();
  }
}
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

String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
