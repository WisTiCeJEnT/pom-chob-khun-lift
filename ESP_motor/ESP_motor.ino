void setup() {
  pinMode(12, OUTPUT);
  pinMode(14, OUTPUT);
}

void loop() {
  digitalWrite(12, HIGH);
  digitalWrite(14, LOW);
  delay(2000);

  digitalWrite(12, LOW);
  digitalWrite(14, LOW);
  delay(2000);

  digitalWrite(12, LOW);
  digitalWrite(14, HIGH);
  delay(2000);

  digitalWrite(12, LOW);
  digitalWrite(14, LOW);
  delay(2000);
}
