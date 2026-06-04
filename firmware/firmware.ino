#include "gantry.h"
char input[128];                            // Buffer to store the command
void setup() {
  initGantry();
  //home();

}

float xyzMovement_g[3][3] =
{
  {100, 0, 0},
  {200, 0, 0},
  {300, 0, 0}
};

int k=0;
void loop() {
  static float distX = 0.0, distY = 0.0, distZ = 0.0;
  int gstate = 0, rot = 0;  
  // Stores XYZ coordinates
  /*
    
  for(int i=0;i<3;i++)
  {
    moveXYZ(xyzMovement_g[i][0],xyzMovement_g[i][1],xyzMovement_g[i][2]);
    gripper(k);
    k=!k;
    delay(100);
  }  
  */                    // Gripper and rotation state
  if (Serial.available() > 0) {
    
    int bytesRead = Serial.readBytesUntil(';', input, sizeof(input) - 1);
    input[bytesRead] = '\0';                          // Null-terminate the string

    // Debugging the raw input
    //Serial.println("Raw Input:");
    //Serial.println(input);

    // Parse the input string
    char* token = strtok(input, " ");
    if (token != NULL) distX = atof(token);           // Parse X coordinate
    else {
      Serial.println("Error: Missing X value.");
      return;
    }

    token = strtok(NULL, " ");
    if (token != NULL) distY = atof(token);           // Parse Y coordinate
    else {
      Serial.println("Error: Missing Y value.");
      return;
    }

    token = strtok(NULL, " ");
    if (token != NULL) distZ = atof(token);           // Parse Z coordinate
    else {
      Serial.println("Error: Missing Z value.");
      return;
    }

    token = strtok(NULL, " ");
    if (token != NULL) gstate = atoi(token);          // Parse gripper state
    else {
      Serial.println("Error: Missing gripper state.");
      return;
    }

    token = strtok(NULL, " ");
    if (token != NULL) rot = atoi(token);             // Parse rotation value
    else {
      Serial.println("Error: Missing rotate value.");
      return;
    }

    // Debugging parsed values
    
    //Serial.print("Parsed Values -> X: ");
    //Serial.println(distX);
    //Serial.print(", Y: ");

    //Serial.println(distY);
    //Serial.print(", Z: ");
    //Serial.println(distZ);
   // Serial.print(", Gripper: ");
    //S0erial.println(Serial.availableForWrite());
    //Serial.println(gstate);
    //Serial.print(", Rotate: ");
    //Serial.println(rot);

    // Execute gantry commands based on parsed input
    if (distX == -1 && distY == -1 && distZ == -1) {
      //Serial.print("Hi");
      home();  // Move the gantry to the home position
      Serial.print("j");
      //Serial.println("Moving to home position.");
    } else {
      grip(gstate);                 // Control the gripper
      rotate(rot);                  // Rotate the servo
      moveXYZ(distX, distY, distZ);  // Move gantry to specified coordinates
      //Serial.println("D69");
      Serial.print("j");
     // Serial.println("XYZ done");
    }
    //Serial.println("DD");
    //Serial.println(Serial.availableForWrite());
    
  }
}
