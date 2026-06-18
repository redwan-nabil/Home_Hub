#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h> 
#include "shared_payload.h"

struct_message receivedData;

// Core 3.x Compliant Asynchronous Data Reception Callback
void OnDataRecv(const esp_now_recv_info_t * recvInfo, const uint8_t *incomingBytes, int len) {
    if (len == sizeof(struct_message)) {
        memcpy(&receivedData, incomingBytes, sizeof(receivedData));
        
        Serial.println("\n========= 📡 DIRECT RF PACKET CAUGHT =========");
        Serial.print("Source Device ID: "); Serial.println(receivedData.device_id);
        Serial.print("Alert Type Flag:  "); Serial.println(receivedData.alert_type);
        Serial.print("Spoofed Temp:    "); Serial.print(receivedData.temp, 1); Serial.println(" C");
        Serial.print("Spoofed Baro:    "); Serial.print(receivedData.pressure, 1); Serial.println(" hPa");
        Serial.print("Spoofed Gas:     "); Serial.print(receivedData.gas_ppm); Serial.println(" PPM");
        Serial.print("UPS Cell Rail:   "); Serial.print(receivedData.battery_volts, 2); Serial.println(" V");
        Serial.println("================================================\n");
    }
}

void setup() {
    Serial.begin(115200);
    delay(1500); // Ensures the Arduino IDE Serial Monitor interface window is active
    
    Serial.println("Initializing Master Receiver Node Stack...");
    
    // 1. Initialize Wi-Fi Mode Profile
    WiFi.mode(WIFI_STA);
    delay(100);
    
    // 2. Initialize ESP-NOW FIRST (Forces the network subsystem baseband to wake up)
    if (esp_now_init() != ESP_OK) {
        Serial.println("!!! Critical Error Initializing ESP-NOW Stack !!!");
        return;
    }
    
    // 3. Attach incoming parsing function handler
    esp_now_register_recv_cb(OnDataRecv);
    
    // 4. Extract and print out the REAL factory hardware identity address
    Serial.print("\n-> Master Node TRUE MAC Address: ");
    String trueMAC = WiFi.macAddress();
    Serial.println(trueMAC);
    Serial.println("COPY THIS ADDRESS AND MATCH IT IN YOUR KITCHEN SKETCH ARRAY!\n");

    // 5. Lock radio frequency onto your local network's channel
    // Note: If your home router defaults to another channel, match this value to it!
    int32_t targetChannel = 6; 
    esp_wifi_set_promiscuous(true);
    esp_wifi_set_channel(targetChannel, WIFI_SECOND_CHAN_NONE);
    esp_wifi_set_promiscuous(false);
    
    Serial.print("-> Radio frequency successfully locked onto Channel: ");
    Serial.println(targetChannel);
    Serial.println("Awaiting incoming hardware emergency airwaves...");
}

void loop() {
    // Left empty intentionally: Network packages read via hardware interrupts
}