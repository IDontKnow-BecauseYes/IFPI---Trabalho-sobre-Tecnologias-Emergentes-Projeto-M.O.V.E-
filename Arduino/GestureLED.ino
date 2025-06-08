#define BLUE_PIN 9
#define RED_PIN 10
#define GREEN_PIN 11

void setup() {
  Serial.begin(9600);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('
');
    cmd.trim();

    if (cmd == "ALL_ON") {
      digitalWrite(BLUE_PIN, HIGH);
      digitalWrite(RED_PIN, HIGH);
      digitalWrite(GREEN_PIN, HIGH);
    } else if (cmd == "ALL_OFF") {
      digitalWrite(BLUE_PIN, LOW);
      digitalWrite(RED_PIN, LOW);
      digitalWrite(GREEN_PIN, LOW);
    } else if (cmd == "BLUE_ON") {
      digitalWrite(BLUE_PIN, HIGH);
      digitalWrite(RED_PIN, LOW);
      digitalWrite(GREEN_PIN, LOW);
    } else if (cmd == "RED_ON") {
      digitalWrite(BLUE_PIN, LOW);
      digitalWrite(RED_PIN, HIGH);
      digitalWrite(GREEN_PIN, LOW);
    } else if (cmd == "GREEN_ON") {
      digitalWrite(BLUE_PIN, LOW);
      digitalWrite(RED_PIN, LOW);
      digitalWrite(GREEN_PIN, HIGH);
    }
    Serial.println("OK");
  }
}
