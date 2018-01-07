float baseline;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  int sensorValue = analogRead(A0);
  baseline = sensorValue*(5.0/1023.0);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  int SensorValue = analogRead(A0);

  // 5 : Voltage, 1023 maximum output for the device
  float nvoltage = SensorValue*(5.0/1023.0);

  // Equation : new/old * initial sensor length
  float newlen = (nvoltage/baseline)*106;
  float change = newlen - 106;

  // Serial.print("Sensor Value : ");
  // Serial.print(SensorValue);
  // Serial.print("\n");

  // Serial.print("Normalised voltage : ");
  // Serial.print(nvoltage);
  // Serial.print("\n");

  // Serial.print("New length : ");
  // Serial.print(newlen);
  // Serial.print("\n");

  // Serial.print("Change in length : ");
  Serial.print(change * -1);
  Serial.print("\n");
  
  // Serial.print("\n\n");

  delay(100);
}
