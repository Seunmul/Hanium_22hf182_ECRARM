
/*
 Stepper Motor Control - one revolution

 This program drives a unipolar or bipolar stepper motor.
 The motor is attached to digital pins 8 - 11 of the Arduino.

 The motor should revolve one revolution in one direction, then
 one revolution in the other direction.


 Created 11 Mar. 2007
 Modified 30 Nov. 2009
 by Tom Igoe

 */

#include <Stepper.h>

const int stepsPerRevolution = 200;  // change this to fit the number of steps per revolution
// for your motor

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

int stepCount = 0;         // number of steps the motor has taken

void setup() {
  // set the speed at 60 rpm:
  myStepper.setSpeed(60);
  // initialize the serial port:
  Serial.begin(9600);
}

void loop() {
  // step one revolution  in one direction:
//  Serial.println("clockwise");
//  myStepper.step(stepsPerRevolution);
//  delay(2000);

  // step one revolution in the other direction:
//  Serial.println("counterclockwise");
//  myStepper.step(-stepsPerRevolution);
//  delay(2000);

  // step one step:
//  while(stepCount<30)
//  {
//    myStepper.step(1);//one step per 1.8degree
//    Serial.print("steps:");
//    Serial.println(stepCount);
//    stepCount++;
//    delay(500);  
//  }
  stepCount=0;
  for(int i=0;i<4;i++)
  {
    Serial.print("90도 : ");
    Serial.println(i);
    myStepper.step(900);//one step per 1.8degree
    delay(2000);  
  }
  for(int i=0;i<4;i++)
  {
    Serial.print("180도 : ");
    Serial.println(i);
    myStepper.step(1800);//one step per 1.8degree
    delay(1000);  
  }
  
}
