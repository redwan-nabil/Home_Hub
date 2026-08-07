# SMART BATHROOM PRESENCE & MASTER AUTOMATION HUB

## PART 2: MASTER CENTER NODE (`CENTER_NODE`) TECHNICAL REFERENCE

### 2.1 Complete Siren Hub & Lifetime Reliability Circuit Schematic

The Master Center Hub uses an ESP32 WROOM-32 DevKit board to bridge local ESP-NOW RF packets to your local Home Assistant MQTT server and Espressif ESP RainMaker cloud. It controls a high-decibel industrial siren via GPIO 18 and includes heavy-duty filtering for 10–20 year continuous uptime.

```text
===================================================================================
MASTER HUB LIFETIME DC POWER & SIREN ACTUATING SCHEMATIC
===================================================================================

  5V 2A Industrial DC Supply (VCC) ───┬───────────────────────────────────> [ ESP32 WROOM 5V (VIN) ]
                                      │
                                      ├─── [ 470µF 16V Electrolytic Cap ] ──┐  Bulk RF Buffer
                                      │                                     │
                                      ├─── [ 0.1µF Ceramic Decoupling Cap ]─┤  High-Freq Noise Filter
                                      │                                     │
  Common Ground (GND) ────────────────┼─────────────────────────────────────┴─> [ ESP32 WROOM GND Pin ]
                                      │
                                      ├───────────────────────────────────────> [ Siren Relay VCC (+) ]
                                      │
                                      │        +─── [ 1N4007 Diode (Reverse) ] ───+
                                      │        │                                  │
                                      │  ┌─────┴──────┐                     ┌─────┴──────┐
                                      │  │ Relay COM  │── Fused 220V Live ──│ Relay N.O. │──> To Industrial
                                      │  └────────────┘                     └────────────┘    Siren Horn
                                      │
  ESP32 WROOM [ GPIO 18 ] ────────────┴───────────────────────────────────────> [ Siren Relay IN (Signal) ]

  ESP32 WROOM [ GPIO 0 ] ───────────── [ Physical Push Button ] ──────────────> [ Common Ground (GND) ]
                                       (Hold 5s on boot for RainMaker Factory Reset & Cloud Unclaim)
===================================================================================
```

---

### 2.2 Comprehensive Master Node Pinout & Component Table

| Component | Pin / Terminal | ESP32 WROOM Pin | Board Track / Connection | Technical Function & Description |
|---|---|---|---|---|
| 5V 2A Power Supply | +5V / GND | VIN / GND | Common DC Rails | Heavy-duty external power supply rail for continuous 24/7 uptime. |
| 470µF 16V Capacitor | (+) / (-) | — | Across VIN / GND | Bulk power reservoir prevents ESP32 brownout during RF Wi-Fi/BLE spikes. |
| 0.1µF Ceramic Cap | Pin 1 / Pin 2 | — | Across VIN / GND | Filters high-frequency switching noise from Wi-Fi radio transmissions. |
| Industrial Siren Relay | VCC / GND | — | 5V Rail / GND Rail | Power supply for mechanical or SSR siren switching module. |
| Industrial Siren Relay | IN (Signal) | GPIO 18 | Logic Output Track | Active-HIGH trigger line (HIGH = ALARM, LOW = SAFE). |
| 1N4007 Diode | Anode / Cathode | — | Across Relay Coil | Flyback diode suppresses reverse EMF inductive kickback across coil. |
| PROV / BOOT Button | Pin 1 / Pin 2 | GPIO 0 / GND | Input Pull-Up Track | Holding for 5s erases NVS Wi-Fi credentials and resets RainMaker claim. |

---

### 2.3 Production Code: `ESP32_Master_Center` (`master-node.ino`)

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <esp_now.h>
#include <ArduinoOTA.h>
#include "RMaker.h"
#include "WiFiProv.h"
#include "RMakerQR.h"

// ==========================================
// 1. PIN ASSIGNMENTS & HARDWARE LOGIC
// ==========================================
#define SIREN_RELAY_PIN    18  // Industrial Siren Relay (Active-HIGH)
#define PROV_BUTTON_PIN    0   // BOOT button: Hold 5s for Factory Reset & Unclaim

// ==========================================
// 2. NETWORK & HA BROKER CREDENTIALS
// ==========================================
const char* MQTT_SERVER   = "192.168.0.40";
const int   MQTT_PORT     = 1883;
const char* MQTT_USER     = "redwansmqtt";
const char* MQTT_PASS     = "abcd2005-";

