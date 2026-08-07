# ESP32 Master Center Node: A-to-Z Engineering Reference & Cheat Sheet

---

## 1. System Architecture & Capabilities

This Master Center Node is a **fault-tolerant, multi-protocol IoT hub** built on the ESP32 WROOM platform. It bridges four independent network layers to ensure whole-home automation never fails, even during ISP outages, Wi-Fi router crashes, or AWS server downtime.

```text
                   +---------------------------------------------------+
                   |         ESP32 MASTER CENTER NODE (WROOM)          |
                   +-------------------------+-------------------------+
                                             |
     +-------------------+-------------------+-------------------+-------------------+
     |                   |                   |                   |                   |
     v                   v                   v                   v                   v
+----------+       +-----------+       +-----------+       +-----------+       +-----------+
| ESP-NOW  |       | RAINMAKER |       | HA MQTT   |       | EMERGENCY |       | HARDWARE  |
|  RADIO   |       | AWS CLOUD |       | LOCAL LAN |       |  SOFTAP   |       |  RELAYS   |
+----------+       +-----------+       +-----------+       +-----------+       +-----------+
| 2.4 GHz  |       | _esp_rmaker|      | Mosquitto |       | 192.168.4.1|      | GPIO 18   |
| 11 Slaves|       | 4 Cards   |       | QoS 1     |       | Captive   |       | Siren     |
+----------+       +-----------+       +-----------+       +-----------+       +-----------+
```

### Key Operational Modes

#### Normal Mode (Router & Internet Online)
- Synchronizes with Espressif RainMaker (AWS Cloud) for mobile app control.
- Maintains an authenticated MQTT connection to Home Assistant (`192.168.0.40:1883`) with `retain: true` state publishing.
- Transmits and receives real-time ESP-NOW RF packets to/from auxiliary C3 slave nodes.

