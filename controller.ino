#include <Servo.h>
Servo xservo;
Servo yservo;

#define trigPin 3
#define echoPin 5
#define gnd 7
////////////////////////variables
long x;
int y;
int posx = 0;
int posy = 0;

///////////////////setup
void setup() {
  // Define inputs and outputs:
  xservo.attach(10);
  yservo.attach(11);
  //Begin Serial communication at a baudrate of 9600:
  Serial.begin(9600);
}
///////////////////////////////main
void loop() {
  String x1;
  String y1;

  if(Serial.available()){  
      x1 = Serial.readStringUntil(':');
      int x = x1.toInt();
//      Serial.println("x:");
//      Serial.println(x1);
      y1 = Serial.readStringUntil('$');
      int y = y1.toInt();
//      Serial.println("y:");
//      Serial.println(y);
  
  x=x-369;
  y=y-261;
  if(x<500 && y<500){
  /////////////////////////pid
  const float targetx = 0;
  const float targety = 0;
  static float xlastError = 0;
  static float xintegral = 0;
   static float ylastError = 0;
  static float yintegral = 0;
  float xerror = x - targetx;
  float yerror = y - targety;  
  xintegral += xerror;  
  yintegral += yerror;
  float xerrorDifference = xerror - xlastError;
  float yerrorDifference = yerror - ylastError;
  posx = 97-0.05*(xerror * 1.5+ xerrorDifference * 20+ xintegral *0);
  posy = 82+0.05*(yerror * 1.5+ yerrorDifference * 20+ yintegral *0);
  posx = constrain(posx, 87, 117);
  posy = constrain(posy, 72,92);
//  Serial.print(posx);
//    Serial.print(posy);
  xservo.write(posx);
  yservo.write(posy);// tell servo to go to position in variable 'pos'
  xlastError = xerror;
  ylastError = yerror;
//  Serial.println("x, y");
//  Serial.println(x);
//  Serial.println(y);
  
  }
  }
}
