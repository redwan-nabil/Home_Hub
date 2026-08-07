#include <WiFi.h>

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  // Set Wi-Fi to Station mode to read the true Station MAC Address
  WiFi.mode(WIFI_STA);
  
  Serial.println("\n==========================================");
  Serial.println("   ESP32 MASTER NODE HARDWARE MAC ADDRESS   ");
  Serial.println("==========================================");
  Serial.print("Copy this into your ESP32-C3 code: ");
  Serial.println(WiFi.macAddress());
  Serial.println("==========================================");
}

void loop() {
  // Do nothing
}