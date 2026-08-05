#include <WiFi.h>
#include <PubSubClient.h>
#include <esp_now.h>
#include <ArduinoOTA.h>

// ==========================================
// 1. PIN ASSIGNMENTS & HARDWARE LOGIC
// ==========================================
#define RADAR_OUT_PIN  8    // HLK-LD2410B OUT pin
#define RELAY_PIN      10   // Active-LOW Relay pin
#define RELAY_ON       LOW  // Active-LOW Relay Module (LOW = ON, HIGH = OFF)
#define RELAY_OFF      HIGH

// ==========================================
// 2. NETWORK & MQTT CREDENTIALS
// ==========================================
const char* WIFI_SSID     = "Syndicate";
const char* WIFI_PASSWORD = "586792023-";
const char* MQTT_SERVER   = "192.168.0.40";  // Raspberry Pi HA Broker IP
const int   MQTT_PORT     = 1883;
const char* MQTT_USER     = "redwanmqtt";
const char* MQTT_PASS     = "abcd2005-";

uint8_t masterMacAddress[] = { 0x68, 0xFE, 0x71, 0x8B, 0x58, 0x50 };

WiFiClient espClient;
PubSubClient mqttClient(espClient);

enum OperatingMode { 
  AUTO_MODE,
  FORCE_ON,
  FORCE_OFF 
};
OperatingMode currentMode = AUTO_MODE;

bool lastRelayState = false;
unsigned long lastPresenceTimestamp = 0;
const unsigned long OFF_TIMEOUT_MS = 3000;
unsigned long lastNetworkRetry = 0;

typedef struct struct_message {
  char nodeID[20];
  bool lightActive;
  uint8_t mode; // 0=Auto, 1=ForceON, 2=ForceOFF
} struct_message;
struct_message telemetryPacket;

typedef struct cmd_message {
  uint8_t targetMode; // 0=Auto, 1=ForceON, 2=ForceOFF
} cmd_message;
cmd_message incomingCmd;

// ==========================================
// 3. TELEMETRY & NETWORK BROADCAST
// ==========================================
void transmitStatus(bool state) {
  telemetryPacket.lightActive = state;
  telemetryPacket.mode = (uint8_t)currentMode;

  esp_now_send(masterMacAddress, (uint8_t*)&telemetryPacket, sizeof(telemetryPacket));

  if (mqttClient.connected()) {
    mqttClient.publish("home/bathroom/light/state", state ? "ON" : "OFF", true);
    const char* modeStr = (currentMode == AUTO_MODE) ? "AUTO" : ((currentMode == FORCE_ON) ? "ON" : "OFF");
    mqttClient.publish("home/bathroom/light/mode_state", modeStr, true);
  }
}

// ==========================================
// 4. ESP-NOW COMMAND RECEIVER (RainMaker App Control)
// ==========================================
void onESPNowCommandRecv(const esp_now_recv_info* recv_info, const uint8_t* incomingData, int len) {
  memcpy(&incomingCmd, incomingData, sizeof(incomingCmd));
  
  if (incomingCmd.targetMode == 1) {
    currentMode = FORCE_ON;
    Serial.println("[ESP-NOW CMD] Overrode Light -> FORCE ON");
  } else if (incomingCmd.targetMode == 2) {
    currentMode = FORCE_OFF;
    Serial.println("[ESP-NOW CMD] Overrode Light -> FORCE OFF");
  } else if (incomingCmd.targetMode == 0) {
    currentMode = AUTO_MODE;
    Serial.println("[ESP-NOW CMD] Restored Light -> AUTO MODE");
    // Immediately evaluate radar when returning to Auto
    bool currentPresence = (digitalRead(RADAR_OUT_PIN) == HIGH);
    digitalWrite(RELAY_PIN, currentPresence ? RELAY_ON : RELAY_OFF);
    lastRelayState = currentPresence;
    if (currentPresence) lastPresenceTimestamp = millis();
  }
  transmitStatus(lastRelayState);
}

