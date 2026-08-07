# REDWAN-BATH-NODE  
### Smart Bathroom Presence Sensor (ESP32-C3 + HLK-LD2410B + Relay)

Industrial-style, humidity-resilient bathroom automation node with dual wireless telemetry (ESP-NOW + MQTT), OTA firmware updates, and long-life electrical protection design.

> ⚠️ **Mains Safety Warning**  
> This project includes **220V AC mains wiring**. If you are not trained in electrical safety, do not build or test the high-voltage section without supervision from a qualified electrician.

---

## Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. Core Features](#2-core-features)
- [3. Hardware BOM (Primary + Bangladesh Alternatives)](#3-hardware-bom-primary--bangladesh-alternatives)
- [4. System Architecture](#4-system-architecture)
- [5. Complete Pinout & Interconnection](#5-complete-pinout--interconnection)
- [6. Firmware Requirements](#6-firmware-requirements)
- [7. Production Firmware (`redwan-bath-node.ino`)](#7-production-firmware-redwan-bath-nodeino)
- [8. LD2410B Gate Calibration Blueprint](#8-ld2410b-gate-calibration-blueprint)
- [9. Bench Test & Permanent Build Guide](#9-bench-test--permanent-build-guide)
- [10. Troubleshooting Matrix](#10-troubleshooting-matrix)
- [11. Export This Guide to PDF](#11-export-this-guide-to-pdf)
- [12. License & Responsibility](#12-license--responsibility)

---

## 1. Project Overview

`REDWAN-BATH-NODE` is a smart bathroom occupancy automation node designed for high uptime in humid environments.

It combines:

- **ESP32-C3** controller
- **HLK-LD2410B 24GHz mmWave radar**
- **Active-LOW 5V relay (or SSR)**
- **Isolated AC-DC mains power module**
- **Surge + inrush + contact arc protection**

The design objective is **10–20 year service reliability** with proper assembly, enclosure sealing, and electrical protection.

---

## 2. Core Features

- ✅ **Human micro-motion detection** (including subtle chest breathing)
- ✅ **Fast local lighting response**
- ✅ **Auto / Force ON / Force OFF operating modes**
- ✅ **Dual telemetry redundancy**
  - ESP-NOW → local master hub
  - MQTT → Home Assistant broker
- ✅ **OTA firmware updates**
- ✅ **Active-LOW relay safety logic**
- ✅ **Anti-chatter delayed OFF logic**
- ✅ **Humidity-aware PCB isolation strategy**

---

## 3. Hardware BOM (Primary + Bangladesh Alternatives)

| Primary Component | Engineering Function | Validated Local Alternative | Long-Life Design Note |
|---|---|---|---|
| **HLK-PM01 (5V 3W)** | Isolated AC-to-DC converter | HLK-5M05, HLK-10M05, Mean Well IRM-03-5 | Encapsulated isolated SMPS for mains safety |
| **ESP32-C3 SuperMini** | Main MCU + Wi-Fi/BLE | ESP32-C3 Zero, ESP32 DevKitC WROOM-32 | Compact RISC-V controller |
| **HLK-LD2410B (24GHz)** | Presence sensing radar | LD2410C, LD2420 | Detects motion + micro-motion |
| **5V Relay (Active-LOW)** | 220V load switching | G3MB-202P SSR | SSR preferred for silent wear-free switching |
| **1A Fuse + Holder** | Overcurrent protection | 1A 250V micro fuse, 1A PPTC | Primary line fault protection |
| **10D471K MOV** | Surge suppression | 7D471K, 14D471K | Clamps high-voltage transients |
| **10Ω 2W resistor** | Inrush limiting | 10D-9 NTC or flameproof 10Ω | Protects SMPS during cold start |
| **0.1µF X2 (275VAC)** | Snubber capacitor | 100nF 275–310VAC X2 | Must be **X2 safety rated** |
| **100Ω 2W resistor** | Snubber series resistor | Metal film / metal oxide | With X2 cap across COM-NO |
| **220µF 16V capacitor** | 5V rail pulse buffering | 330µF / 470µF 16V | Prevents ESP brownout from radar spikes |

---

## 4. System Architecture

The PCB is split into two physical zones:

- **Zone A:** High-voltage AC mains (220V)
- **Zone B:** Low-voltage DC logic (5V / 3.3V)

A **2mm isolation slot** must be cut through the PCB between both zones to prevent humid-surface creepage tracking.

### High-Level Wiring Diagram

```text
ZONE A (AC MAINS)
L -> Fuse -> 10Ω Inrush -> HLK-PM01 (AC-L)
N -----------------------> HLK-PM01 (AC-N)
MOV across L-N
Snubber (X2 + 100Ω series) across Relay COM-NO
Relay COM from Live, Relay NO to bathroom light live

[ 2mm physical PCB isolation slot ]

ZONE B (LOW VOLTAGE)
HLK-PM01 +5V -> ESP32 VIN, LD2410B VCC, Relay VCC
HLK-PM01 GND -> ESP32 GND, LD2410B GND, Relay GND
LD2410B OUT -> ESP32 GPIO8
Relay IN -> ESP32 GPIO10
220µF capacitor across +5V and GND rails
```

### Why Isolation Slot Is Mandatory

In high humidity, dust + moisture can create a conductive film over PCB surfaces.  
The 2mm air gap interrupts this creepage path and significantly improves long-term electrical safety.

---

## 5. Complete Pinout & Interconnection

| Sub-Assembly | Pin / Terminal | ESP32-C3 Pin | Rail / Track | Purpose |
|---|---|---|---|---|
| HLK-PM01 | AC `L` | — | Fused live | Mains input line |
| HLK-PM01 | AC `N` | — | Neutral | Mains return |
| HLK-PM01 | `+VO` | `VIN/5V` | 5V rail | DC supply |
| HLK-PM01 | `-VO` | `GND` | Ground rail | Common reference |
| LD2410B | `VCC` | — | 5V rail | Radar power |
| LD2410B | `GND` | — | GND rail | Radar reference |
| LD2410B | `OUT` | `GPIO8` | Signal input | Presence logic |
| Relay | `VCC` | — | 5V rail | Relay power |
| Relay | `GND` | — | GND rail | Relay reference |
| Relay | `IN` | `GPIO10` | Signal output | Active-LOW trigger |
| Relay | `COM` | — | Fused live | AC input contact |
| Relay | `N.O.` | — | Light live | Switched output |
| 220µF cap | `+` | — | 5V rail | Pulse buffering |
| 220µF cap | `-` | — | GND rail | Buffer return |
| Snubber | X2 + 100Ω | — | COM ↔ N.O. | Arc suppression |

---

## 6. Firmware Requirements

### Board Manager

- Platform: **esp32 by Espressif Systems** (recommended 3.x.x)
- Board: **ESP32C3 Dev Module** or **ESP32-C3 SuperMini**
- USB CDC On Boot: **Enabled**
- Flash / Partition: **4MB default with SPIFFS**

### Libraries

- `WiFi.h`
- `PubSubClient.h` (Nick O'Leary)
- `esp_now.h`
- `ArduinoOTA.h`

---

## 7. Production Firmware (`redwan-bath-node.ino`)

Create file: `redwan-bath-node.ino`

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <esp_now.h>
#include <ArduinoOTA.h>

// ==========================================
// 1. PIN ASSIGNMENTS & HARDWARE LOGIC
// ==========================================
#define RADAR_OUT_PIN  8
#define RELAY_PIN      10
#define RELAY_ON       LOW
#define RELAY_OFF      HIGH

// ==========================================
// 2. NETWORK & MQTT CREDENTIALS
// ==========================================
const char* WIFI_SSID     = "Syndicate";
const char* WIFI_PASSWORD = "586792023-";
const char* MQTT_SERVER   = "192.168.0.40";
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
  uint8_t mode;
} struct_message;
struct_message telemetryPacket;

typedef struct cmd_message {
  uint8_t targetMode;
} cmd_message;
cmd_message incomingCmd;

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
    bool currentPresence = (digitalRead(RADAR_OUT_PIN) == HIGH);
    digitalWrite(RELAY_PIN, currentPresence ? RELAY_ON : RELAY_OFF);
    lastRelayState = currentPresence;
    if (currentPresence) lastPresenceTimestamp = millis();
  }
  transmitStatus(lastRelayState);
}

void handleMQTTMessage(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (unsigned int i = 0; i < length; i++) message += (char)payload[i];

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

void loop() {
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
  } else if (currentMode == FORCE_ON) {
    digitalWrite(RELAY_PIN, RELAY_ON);
    if (!lastRelayState) {
      lastRelayState = true;
      transmitStatus(true);
    }
  } else if (currentMode == FORCE_OFF) {
    digitalWrite(RELAY_PIN, RELAY_OFF);
    if (lastRelayState) {
      lastRelayState = false;
      transmitStatus(false);
    }
  }

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
```

---

## 8. LD2410B Gate Calibration Blueprint

For a ~2.2m bathroom depth:

- **Max Moving Gate = 3**
- **Max Static Gate = 3**
- **Unmanned Duration = 5s**

### Suggested Sensitivity Profile

| Gate | Zone | Moving | Static |
|---|---|---:|---:|
| Gate 0 | Door threshold | 60 | 40 |
| Gate 1 | Sink/vanity | 60 | 40 |
| Gate 2 | Toilet zone (micro-motion critical) | 50 | 15–20 |
| Gate 3+ | Outside bathroom/hallway | 0 | 0 |

> Note: In HLKRadarTool, lower static value generally means higher sensitivity to subtle still-body motion.

---

## 9. Bench Test & Permanent Build Guide

### A) Low-Voltage Bench Test (Before Mains Wiring)

1. Connect 5V/GND + radar OUT + relay input.
2. Upload firmware and open Serial Monitor (`115200`).
3. Trigger presence and confirm immediate relay ON behavior.
4. Clear area and verify delayed OFF behavior (`OFF_TIMEOUT_MS` after sensor unmanned state).

### B) Permanent Build (High Voltage + Enclosure)

1. Cut **2mm PCB isolation slot** between AC and DC zones.
2. Build AC zone (fuse, MOV, inrush, snubber, relay line path).
3. Build DC zone (ESP32 headers, radar wiring, 220µF+ bulk cap).
4. Clean and coat PCB bottom (except antennas/fuse), then mount in **IP65/IP67** enclosure.

---

## 10. Troubleshooting Matrix

| Symptom | Root Cause | Action |
|---|---|---|
| ESP32 bootloop / reset | 5V rail dip from radar burst current | Add 220–470µF capacitor close to VIN/GND |
| Relay chatter or arcing | Inductive/capacitive load transient | Verify X2 + 100Ω snubber across COM-NO |
| Hallway false trigger | Radar range too deep | Set max moving/static gate to `3` |
| Light off while user is still | Static sensitivity too weak | Gate 2 static: lower to `15–20` |
| OTA not visible | mDNS/routing/firewall issue | Confirm hostname, LAN routing, and network port visibility |

---

## 11. Export This Guide to PDF

- In VS Code: Open Markdown Preview → Print → Save as PDF
- In Browser: `Ctrl/Cmd + P` → Destination: Save as PDF → disable headers/footers

---

## 12. License & Responsibility

You are responsible for safe implementation of mains electrical sections and local electrical code compliance.  
Use proper insulation, enclosure, strain relief, and isolation methods during installation.

For open-source sharing, add your preferred license file (`MIT`, `Apache-2.0`, etc.) to the repository.