WiFiClient espClient;
PubSubClient mqttClient(espClient);

// ==========================================
// 3. RAINMAKER & ESP-NOW STRUCTURES
// ==========================================
const char *service_name = "CENTER_NODE";
const char *pop          = "abcd2005-"; // Proof-of-Possession PIN for BLE security

static uint8_t siren_pin      = SIREN_RELAY_PIN;
static uint8_t bath_dummy_pin = 0; // Virtual pin for Bathroom Light App Switch
static uint8_t auto_dummy_pin = 0; // Virtual pin for Radar Auto Mode Switch

static Switch *mySirenSwitch     = NULL;
static Switch *myBathroomSwitch  = NULL;
static Switch *myRadarAutoSwitch = NULL;
static Param  *alarmStatusParam  = NULL;

bool emergencyAlarmActive = false;

// Broadcast address to transmit control overrides to REDWAN-BATH-NODE over ESP-NOW
uint8_t broadcastAddress[] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF };

typedef struct struct_message {
  char nodeID[20];
  bool lightActive;
  uint8_t mode;
} struct_message;
struct_message incomingBathroomData;

typedef struct cmd_message {
  uint8_t targetMode; // 0=Auto, 1=ForceON, 2=ForceOFF
} cmd_message;
cmd_message outgoingCmd;

// ==========================================
// 4. OFFICIAL PROVISIONING EVENT HANDLER
// ==========================================
void sysProvEvent(arduino_event_t *sys_event) {
  switch (sys_event->event_id) {
    case ARDUINO_EVENT_PROV_START:
      Serial.printf("\n[PROV] BLE Provisioning Started! Name: \"%s\" | PoP: \"%s\"\n", service_name, pop);
      printQR(service_name, pop, "ble");
      break;
    case ARDUINO_EVENT_WIFI_STA_CONNECTED:
      Serial.println("\n[WIFI] Connected to Router!");
      break;
    case ARDUINO_EVENT_PROV_CRED_RECV:
      Serial.println("\n[PROV] Credentials Received from Phone App!");
      break;
    case ARDUINO_EVENT_PROV_CRED_FAIL:
      Serial.println("\n[PROV] Provisioning Credential Verification Failed!");
      break;
    case ARDUINO_EVENT_PROV_END:
      Serial.println("\n[PROV] Provisioning Successful & Closed!");
      break;
    default:
      break;
  }
}

// ==========================================
// 5. ESP RAINMAKER APP CALLBACK
// ==========================================
void write_callback(Device *device, Param *param, const param_val_t val, void *priv_data, write_ctx_t *ctx) {
  const char *device_name = device->getDeviceName();
  const char *param_name  = param->getParamName();

  // 1. Emergency Siren Manual Control
  if (strcmp(device_name, "Emergency Siren") == 0 && strcmp(param_name, "Power") == 0) {
    bool newState = val.val.b;
    emergencyAlarmActive = newState;
    digitalWrite(SIREN_RELAY_PIN, newState ? HIGH : LOW);
    Serial.printf("[RAINMAKER] Siren manually toggled to: %s\n", newState ? "ON" : "OFF");
    param->updateAndReport(val);
    if (!newState && alarmStatusParam) {
      alarmStatusParam->updateAndReport(value("SYSTEM SAFE - ALL CLEAR"));
    }
  }

  // 2. Radar Auto Mode Toggle in RainMaker App
  if (strcmp(device_name, "Radar Auto Mode") == 0 && strcmp(param_name, "Power") == 0) {
    bool autoCommand = val.val.b;
    if (autoCommand) {
      Serial.println("[RAINMAKER] Radar Auto Mode Enabled -> Restoring AUTO(0)");
      outgoingCmd.targetMode = 0;
      esp_now_send(broadcastAddress, (uint8_t *)&outgoingCmd, sizeof(outgoingCmd));

      if (mqttClient.connected()) {
        mqttClient.publish("home/bathroom/light/mode_cmd", "AUTO", true);
      }
    }
    param->updateAndReport(val);
  }

  // 3. Bathroom Light Manual Control via RainMaker App
  if (strcmp(device_name, "Bathroom Light") == 0 && strcmp(param_name, "Power") == 0) {
    bool lightCommand = val.val.b;
    Serial.printf("[RAINMAKER] Bathroom Light override toggled to: %s\n", lightCommand ? "ON" : "OFF");

    outgoingCmd.targetMode = lightCommand ? 1 : 2;
    esp_now_send(broadcastAddress, (uint8_t *)&outgoingCmd, sizeof(outgoingCmd));

    if (myRadarAutoSwitch) {
      myRadarAutoSwitch->updateAndReportParam("Power", false);
    }

    if (mqttClient.connected()) {
      mqttClient.publish("home/bathroom/light/mode_cmd", lightCommand ? "ON" : "OFF", true);
    }
    param->updateAndReport(val);
  }
}

