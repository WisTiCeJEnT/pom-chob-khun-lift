// HC-SR04
const int trigPin = 2;
const int echoPin = 0;
long duration;
int distance;

// L298N
const int out1 = 12;
const int out2 = 14;
const int out3 = 16;
const int out4 = 17;
int pin1;
int pin2;

void setup(){
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(out1, OUTPUT);
  pinMode(out2, OUTPUT);
  pinMode(out3, OUTPUT);
  pinMode(out4, OUTPUT);
  Serial.begin(9600);
}
int ObjDist(){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);  
  duration = pulseIn(echoPin, HIGH);
  distance= duration*0.034/2;
  Serial.println(distance);
  return distance;
}

void goDown(int n){
  if (n == 1){
    pin1 = out1;
    pin2 = out2;
  }
  else{
    pin1 = out3;
    pin2 = out4;
  }
  digitalWrite(pin1, HIGH);
  digitalWrite(pin2, LOW);
}

void goUp(int n){
  if (n == 1){
    pin1 = out1;
    pin2 = out2;
  }
  else{
    pin1 = out3;
    pin2 = out4;
  }
  digitalWrite(pin1, LOW);
  digitalWrite(pin2, HIGH);
}

void goStop(int n){
  if (n == 1){
    pin1 = out1;
    pin2 = out2;
  }
  else{
    pin1 = out3;
    pin2 = out4;
  }
  digitalWrite(pin1, LOW);
  digitalWrite(pin2, LOW);
}

void goFloor(int n, int Floor){
  if (Floor == 1){
    while (ObjDist() < 50 and ObjDist() > 45)
      goDown(n);
  }
  if (Floor == 2){
    while(ObjDist() < 33)
      goDown(n);
    while(ObjDist() > 37)
      goUp(n);
  }
  if (Floor == 3){
    while(ObjDist() < 18)
      goDown(n);
    while(ObjDist() > 22)
      goUp(n);
  }
  if (Floor == 4){
    while(ObjDist() > 5)
      goUp(n);
  }
  goStop(n);
  Serial.print("Arrived Floor ");
  Serial.println(Floor);
}

void loop() {
    delay(5000);
    goFloor(1,1);    
    delay(5000);
    goFloor(1,2);
    delay(5000);
    goFloor(1,3);
    delay(5000);
    goFloor(1,4);
    delay(5000);
}
