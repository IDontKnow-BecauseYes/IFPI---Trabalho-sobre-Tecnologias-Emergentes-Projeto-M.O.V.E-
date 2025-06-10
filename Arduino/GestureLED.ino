// programa: detector gestual sem fio
// autor: por enquanto Antonio Carlos

#define STATE_PIN 7
#define BLUE_PIN 8
#define RED_PIN 9
#define GREEN_PIN 10

bool wasConnected = false;

void setup() {
  Serial.begin(9600);
  pinMode(STATE_PIN, INPUT);
  pinMode(BLUE_PIN, OUTPUT);
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
}

void loop() {
  // Verifica conexão Bluetooth
  bool isConnected = digitalRead(STATE_PIN);

  if (isConnected && !wasConnected) {
    // Conectado agora, mas não estava antes — piscar LEDs
    for (int i = 0; i < 2; i++) {
      digitalWrite(BLUE_PIN, HIGH);
      digitalWrite(RED_PIN, HIGH);
      digitalWrite(GREEN_PIN, HIGH);
      delay(200);
      digitalWrite(BLUE_PIN, LOW);
      digitalWrite(RED_PIN, LOW);
      digitalWrite(GREEN_PIN, LOW);
      delay(200);
    }
    wasConnected = true;
  } else if (!isConnected) {
    wasConnected = false;
  }

  // Verifica comandos recebidos
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "ALL_ON") {
      digitalWrite(BLUE_PIN, HIGH);
      digitalWrite(RED_PIN, HIGH);
      digitalWrite(GREEN_PIN, HIGH);
      delay(1000);
    } else if (cmd == "ALL_OFF") {
      digitalWrite(BLUE_PIN, LOW);
      digitalWrite(RED_PIN, LOW);
      digitalWrite(GREEN_PIN, LOW);
      delay(1000);
    } else if (cmd == "BLUE_ON") {
      digitalWrite(BLUE_PIN, HIGH);
      digitalWrite(RED_PIN, LOW);
      digitalWrite(GREEN_PIN, LOW);
      delay(1000);
    } else if (cmd == "RED_ON") {
      digitalWrite(BLUE_PIN, LOW);
      digitalWrite(RED_PIN, HIGH);
      digitalWrite(GREEN_PIN, LOW);
      delay(1000);
    } else if (cmd == "GREEN_ON") {
      digitalWrite(BLUE_PIN, LOW);
      digitalWrite(RED_PIN, LOW);
      digitalWrite(GREEN_PIN, HIGH);
      delay(1000);
    }

    Serial.println("OK");
  }
}
