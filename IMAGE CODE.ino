int humanLED = 8;
int animalLED = 7;
int buzzer = 9;
int relay = 10;

void setup() {
  // Initialize the pins as outputs
  pinMode(humanLED, OUTPUT);
  pinMode(animalLED, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(relay, OUTPUT);
  
  // Start the serial communication
  Serial.begin(9600);
}

void loop() {
  // Check if data is available on the serial port
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    
    if (receivedChar == 'H') {
      digitalWrite(humanLED, HIGH);
      digitalWrite(animalLED, LOW);
      digitalWrite(buzzer, HIGH);
      digitalWrite(relay, LOW);
      
    } 
    else if (receivedChar == 'A') {
      digitalWrite(animalLED, HIGH);
      digitalWrite(humanLED, LOW);
      digitalWrite(buzzer, LOW);
      digitalWrite(relay, HIGH);
      
    }
    else if (receivedChar == 'B') { // Assuming 'B' stands for both Human and Animal detected
      digitalWrite(humanLED, LOW);
      digitalWrite(animalLED, LOW);
      digitalWrite(buzzer, HIGH);
      digitalWrite(relay, HIGH);
    }
    else if (receivedChar == 'O' || receivedChar == 'Q') {
      digitalWrite(humanLED, LOW);
      digitalWrite(animalLED, LOW);
      digitalWrite(buzzer, LOW);
      digitalWrite(relay, HIGH);
    }
  }
}