// ==========================================
// 5. MQTT RECEIVER CALLBACK (HA Manual Override)
// ==========================================
void handleMQTTMessage(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  if (String(topic) == "home/bathroom/light/mode_cmd") {
    if (message == "AUTO") {
      currentMode = AUTO_MODE;
      Serial.println("[OVERRIDE] Mode set to AUTO -> Re-evaluating Radar");
      bool currentPresence = (digitalRead(RADAR_OUT_PIN) == HIGH);
      digitalWrite(RELAY_PIN, currentPresence ? RELAY_ON : RELAY_OFF);
      lastRelayState = currentPresence;
      if (currentPresence) lastPresenceTimestamp = millis();
    } else if (message == "ON") {
      currentMode = FORCE_ON;
      Serial.println("[OVERRIDE] Mode set to FORCE ON");
    } else if (message == "OFF") {
      currentMode = FORCE_OFF;
      Serial.println("[OVERRIDE] Mode set to FORCE OFF");
    }
    transmitStatus(lastRelayState);
  }
}

// ==========================================
// 6. SETUP ROUTINE
// ==========================================
void setup() {
  Serial.begin(115200);
  delay(300);

  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, RELAY_OFF);
  lastRelayState = false;

  pinMode(RADAR_OUT_PIN, INPUT_PULLDOWN);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  if (esp_now_init() == ESP_OK) {
    esp_now_register_recv_cb(onESPNowCommandRecv);
    esp_now_peer_info_t peerInfo = {};
    memcpy(peerInfo.peer_addr, masterMacAddress, 6);
    peerInfo.channel = 0;
    peerInfo.encrypt = false;
    esp_now_add_peer(&peerInfo);
  }

  mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
  mqttClient.setCallback(handleMQTTMessage);

  ArduinoOTA.setHostname("Redwan-Bathroom-Node");
  ArduinoOTA.setPassword("abcd2005-");
  ArduinoOTA.begin();

  strcpy(telemetryPacket.nodeID, "REDWAN-BATH-NODE");
  Serial.println("[BOOT] REDWAN-BATH-NODE Online!");
}

// ==========================================
// 7. MAIN PRODUCTION LOOP
// ==========================================
void loop() {
  // 1. STATE MACHINE & CONTINUOUS RELAY ENFORCEMENT
  if (currentMode == AUTO_MODE) {
    bool currentPresence = (digitalRead(RADAR_OUT_PIN) == HIGH);

    if (currentPresence) {
      lastPresenceTimestamp = millis();
      if (!lastRelayState) {
        digitalWrite(RELAY_PIN, RELAY_ON);
        lastRelayState = true;
        transmitStatus(true);
        Serial.println("[RADAR] Occupied -> Light ON");
      }
    } else {
      if (lastRelayState && (millis() - lastPresenceTimestamp >= OFF_TIMEOUT_MS)) {
        digitalWrite(RELAY_PIN, RELAY_OFF);
        lastRelayState = false;
        transmitStatus(false);
        Serial.println("[RADAR] Clear -> Light OFF");
      }
    }
  } 
  else if (currentMode == FORCE_ON) {
    // Continually enforce physical ON state so it NEVER fails to switch
    digitalWrite(RELAY_PIN, RELAY_ON);
    if (!lastRelayState) {
      lastRelayState = true;
      transmitStatus(true);
    }
  } 
  else if (currentMode == FORCE_OFF) {
    // Continually enforce physical OFF state
    digitalWrite(RELAY_PIN, RELAY_OFF);
    if (lastRelayState) {
      lastRelayState = false;
      transmitStatus(false);
    }
  }

  // 2. NETWORK & OTA MAINTENANCE
  if (WiFi.status() == WL_CONNECTED) {
    ArduinoOTA.handle();

    if (!mqttClient.connected()) {
      if (millis() - lastNetworkRetry > 5000) {
        lastNetworkRetry = millis();
        if (mqttClient.connect("REDWAN-BATH-NODE", MQTT_USER, MQTT_PASS)) {
          mqttClient.subscribe("home/bathroom/light/mode_cmd");
          transmitStatus(lastRelayState);
        }
      }
    } else {
      mqttClient.loop();
    }
  }

  delay(10);
}