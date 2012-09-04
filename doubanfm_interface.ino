/*
 * Douban FM interface
 */
 
void setup()
{
  Serial.begin(9600);
  Serial.println("Douban FM interface init.");
}

void loop()
{
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  Serial.print("tuner: ");
  Serial.println(sensorValue);
  delay(1000);     
}