#### Emergency Mode (Router Offline / Manual Override)
- The **60-second Auto-Supervisor** detects router loss and activates an emergency Wi-Fi Access Point (`ESP32-EMERGENCY-HUB`).
- A **Captive Portal DNS Server** intercepts client DNS requests and automatically pops up an interactive, dark-themed **Obsidian Web Dashboard** at [http://192.168.4.1](http://192.168.4.1).
- The embedded web dashboard uses **AJAX background polling (`1500ms`)** to highlight live hardware states without page reloads.

---

## 2. Hardware Pinout & Memory Mapping

| Pin / Resource | Assignment / Value | Electrical Description | Functional Purpose |
|---|---|---|---|
| **GPIO 18** | `SIREN_RELAY_PIN` | Active-HIGH Digital Output | Triggers the industrial security alarm siren relay. |
| **GPIO 0** | `PROV_BUTTON_PIN` | Active-LOW Input (Pull-Up) | BOOT button. **Hold for 5 seconds** to Factory Reset & Unclaim from AWS. |
| **Virtual 253** | `bath_dummy_pin` | Memory Pointer Only | Isolates `REDWAN-BATH-NODE` light override from physical GPIO pull-up traps. |
| **Virtual 254** | `auto_dummy_pin` | Memory Pointer Only | Isolates `Bath Radar Auto` switch card from physical GPIO 0 pull-up traps. |
| **Virtual 255** | `ap_dummy_pin` | Memory Pointer Only | Isolates `Master Hub Controls` SoftAP switch from physical GPIO pull-up traps. |

---

## 3. Communication Protocol Reference

### A) ESP-NOW RF Packet Structures (`broadcastAddress: FF:FF:FF:FF:FF:FF`)

#### Incoming Telemetry (`struct_message`)
- `char nodeID[20]`: Originating slave identifier (e.g., `"REDWAN-BATH-NODE"`).
- `bool lightActive`: Live relay state of the slave (`true` = ON, `false` = OFF).
- `uint8_t mode`: Slave operational mode (`0` = Auto/Radar, `1` = Force ON, `2` = Force OFF).

#### Outgoing Command (`cmd_message`)
- `uint8_t targetMode`: Broadcast instruction sent to slaves (`0` = Auto, `1` = Force ON, `2` = Force OFF).

### B) Home Assistant MQTT Topic Map

| HA Entity Name | MQTT Topic | Direction | Expected Values | Purpose |
|---|---|---|---|---|
| **Siren Relay Switch** | `home/master_node/siren/set` | HA → ESP32 | `"ON"` / `"OFF"` | Commands physical siren relay on GPIO 18. |
| **Siren State Feedback** | `home/master_node/siren/state` | ESP32 → HA | `"ON"` / `"OFF"` | Synchronizes UI switch toggle state in HA. |
| **SoftAP Override Switch** | `home/master_node/ap_mode/set` | HA → ESP32 | `"ON"` / `"OFF"` | Manually triggers Captive Portal SoftAP. |
| **SoftAP State Feedback** | `home/master_node/ap_mode/state` | ESP32 → HA | `"ON"` / `"OFF"` | Synchronizes SoftAP override switch in HA. |
| **Alarm Safety Binary** | `home/alarms/master_siren` | ESP32 → HA | `"TRIGGERED"` / `"SAFE"` | Safety binary sensor for alarm automations. |
| **Siren Reason Text** | `home/alarms/reason` | ESP32 → HA | Text String | Diagnostic sensor showing trigger origin. |
| **AP Network Status** | `home/master_node/ap_mode/status` | ESP32 → HA | Text String | Displays live IP or standby status string. |

---

## 4. Home Assistant Configuration (`configuration.yaml`)

Add this configuration block under your root `mqtt:` key. Every entity is bound to the **`REDWAN-MASTER-NODE`** device registry entry:

```yaml
mqtt:
  switch:
    # --- DEVICE 1: EMERGENCY SIREN CONTROL SWITCH ---
    - name: "Master Emergency Siren Control"
      unique_id: "redwans_master_node_siren_switch_01"
      command_topic: "home/master_node/siren/set"
      state_topic: "home/master_node/siren/state"
      payload_on: "ON"
      payload_off: "OFF"
      icon: "mdi:alarm-light"
      qos: 1
      retain: true
      device:
        identifiers: ["redwans_master_node"]
        name: "REDWAN-MASTER-NODE"
        model: "ESP32 WROOM Center Hub"
        manufacturer: "Expressif / Redwan"

    # --- DEVICE 2: EMERGENCY SOFTAP OVERRIDE SWITCH ---
    - name: "Master Emergency AP Mode Override"
      unique_id: "redwans_master_node_ap_switch_01"
      command_topic: "home/master_node/ap_mode/set"
      state_topic: "home/master_node/ap_mode/state"
      payload_on: "ON"
      payload_off: "OFF"
      icon: "mdi:wifi-access-point"
      qos: 1
      retain: true
      device:
        identifiers: ["redwans_master_node"]
        name: "REDWAN-MASTER-NODE"
        model: "ESP32 WROOM Center Hub"
        manufacturer: "Expressif / Redwan"

  binary_sensor:
    # --- DEVICE 3: MASTER CENTER NODE (ALARM STATE) ---
    - name: "Master Siren Alarm Active"
      unique_id: "redwans_master_node_alarm_state_01"
      state_topic: "home/alarms/master_siren"
      payload_on: "TRIGGERED"
      payload_off: "SAFE"
      device_class: safety
      qos: 1
      device:
        identifiers: ["redwans_master_node"]
        name: "REDWAN-MASTER-NODE"
        model: "ESP32 WROOM Center Hub"
        manufacturer: "Expressif / Redwan"

    # --- DEVICE 4: EMERGENCY AP BROADCASTING STATE ---
    - name: "Master AP Mode Active"
      unique_id: "redwans_master_node_ap_binary_01"
      state_topic: "home/master_node/ap_mode/state"
      payload_on: "ON"
      payload_off: "OFF"
      device_class: connectivity
      icon: "mdi:access-point-network"
      qos: 1
      device:
        identifiers: ["redwans_master_node"]
        name: "REDWAN-MASTER-NODE"
        model: "ESP32 WROOM Center Hub"
        manufacturer: "Expressif / Redwan"

  sensor:
    # --- DEVICE 5: MASTER CENTER NODE (SIREN REASON) ---
    - name: "Master Center Node Siren Status"
      unique_id: "redwans_master_node_siren_reason_01"
      state_topic: "home/alarms/reason"
      icon: "mdi:alarm-bell"
      qos: 1
      device:
        identifiers: ["redwans_master_node"]
        name: "REDWAN-MASTER-NODE"
        model: "ESP32 WROOM Center Hub"
        manufacturer: "Expressif / Redwan"

    # --- DEVICE 6: EMERGENCY AP IP & NETWORK STATUS ---
    - name: "Master AP Network Status"
      unique_id: "redwans_master_node_ap_status_01"
      state_topic: "home/master_node/ap_mode/status"
      icon: "mdi:ip-network"
      qos: 1
      device:
        identifiers: ["redwans_master_node"]
        name: "REDWAN-MASTER-NODE"
        model: "ESP32 WROOM Center Hub"
        manufacturer: "Expressif / Redwan"
```

---

## 5. Complete Production Firmware (`master-node.ino`)

```cpp
// (Your original full firmware code goes here exactly as provided)
// Tip: Keep it in /firmware/master-node.ino and link it from this README for readability.
```

> ✅ You already provided the full firmware.  
> For best project hygiene, store that large code block in a separate file and keep README concise.

---

## 6. How to Save This as a Clean Reference PDF

To export this Markdown document into a clean PDF document:

1. **In VS Code / Cursor / Markdown Editors:**  
   Open the Markdown Preview tab (`Ctrl + Shift + V`) → Right-click inside the preview → Select **Print...** → Choose **Save as PDF**.

2. **In Chrome / Edge Browser:**  
   Press **`Ctrl + P`** → Set **Destination** to **Save as PDF** → Uncheck *Headers and footers* → Set **Margins** to *Default* → Click **Save**.