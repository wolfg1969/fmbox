/*
 * Douban FM interface
 */
 
void setup() {
  // initialize serial:
  Serial.begin(9600);
  Serial.println("Douban FM interface init.");
}

void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  Serial.print("tuner: ");
  Serial.println(sensorValue);
  delay(1000);     
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
  
  }  
}