// ==========================================
// 6. ESP-NOW BACKUP RECEIVER CALLBACK
// ==========================================
void onESPNowDataRecv(const esp_now_recv_info* recv_info, const uint8_t* incomingData, int len) {
  memcpy(&incomingBathroomData, incomingData, sizeof(incomingBathroomData));
  Serial.printf("[ESP-NOW BACKUP] From %s -> Light: %s\n",
                incomingBathroomData.nodeID,
                incomingBathroomData.lightActive ? "ON" : "OFF");

  if (mqttClient.connected()) {
    mqttClient.publish("home/bathroom/light/state", incomingBathroomData.lightActive ? "ON" : "OFF", true);
  }

  if (myBathroomSwitch) {
    myBathroomSwitch->updateAndReportParam("Power", incomingBathroomData.lightActive);
  }

  if (myRadarAutoSwitch) {
    bool isAuto = (incomingBathroomData.mode == 0);
    myRadarAutoSwitch->updateAndReportParam("Power", isAuto);
  }
}

// ==========================================
// 7. EMERGENCY SIREN TRIGGER
// ==========================================
void triggerEmergencySiren(const char* reason) {
  emergencyAlarmActive = true;
  digitalWrite(SIREN_RELAY_PIN, HIGH);
  Serial.printf("[EMERGENCY ALARM] TRIGGERED BY: %s\n", reason);

  if (mySirenSwitch) mySirenSwitch->updateAndReportParam("Power", true);
  if (alarmStatusParam) alarmStatusParam->updateAndReport(value(reason));

  if (mqttClient.connected()) {
    mqttClient.publish("home/alarms/master_siren", "TRIGGERED", true);
    mqttClient.publish("home/alarms/reason", reason, true);
  }
}

// ==========================================
// 8. SETUP ROUTINE
// ==========================================
void setup() {
  Serial.begin(115200);
  pinMode(SIREN_RELAY_PIN, OUTPUT);
  digitalWrite(SIREN_RELAY_PIN, LOW);
  pinMode(PROV_BUTTON_PIN, INPUT_PULLUP);

  WiFi.mode(WIFI_STA);

  Node my_node = RMaker.initNode("ESP32-Center-Node", "HomeAutomation");

  mySirenSwitch = new Switch("Emergency Siren", &siren_pin);
  mySirenSwitch->addCb(write_callback);
  alarmStatusParam = new Param("Security Status", "esp.param.name", value("SYSTEM SAFE"), PROP_FLAG_READ | PROP_FLAG_WRITE);
  mySirenSwitch->addParam(*alarmStatusParam);
  my_node.addDevice(*mySirenSwitch);

  myBathroomSwitch = new Switch("Bathroom Light", &bath_dummy_pin);
  myBathroomSwitch->addCb(write_callback);
  my_node.addDevice(*myBathroomSwitch);

  myRadarAutoSwitch = new Switch("Radar Auto Mode", &auto_dummy_pin);
  myRadarAutoSwitch->addCb(write_callback);
  my_node.addDevice(*myRadarAutoSwitch);

  RMaker.enableOTA(OTA_USING_TOPICS, "Official_Release");
  RMaker.enableTZService();
  RMaker.enableSchedule();
  RMaker.start();

  WiFi.onEvent(sysProvEvent);
  WiFiProv.beginProvision(NETWORK_PROV_SCHEME_BLE, NETWORK_PROV_SCHEME_HANDLER_FREE_BTDM, NETWORK_PROV_SECURITY_1, pop, service_name);

  if (esp_now_init() == ESP_OK) {
    esp_now_register_recv_cb(onESPNowDataRecv);
    esp_now_peer_info_t peerInfo = {};
    memcpy(peerInfo.peer_addr, broadcastAddress, 6);
    peerInfo.channel = 0;
    peerInfo.encrypt = false;
    esp_now_add_peer(&peerInfo);
  }

  mqttClient.setServer(MQTT_SERVER, MQTT_PORT);

  ArduinoOTA.setHostname("Redwan-Master-Node");
  ArduinoOTA.setPassword("abcd2005-");
  ArduinoOTA.begin();

  Serial.println("[BOOT] Master Center Node System Online!");
}

