void setup() {
  // Initialize the onboard LED pin
  pinMode(7, OUTPUT);
  
  // Start the serial communication
  Serial.begin(9600);
}

void loop() {
  // Check if data is available on the serial port
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    
    if (receivedChar == 'H') {
      // Turn on the LED (human detected)
      digitalWrite(7, HIGH);
    } else if (receivedChar == 'A') {
      // Blink the LED (animal detected)
      digitalWrite(7, HIGH);
      delay(500); // Adjust the delay to change blinking speed
      digitalWrite(7, LOW);
      delay(500);
    } else if (receivedChar == 'O' || receivedChar == 'Q') {
      // Turn off the LED (no human or animal detected, or quit signal received)
      digitalWrite(7, LOW);
    }
  }
}
