#include "WiFi.h"
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define motor_1_1 12
#define motor_1_2 14
#define motor_2_1 10
#define motor_2_2 13
#define sw1 15
#define sw2_up 0
#define sw2_down 16
#define sw3_up 5
#define sw3_down 19
#define sw4 22
#define led1 2
#define led2_up 4
#define led2_down 17
#define led3_up 18
#define led3_down 21
#define led4 23

#define enable1Pin 27
#define enable2Pin 27

const char* ssid = "FCnoctisak47";
const char* password = "jui123456";
// HC-SR04
const int trigPin = 25;
const int echoPin = 26;
long duration;
int distance;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(motor_1_1, OUTPUT);
  pinMode(motor_1_2, OUTPUT);
  pinMode(motor_2_1, OUTPUT);
  pinMode(motor_2_2, OUTPUT);
  pinMode(sw1, INPUT_PULLUP);
  pinMode(sw2_up, INPUT_PULLUP);
  pinMode(sw2_down, INPUT_PULLUP);
  pinMode(sw3_up, INPUT_PULLUP);
  pinMode(sw3_down, INPUT_PULLUP);
  pinMode(sw4, INPUT_PULLUP);
  pinMode(led1, OUTPUT);
  pinMode(led2_up, OUTPUT);
  pinMode(led2_down, OUTPUT);
  pinMode(led3_up, OUTPUT);
  pinMode(led3_down, OUTPUT);
  pinMode(led4, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  pinMode(enable2Pin, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  ledcSetup(0,30000,8);
  ledcAttachPin(enable1Pin,0);
  ledcAttachPin(enable2Pin,0);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
    digitalWrite(led1,HIGH);
    digitalWrite(led2_up,HIGH);
    digitalWrite(led2_down,HIGH);
    digitalWrite(led3_up,HIGH);
    digitalWrite(led3_down,HIGH);
    digitalWrite(led4,HIGH);
  
  }
  Serial.println("Connected to the WiFi network");
  digitalWrite(led1,LOW);
    digitalWrite(led2_up,LOW);
    digitalWrite(led2_down,LOW);
    digitalWrite(led3_up,LOW);
    digitalWrite(led3_down,LOW);
    digitalWrite(led4,LOW);
  
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

void loop() {
  // put your main code here, to run repeatedly:
  delay(1000);
  if (WiFi.status() == WL_CONNECTED) {
    // กดเลือกขึ้นลงจากข้างนอก
    HTTPClient http_up_down;
    http_up_down.begin("http://pckl-api.herokuapp.com/liftcall");
    http_up_down.addHeader("Content-Type", "application/json");
    String selected_payload = "";
    String up = "\"UP\"";
    String down = "\"DOWN\"";
    String going = "{\"going\":";
    if (digitalRead(sw1) == LOW) {
      selected_payload = going + up + ",\"floor\":1}";
    }
    else if (digitalRead(sw2_up) == LOW) {
      selected_payload = going + up + ",\"floor\":2}";

    }
    else if (digitalRead(sw2_down) == LOW) {
      selected_payload = going + down + ",\"floor\":2}";

    }
    else if (digitalRead(sw3_up) == LOW) {
      selected_payload = going + up + ",\"floor\":3}";

    }
    else if (digitalRead(sw3_down) == LOW) {
      selected_payload = going + down + ",\"floor\":3}";

    }
    else if (digitalRead(sw4) == LOW) {
      selected_payload = going + down + ",\"floor\":4}";
    }

    if (selected_payload != "") {
      Serial.println("this is selected payload : " + selected_payload);
      int httpResponse = http_up_down.POST(selected_payload);
      if (httpResponse > 0) {
        String response = http_up_down.getString();
        Serial.println(response);
        Serial.println("Post your choices (up or down) already .");
      }
      else {
        Serial.println("Error POST from outside elevator.");
      }
      http_up_down.end();
    }
    Serial.println("selected payload is null.");

    string c_floor;
    if (ObjDist() > 50)
      c_floor = "1";
    else if (ObjDist() > 37)
      c_floor = "2";
    else if (ObjDist() > 22)
      c_floor = "3";
    else 
      c_floor = "4";
    // กดดเลือกชั้นในลิฟท์
    HTTPClient http;
    http.begin("http://pckl-api.herokuapp.com/liftstatus");
    http.addHeader("Content-Type", "application/json");
    int httpResponse = http.POST("{\"lift_position\": "+c_floor+"}");
    if (httpResponse > 0) {
      String response = http.getString();
      Serial.println(response);
      StaticJsonBuffer<500> jsonBuffer;
      JsonObject& root = jsonBuffer.parseObject(response);
      String lift_1_move = root["lift_1_move"];
      String lift_2_move = root["lift_2_move"];
      String x1_up = root["1_UP"];
      String x2_up = root["2_UP"];
      String x2_down = root["2_DOWN"];
      String x3_up = root["3_UP"];
      String x3_down = root["3_DOWN"];
      String x4_down = root["4_DOWN"];
        if (x1_up == "0")
            digitalWrite(led1, LOW);
        else if (x1_up == "1")
          digitalWrite(led1, HIGH);
        if (x2_up == "0")
          digitalWrite(led2_up, LOW);
        else if (x2_up == "1")
          digitalWrite(led2_up, HIGH);
        if (x2_down == "0")
          digitalWrite(led2_down, LOW);
        else if (x2_down == "1")
          digitalWrite(led2_down, HIGH);
        if (x3_up == "0")
          digitalWrite(led3_up, LOW);
        else if (x3_up == "1")
          digitalWrite(led3_up, HIGH);
          if (x3_down == "0")
          digitalWrite(led3_down, LOW);
        else if (x3_down == "1")
          digitalWrite(led3_down, HIGH);
          if (x4_down == "0")
          digitalWrite(led4, LOW);
        else if (x4_down == "1")
          digitalWrite(led4, HIGH);

        if (lift_1_move == "0") {
        digitalWrite(motor_1_1, LOW);
        digitalWrite(motor_1_2, LOW);
        Serial.println("lift_1_move=0");
        delay(2000);
      }
      else if (lift_1_move == "1") {
        digitalWrite(motor_1_1, HIGH);
        digitalWrite(motor_1_2, LOW);
        ledcWrite(0,195 );
        Serial.println("lift_1_move=1");
        delay(2000);
      }
      else if (lift_1_move == "-1") {
        digitalWrite(motor_1_1, LOW);
        digitalWrite(motor_1_2, HIGH);
        ledcWrite(0,195 );
        Serial.println("lift_1_move=-1");
        delay(2000);
      }
      if (lift_2_move == "0") {
        digitalWrite(motor_2_1, LOW);
        digitalWrite(motor_2_2, LOW);
        Serial.println("lift_2_move=0");
        delay(2000);
      }
      else if (lift_2_move == "1") {
        digitalWrite(motor_2_1, HIGH);
        digitalWrite(motor_2_2, LOW);
        ledcWrite(0,195 );
        Serial.println("lift_2_move=1");
        delay(2000);
      }
      else if (lift_2_move == "-1") {
        digitalWrite(motor_2_1, LOW);
        digitalWrite(motor_2_2, HIGH);
        ledcWrite(0,195 );
        Serial.println("lift_2_move=-1");
        delay(2000);
      }
    }
    else {
      Serial.println("Error POST");
    }
    http.end();
  }

}