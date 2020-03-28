
#include "WiFi.h"
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 21
#define RST_PIN 27
#define sw1_1 10
#define sw1_2 13
#define sw1_3 12
#define sw1_4 14
#define sw1_close 27
#define sw1_open 26
#define led1_1 15
#define led1_2 2
#define led1_3 0
#define led1_4 4
#define led1_close 16
#define led1_open 17


MFRC522 mfrc522(SS_PIN, RST_PIN);
String cur_floor;
String url = "http://pckl-api.herokuapp.com";
const char* ssid = "FCnoctisak47";
const char* password =  "jui123456";
char *UID[] = {"99 91 8C A3", "07 72 92 62", "62 82 95 1B", "C7 7E 31 4B"};
String lift_number = "1";
unsigned long stop_time;
void setup() {
  Serial.begin(9600);
  stop_time = millis();
  pinMode(sw1_1, INPUT_PULLUP);
  pinMode(sw1_2, INPUT_PULLUP);
  pinMode(sw1_3, INPUT_PULLUP);
  pinMode(sw1_4, INPUT_PULLUP);
  pinMode(sw1_close, INPUT_PULLUP);
  pinMode(sw1_open, INPUT_PULLUP);
  pinMode(led1_1, OUTPUT);
  pinMode(led1_2, OUTPUT);
  pinMode(led1_3, OUTPUT);
  pinMode(led1_4, OUTPUT);
  pinMode(led1_close, OUTPUT);
  pinMode(led1_open, OUTPUT);
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
    digitalWrite(led1_close, HIGH);
    digitalWrite(led1_open, HIGH);
    delay(100);
    digitalWrite(led1_1, HIGH);
    delay(150);
    digitalWrite(led1_2, HIGH);
    delay(200);
    digitalWrite(led1_3, HIGH);
    delay(250);
    digitalWrite(led1_4, HIGH);
    delay(300);

    digitalWrite(led1_close, LOW);
    digitalWrite(led1_open, LOW);
    delay(100);
    digitalWrite(led1_1, LOW);
    delay(150);
    digitalWrite(led1_2, LOW);
    delay(200);
    digitalWrite(led1_3, LOW);
    delay(250);
    digitalWrite(led1_4, LOW);
    delay(300);

    digitalWrite(led1_close, HIGH);
    digitalWrite(led1_open, HIGH);
    delay(100);
    digitalWrite(led1_4, HIGH);
    delay(150);
    digitalWrite(led1_3, HIGH);
    delay(200);
    digitalWrite(led1_2, HIGH);
    delay(250);
    digitalWrite(led1_1, HIGH);
    delay(300);

    digitalWrite(led1_close, LOW);
    digitalWrite(led1_open, LOW);
    delay(100);
    digitalWrite(led1_4, LOW);
    delay(150);
    digitalWrite(led1_3, LOW);
    delay(200);
    digitalWrite(led1_2, LOW);
    delay(250);
    digitalWrite(led1_1, LOW);
    delay(300);

    digitalWrite(led1_close, HIGH);
    digitalWrite(led1_open, HIGH);
    delay(100);
    digitalWrite(led1_2, HIGH);
    delay(150);
    digitalWrite(led1_4, HIGH);
    delay(200);
    digitalWrite(led1_1, HIGH);
    delay(250);
    digitalWrite(led1_3, HIGH);
    delay(300);

    digitalWrite(led1_close, LOW);
    digitalWrite(led1_open, LOW);
    delay(100);
    digitalWrite(led1_2, LOW);
    delay(150);
    digitalWrite(led1_4, LOW);
    delay(200);
    digitalWrite(led1_1, LOW);
    delay(250);
    digitalWrite(led1_3, LOW);
    delay(300);
  }
  Serial.println("Connected to the WiFi network");
  digitalWrite(led1_close, HIGH);
    digitalWrite(led1_open, HIGH);
    digitalWrite(led1_1, HIGH);
    digitalWrite(led1_2, HIGH);
    digitalWrite(led1_3, HIGH);
    digitalWrite(led1_4, HIGH);
    delay(400);
    digitalWrite(led1_close, LOW);
    digitalWrite(led1_open, LOW);
    digitalWrite(led1_1, LOW);
    digitalWrite(led1_2, LOW);
    digitalWrite(led1_3, LOW);
    digitalWrite(led1_4, LOW);
    
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    delay(1000);

    HTTPClient http_close_open;
    http_close_open.begin("http://pckl-api.herokuapp.com/liftcontrol?lift_no=" + lift_number);
    int httpResponseCode = http_close_open.GET();
    if (httpResponseCode > 0) {
      String response = http_close_open.getString();
      StaticJsonBuffer<500> jsonBuffer;
      JsonObject& root_close_open = jsonBuffer.parseObject(response);
      String close_open = root_close_open["door_open"];
      String oled = root_close_open["oled"];
      cur_floor = oled;
      Serial.println(close_open);
      if (close_open == "1" ) {//|| digitalRead(sw1_close)==LOW
        stop_time = millis() + 6000; //เปิดประตู
        Serial.println("closeopen OK = 1");
      }
      else if (close_open == "0") {
        
        if ((millis() > stop_time)||(digitalRead(sw1_open)==LOW)) { // ส่งไปบอกว่าปิดประตูแล้ว
          Serial.println("closeopen OK = 0");
          String lift_is_closed = "{\"lift_no\":1}";
          http_close_open.addHeader("Content-Type", "application/json");
          int httpResponseCodeFloor = http_close_open.POST(lift_is_closed);
          if (httpResponseCodeFloor > 0) {
            String response = http_close_open.getString();
            Serial.println(response);
          }
          else {
            Serial.println("Error POST");
          }

          http_close_open.end();
        }
      }
    }

    // rfid
    if ( ! mfrc522.PICC_IsNewCardPresent())
    {
      return;
    }
    if ( ! mfrc522.PICC_ReadCardSerial())
    {
      return;
    }
    String content = "";
    byte letter;
    for (byte i = 0; i < mfrc522.uid.size; i++)
    {
      content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : "%20"));
      content.concat(String(mfrc522.uid.uidByte[i], HEX));
    }
    content.toUpperCase();
    // end of rfid

    // get post req.
    HTTPClient http;

    http.begin(url + "/checkpermission?card_id=" + content.substring(1) + "&lift_no=" + lift_number + "&arrival=" + cur_floor);
    httpResponseCode = http.GET();
    if (httpResponseCode > 0) { // ถ้ามากกว่า 0 คือ connect ได้
      String response = http.getString();
      StaticJsonBuffer<500> jsonBuffer;
      JsonObject& root = jsonBuffer.parseObject(response);
      //    const char* av_floor = root["event_id"];
      JsonArray& value0 = root["available_floor"];
      int arraySize = root["available_floor"].size();
      for (int i = 0; i < arraySize; i++) {
        int floor_status = root["available_floor"][i];
        if (i == 0 && floor_status == 1)
          digitalWrite(led1_1, HIGH);
        else if (i == 1 && floor_status == 1)
          digitalWrite(led1_2, HIGH);
        else if (i == 2 && floor_status == 1)
          digitalWrite(led1_3, HIGH);
        else if (i == 3 && floor_status == 1)
          digitalWrite(led1_4, HIGH);
      }
      delay(1000);

      String floor_to_go;
      while (digitalRead(sw1_1) == HIGH && digitalRead(sw1_2) == HIGH && digitalRead(sw1_3) == HIGH && digitalRead(sw1_4) == HIGH) {
        Serial.println("Selecting floor...");
        if (digitalRead(sw1_1) == LOW) {
          floor_to_go = "1";
          Serial.println("Going to 1st floor...");
          break;
        }
        else if (digitalRead(sw1_2) == LOW) {
          floor_to_go = "2";
          Serial.println("Going to 2nd floor...");
          break;
        }
        else if (digitalRead(sw1_3) == LOW) {
          floor_to_go = "3";
          Serial.println("Going to 3rd floor...");
          break;
        }
        else if (digitalRead(sw1_4) == LOW) {
          floor_to_go = "4";
          Serial.println("Going to 4th floor...");
          break;
        }
      }

      digitalWrite(led1_1, LOW);
      digitalWrite(led1_2, LOW);
      digitalWrite(led1_3, LOW);
      digitalWrite(led1_4, LOW);

      Serial.println(response);
      // send the selected floor.
      HTTPClient http_floor;
      http_floor.begin("http://pckl-api.herokuapp.com/useractivity");
      http_floor.addHeader("Content-Type", "application/json");
      String event_id = root["event_id"];

      String liftactivity = "{\"event_id\":" + event_id + ",\"target\":" + floor_to_go + ",\"lift_no\":" + lift_number + "}";
      int httpResponseCodeFloor = http_floor.PATCH(liftactivity);
      if (httpResponseCodeFloor > 0) {
        String response = http_floor.getString();
        Serial.println(response + "FROM POSTING");
      }
      else {
        Serial.println("Error POST");
      }
      http.end();
    }
    else {
      Serial.println(httpResponseCode);
      Serial.println("Error GET");
    }
  }
}
