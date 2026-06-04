#ifndef GANTRY_H
#define GANTRY_H
#include <AccelStepper.h>
#include <Servo.h>
#define STEPS_PER_REVOLUTION 200
#define xlimit 9
#define ylimit 10
#define zlimit 11
#define INIT_X_HOMING -1
#define INIT_Y_HOMING 1
#define INIT_Z_HOMING -1
#define GRIPPER 39
#define ROTATOR 41
void initGantry();
void moveXYZ(float x , float y ,float z);
void grip(int grip);
void rotate(int rotate);
void home();
#endif
