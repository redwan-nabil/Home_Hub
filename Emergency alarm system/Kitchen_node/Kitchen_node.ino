#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <UniversalTelegramBot.h>
#include <WiFiClientSecure.h>
#include <ESP_Mail_Client.h>
#include <PubSubClient.h>
#include "shared_payload.h"

// ==========================================
// CONFIGURATION CREDENTIALS
// ==========================================
const char* ssid = "Syndicate";
const char* password = "586792023-";
const char* mqtt_server = "192.168.0.40"; 

#define BOT_TOKEN "8656067869:AAFSea_-LngpR87IYf_iR6-iyxuqqJ8u_LI"
#define CHAT_ID "1435882929"
#define AUTHOR_EMAIL "nabilredwoan2005@gmail.com"
#define AUTHOR_PASSWORD "uexp klsj jfuq xhkt" 

#define TEST_TRIGGER_PIN 13  

uint8_t receiverMAC[] = {0x68, 0xFE, 0x71, 0x8B, 0x58, 0x50}; 

// ==========================================
// OBJECTS & GLOBALS
// ==========================================
WiFiClientSecure secureClient;         
UniversalTelegramBot bot(BOT_TOKEN, secureClient);

SMTPSession smtp;
WiFiClient espClient;                  
PubSubClient mqtt(espClient);

struct_message myData;
unsigned long lastMqttSend = 0;
unsigned long lastMqttReconnect = 0;
unsigned long lastPinLog = 0; 

// Debounce & Alarm Tracking
bool alarmActive = false;
bool potentialFire = false;
unsigned long fireStartTime = 0;

void setupHybridNetwork() {
    Serial.print("Connecting to Wi-Fi");
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
    Serial.println("\nWi-Fi Connected successfully!");

    // --- COOLING FIX: Lower Wi-Fi Tx Power to reduce heat ---
    WiFi.setTxPower(WIFI_POWER_8_5dBm);

    int32_t channel = WiFi.channel();
    esp_wifi_set_promiscuous(true);
    esp_wifi_set_channel(channel, WIFI_SECOND_CHAN_NONE);
    esp_wifi_set_promiscuous(false);

    if (esp_now_init() != ESP_OK) { Serial.println("ESP-NOW Init Failed"); return; }
    
    esp_now_peer_info_t peerInfo = {};
    memcpy(peerInfo.peer_addr, receiverMAC, 6);
    peerInfo.channel = channel;
    peerInfo.encrypt = false;
    esp_now_add_peer(&peerInfo);

    mqtt.setServer(mqtt_server, 1883);
}

void sendCloudAlert(String msg) {
    secureClient.setTimeout(5000); 
    Serial.println("Sending outbound Telegram panic notification...");
    bot.sendMessage(CHAT_ID, msg, "");
    
    Serial.println("Connecting to Google SMTP Relay Server...");
    Session_Config config;
    config.server.host_name = "smtp.gmail.com";
    config.server.port = 465;
    config.login.email = AUTHOR_EMAIL;
    config.login.password = AUTHOR_PASSWORD;
    
    SMTP_Message message;
    message.sender.name = "Kitchen Node";
    message.sender.email = AUTHOR_EMAIL;
    message.subject = "🚨 EMERGENCY ALARM";
    message.addRecipient("Admin", AUTHOR_EMAIL);
    message.text.content = msg.c_str();
    
    if (smtp.connect(&config)) {
        MailClient.sendMail(&smtp, &message);
        Serial.println("Email notification dispatched!");
    }
}

void setup() {
    Serial.begin(115200);
    // --- FALSE ALARM FIX 1: Internal Pull-Up Resistor ---
    pinMode(TEST_TRIGGER_PIN, INPUT_PULLUP); 
    secureClient.setInsecure(); 
    setupHybridNetwork();
    myData.device_id = 2; 
}

void loop() {
    if (WiFi.status() == WL_CONNECTED) {
        if (!mqtt.connected() && (millis() - lastMqttReconnect > 5000)) {
            if (mqtt.connect("KitchenTestNode")) Serial.println("MQTT Connected to Pi Broker!");
            lastMqttReconnect = millis();
        }
        mqtt.loop();
    }

    int pinValue = digitalRead(TEST_TRIGGER_PIN);
    bool isShortedToGnd = (pinValue == LOW);

    // Keep the Serial Monitor clean with less frequent logging
    if (millis() - lastPinLog > 10000) {
        Serial.print("Heartbeat -> Pin 13 State: "); 
        Serial.println(pinValue == HIGH ? "HIGH (Safe/Open)" : "LOW (SHORTED TO GND)");
        lastPinLog = millis();
    }

    // --- FALSE ALARM FIX 2: Non-Blocking 3-Second Verification ---
    if (isShortedToGnd) {
        if (!potentialFire) {
            // First millisecond the pin drops LOW. Start the timer.
            potentialFire = true;
            fireStartTime = millis();
            Serial.println("Warning: Possible fire detected. Verifying for 3 seconds...");
        } 
        else if (millis() - fireStartTime >= 3000) {
            // Pin has remained LOW continuously for 3+ seconds! Real Fire!
            myData.alert_type = 2; 
            myData.temp = 94.8;    
            myData.pressure = 945.2;
            myData.humidity = 14.5;
            myData.gas_ppm = 8200; 
            myData.battery_volts = 3.62;
            
            esp_now_send(receiverMAC, (uint8_t *) &myData, sizeof(myData)); 

            if (!alarmActive) {
                Serial.println("\n🚨 PIN TRIGGER DETECTED AND VERIFIED! Blasting network alerts!");
                if (mqtt.connected()) mqtt.publish("home/alarms/kitchen", "TRIGGERED");
                
                if (WiFi.status() == WL_CONNECTED) {
                    sendCloudAlert("🚨 KITCHEN PROTOCOL ALERT: FIRE EVENT DETECTED ON PIN 13!");
                }
                alarmActive = true;
            }
        }
    } else {
        // Pin is HIGH (Safe). Reset the timer and system immediately.
        potentialFire = false;
        
        myData.alert_type = 0; 
        myData.temp = 27.4;    
        myData.pressure = 1013.1;
        myData.humidity = 58.0;
        myData.gas_ppm = 145;  
        myData.battery_volts = 4.16;

        if (alarmActive) {
            Serial.println("\n✅ System returned to safe standby.");
            if (mqtt.connected()) mqtt.publish("home/alarms/kitchen", "SAFE");
            alarmActive = false;
        }
    }
    
    // Telemetry Broadcasting
    if (mqtt.connected() && (millis() - lastMqttSend > 3000)) {
        String jsonPayload = "{\"temp\":" + String(myData.temp) + 
                             ",\"hum\":" + String(myData.humidity) +
                             ",\"pressure\":" + String(myData.pressure) + 
                             ",\"gas\":" + String(myData.gas_ppm) + 
                             ",\"batt_volts\":" + String(myData.battery_volts) + "}";
        mqtt.publish("home/sensors/kitchen", jsonPayload.c_str());
        lastMqttSend = millis();
    }

    delay(30); 
}