// ==========================================
// 9. MAIN PRODUCTION LOOP
// ==========================================
void loop() {
  if (digitalRead(PROV_BUTTON_PIN) == LOW) {
    unsigned long pressStart = millis();
    while (digitalRead(PROV_BUTTON_PIN) == LOW) {
      if (millis() - pressStart > 5000) {
        Serial.println("[RESET] Restoring Factory Settings & Unclaiming...");
        RMakerFactoryReset(0);
      }
      delay(50);
    }
  }

  if (WiFi.status() == WL_CONNECTED) {
    ArduinoOTA.handle();

    if (!mqttClient.connected()) {
      static unsigned long lastRetry = 0;
      if (millis() - lastRetry > 5000) {
        lastRetry = millis();
        if (mqttClient.connect("ESP32_Master_Center", MQTT_USER, MQTT_PASS)) {
          Serial.println("[MQTT] Master Node Authenticated with Home Assistant!");
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

## PART 3: A-TO-Z DEPLOYMENT, RAINMAKER PAIRING & ARDUINO UPLOAD FIX PROTOCOL

### 3.1 Solving Arduino IDE `exit status 1` Upload Error

When flashing the Master Node (ESP32 WROOM-32), upload failures can happen due to COM port locks or bootloader timing issues.

#### Checklist
1. **Close all port monitors**  
   Ensure Serial Monitor and Serial Plotter are closed before upload.

2. **Verify partition scheme**  
   Arduino IDE → **Tools > Partition Scheme** → select **Custom** or **Custom (partitions.csv)**.

3. **Manual boot override**  
   When console shows:
   ```text
   Connecting........_____....._____.....
   ```
   Hold **BOOT** for ~2 seconds, release when writing starts.

4. **Lower upload speed (if needed)**  
   Arduino IDE → **Tools > Upload Speed**: change from `921600` to `115200`.

---

### 3.2 ESP RainMaker BLE + Wi-Fi Pairing Procedure

1. **First-time flash wipe**  
   Set **Tools > Erase All Flash Before Sketch Upload = Enabled** and upload once.

2. **Restore safe upload mode**  
   Set **Erase All Flash Before Sketch Upload = Disabled** afterward.

3. **Boot and QR generation**
   - Open Serial Monitor at `115200`
   - Press `EN` reset button
   - Look for:
   ```text
   [PROV] BLE Provisioning Started! Name: "CENTER_NODE" | PoP: "abcd2005-"
   ```

4. **Phone app pairing**
   - Open ESP RainMaker app → tap **+**
   - Scan QR or enter PoP manually: `abcd2005-`
   - Accept BLE pairing
   - Choose Wi-Fi SSID `Syndicate` and enter password
   - After provisioning, controls should appear:
     - **Emergency Siren**
     - **Bathroom Light**
     - **Radar Auto Mode**

---

### 3.3 Final System Verification Cheat Sheet

| Test / Scenario | Expected Hardware / System Behavior |
|---|---|
| 1. Walk into Bathroom (Normal) | LD2410B OUT pin goes HIGH (3.3V); C3 GPIO10 goes HIGH; SSR ON (<10ms); HA dashboard shows ON. |
| 2. RPi / HA Server Powered OFF (Offline Fail-Safe) | ESP-NOW remains active; RainMaker Bathroom Light toggle still controls C3 node; SSR switches locally without HA. |
| 3. Restore Auto Mode in RainMaker | Turn ON “Radar Auto Mode”; C3 immediately evaluates radar occupancy; SSR syncs instantly to occupancy state. |
| 4. Hold BOOT Button for 5s (Factory Reset) | WROOM master erases stored Wi-Fi/BLE NVS, unclaims from RainMaker cloud, generates fresh BLE pairing QR on reboot. |

---

## Safety Note

⚠️ This system includes **high-voltage AC mains** circuitry.  
Only proceed with AC wiring if you are trained and follow local electrical safety codes, proper insulation, fuse protection, and enclosure standards.
