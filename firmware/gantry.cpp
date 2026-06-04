#include "gantry.h"
#define motorInterfaceType 1  
AccelStepper stepperX(motorInterfaceType, 2, 5);
AccelStepper stepperY(motorInterfaceType, 3, 6); 
AccelStepper stepperZ(motorInterfaceType, 4, 7);
Servo gripper;
Servo rotator;
long preY = 0;
long preZ =0;

#define MIN_BUF_LENGTH_WRITE  20
/*
void sendInfo(char* info)
{
   if (Serial.availableForWrite() >= MIN_BUF_LENGTH_WRITE)
       Serial.println(info);
   else
   {


   }


}
*/
void initGantry()
{
  Serial.begin(115200);
  //Serial.print(Serial.availableForWrite());
  //Serial.println("done");
  stepperX.setMaxSpeed(300); 
  stepperX.setAcceleration(600);
  stepperX.setSpeed(0);
  stepperY.setMaxSpeed(2000);
  stepperY.setAcceleration(800);
  stepperY.setSpeed(0);
  stepperZ.setMaxSpeed(2000);
  stepperZ.setAcceleration(800);
  stepperZ.setSpeed(0);
  gripper.attach(GRIPPER);
  rotator.attach(ROTATOR);
  gripper.write(0);
  rotator.write(0);
}
#define MulY 1.59235669 *2
#define MulX 3.18471338 *2
#define MulZ 3.18471338 *2
bool onebyone = true;
void moveXYZ(float x, float y , float z)
{

  float xsteps = x * MulX;
  float ysteps = y * MulY;
  float zsteps = z * MulZ;
  //Serial.println("Previous Y :");
 // Serial.println(preY);
  bool xdone = false;
  bool ydone = false;
  bool zdone = false;
 // Serial.println(xsteps);
  //Serial.println(ysteps);
  //Serial.println(zsteps);
  stepperY.setCurrentPosition(preY);
  stepperZ.setCurrentPosition(preY);
  stepperX.moveTo(xsteps);
  stepperY.moveTo(-ysteps*2);
  stepperZ.moveTo(-ysteps*2);
  if(!onebyone){
  while(!xdone||!ydone||!zdone)
  {
    //Serial.print("Im here");
    if (stepperX.distanceToGo() != 0) {
          stepperX.run();
        } else {
          xdone = true;
        }
    if (stepperY.distanceToGo() != 0) {
            //Serial.println("Im running");
            stepperY.run();
          } else {
            ydone = true;
          }
    if (stepperZ.distanceToGo() != 0) {
          stepperZ.run();
            //Serial.println("Im running");
           
          } else {
            zdone = true;
          }
    
  }
  }
  else
  {
   while(!xdone) 
   {
    if (stepperX.distanceToGo() != 0) {
          stepperX.run();
        } else {
          xdone = true;
        }
   }
   while(!ydone||!zdone)
   {
    if (stepperY.distanceToGo() != 0) {
            //Serial.println("Im running");
            stepperY.run();
          } else {
            ydone = true;
          }
    if (stepperZ.distanceToGo() != 0) {
          stepperZ.run();
            //Serial.println("Im running");
           
          } else {
            zdone = true;
          }
   }
  }
  preY = -ysteps*2;
  stepperY.setCurrentPosition(-preZ);
  stepperZ.setCurrentPosition(preZ);
  ydone = false;
  zdone = false;
  //Serial.println("Previous Z :");
  //Serial.println(preZ);
  //delay(1000);
  stepperY.moveTo(zsteps);
  stepperZ.moveTo(-zsteps);

  while(!zdone||!ydone)
  {
    if (stepperY.distanceToGo() != 0) {
            //Serial.println("Im running");
            stepperY.run();
          } else {
            ydone = true;
          }
    if (stepperZ.distanceToGo() != 0) {
            //Serial.println("Im running");
            stepperZ.run();
          } else {
            zdone = true;
          }
  }
  preZ = -zsteps;
  Serial.println("d");
}
void homeX()
{
   delay(5);

  stepperX.setMaxSpeed(4000.0);
  stepperX.setAcceleration(1000.0);

  long initial_homing = INIT_X_HOMING;

  while (digitalRead(xlimit)) {
    stepperX.moveTo(initial_homing);
    initial_homing--;
    stepperX.run();
    delay(2);
  }

  stepperX.setCurrentPosition(0);
  stepperX.setMaxSpeed(6000.0);
  stepperX.setAcceleration(3000.0);
  initial_homing = -INIT_X_HOMING;

  while (!digitalRead(xlimit)) {
    stepperX.moveTo(initial_homing);
    stepperX.run();
    initial_homing++;
    delay(2);
  }

  stepperX.setCurrentPosition(0);
  //Serial.println("X homing done");
}
void homeY()
{
  stepperY.setMaxSpeed(900);
  stepperY.setAcceleration(200);
  stepperZ.setMaxSpeed(900);
  stepperZ.setAcceleration(200);
  long initial_homing = INIT_Y_HOMING;
  while (digitalRead(ylimit)) {
    stepperY.moveTo(initial_homing);
    stepperZ.moveTo(initial_homing);
    stepperY.run();
    stepperZ.run();
    initial_homing++;
    //delay(2);
  }
  stepperY.setCurrentPosition(0);
  stepperY.setMaxSpeed(6000.0);
  stepperY.setAcceleration(3000.0);
  stepperZ.setCurrentPosition(0);
  stepperZ.setMaxSpeed(6000.0);
  stepperZ.setAcceleration(3000.0);
  initial_homing = -INIT_Y_HOMING;
  while (!digitalRead(ylimit)) {
    stepperY.moveTo(initial_homing);
    stepperZ.moveTo(initial_homing);
    stepperY.run();
    stepperZ.run();
    initial_homing--;
    //delay(2);
  }
  stepperY.setCurrentPosition(0);
  stepperZ.setCurrentPosition(0);
  //Serial.println("Y homing Done");
  preY =0;
  preZ=0;
}
void homeZ()
{
  stepperY.setMaxSpeed(900);
  stepperY.setAcceleration(200);
  stepperZ.setMaxSpeed(900);
  stepperZ.setAcceleration(200);
  long homingy = INIT_Y_HOMING;
  long homingz = -INIT_Z_HOMING;
  while (digitalRead(zlimit)) {
    stepperY.moveTo(homingy);
    stepperZ.moveTo(homingz);
    stepperY.run();
    stepperZ.run();
    homingy--;
    homingz++;
    //delay(2);
  }
  homingy = -INIT_Y_HOMING;
  homingz = INIT_Z_HOMING;
  stepperY.setCurrentPosition(0);
  stepperZ.setCurrentPosition(0);
  //Serial.println("HEHE");
  while (!digitalRead(zlimit)) {
    stepperY.moveTo(homingy);
    stepperZ.moveTo(homingz);
    stepperY.run();
    stepperZ.run();
    homingy++;
    homingz--;
    
    //delay(2);
  }
  stepperY.setCurrentPosition(0);
  stepperZ.setCurrentPosition(0);
  //Serial.println("Z homing Done");
  preY =0;
  preZ= 0;


}
void rotate(int degrees)
{
 // Serial.println(degrees);
  rotator.write(degrees);
  delay(50);
  Serial.print("r");
}
void grip(int grip)
{
  //Serial.print(grip);
  if(grip==1)
  {
    gripper.write(20);
  }
  else if(grip==0)
  {
    gripper.write(0);
  }
  else
  {
    Serial.println("Wrong command");
  }
  delay(50);
  Serial.print("e");
}
void home()
{
    //Serial.println("homing");
    grip(0);
    rotate(0);
    //Serial.println(Serial.availableForWrite());
    //Serial.print("Hiiii");
    //delay(1000);
    homeZ();
    //Serial.println("z");
    homeY();
    //Serial.println("y");
    homeX();
    //Serial.println("x");
    stepperX.setMaxSpeed(3000); 
    stepperX.setAcceleration(10000);
    stepperX.setSpeed(0);
    stepperY.setMaxSpeed(20000);
    stepperY.setAcceleration(8000);
    stepperY.setSpeed(0);
    stepperZ.setMaxSpeed(20000);
    stepperZ.setAcceleration(8000);
    stepperZ.setSpeed(0);
    Serial.println("h");
}
