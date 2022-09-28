// Include the Wire library for I2C
#include <Stepper.h>
#include <Wire.h>

const int stepsPerRevolution = 200;  // change this to fit the number of steps per revolution
// for your motor
int c=0;
 // initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

// LED on pin 13
const int ledPin = 13; 

void setup() {
  // Join I2C bus as slave with address 8
  Wire.begin(0x8);
  
  // Call receiveEvent when data received                
  Wire.onReceive(receiveEvent);
  
  // Setup pin 13 as output and turn LED off
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  
  // set the speed at 60 rpm:
  myStepper.setSpeed(60);
  // serial port;
  Serial.begin(9600);
}
 
// Function that executes whenever data is received from master
void receiveEvent(int howMany) {
  while (Wire.available()) { // loop through all but the last
    c= Wire.read(); // receive byte as a character
    digitalWrite(ledPin, c);
    Serial.println(c);
    Serial.println("event");
    }
  
}
void loop() {
  delay(100);
  if(c!=0)
    {
      Serial.println("각도 : 90");
      for(int i=0;i<4;i++)
        myStepper.step(c);//one step per 1.8degree
      delay(500);
      myStepper.step(-800);//one step per 1.8degree
      Serial.println("end");
      c=0;
    }
   delay(500);
    
}
