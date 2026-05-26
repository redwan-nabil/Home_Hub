# Home Assistant Automations

This document provides a detailed explanation of the automations defined in the `automations.yaml` file for Home Assistant. Each automation is designed to enhance the functionality of the Home Assistant setup by providing notifications, logging events, and automating system maintenance tasks.

---

## Table of Contents

1. [IUT Home Notification](#iut-home-notification)
2. [Home Assistant Update Notification](#home-assistant-update-notification)
3. [Critical Airspace Alert: Helicopters & Military Aircraft](#critical-airspace-alert-helicopters--military-aircraft)
4. [System: Log Flights to CSV File](#system-log-flights-to-csv-file)
5. [System: Auto-Clean Surveillance Databases](#system-auto-clean-surveillance-databases)
6. [Critical Threat Alarm](#critical-threat-alarm)
7. [Space Weather Radio Interruption Warning](#space-weather-radio-interruption-warning)
8. [ISS Overhead Alert](#iss-overhead-alert)
9. [System: Log Helicopter to CSV Archive](#system-log-helicopter-to-csv-archive)

---

## IUT Home Notification

**ID:** `1776752047278`  
**Alias:** IUT home  
**Description:** Sends a notification when a specific person (`person.redwan_s_home`) leaves the `zone.iut_home`.

### Configuration
- **Blueprint:** `homeassistant/notify_leaving_zone.yaml`
- **Inputs:**
  - `person_entity`: `person.redwan_s_home`
  - `zone_entity`: `zone.iut_home`
  - `notify_device`: `439bbeccddde0413130e97a847e10794`

---

## Home Assistant Update Notification

**ID:** `1776778529372`  
**Alias:** Home assistant update  
**Description:** Notifies the user when a new Home Assistant update is available.

### Triggers
- **Trigger Type:** State change
- **Entity:** `sensor.home_assistant_version_current_version`
- **To State:** `on`

### Actions
- **Notification:**
  - **Device:** `mobile_app_redwan_s_s23`
  - **Title:** `Home assistant Update Alert`
  - **Message:** 🚨 A new Home Assistant update is available! Check the release notes to see if you want to install it.

---

## Critical Airspace Alert: Helicopters & Military Aircraft

**ID:** `1778964460052`  
**Alias:** Critical Airspace Alert: Heli & Military (5km)  
**Description:** Sends an alert when a helicopter or military aircraft is detected within 5 km.

### Triggers
- **Event Type:** `flightradar24_entry`

### Conditions
- **Distance:** `<= 5.0 km`
- **Aircraft Type or Airline:**
  - Aircraft model contains `helicopter`, `bell`, `robinson`, or `aw1`
  - Airline contains `air force`, `military`, `army`, or `navy`

### Actions
- **Notification:**
  - **Device:** `mobile_app_redwan_s_s23`
  - **Title:** `🚨 Airspace Intrusion Detected`
  - **Message:** Includes details about the detected aircraft, such as airline, model, distance, altitude, and speed.
  - **Additional Data:**
    - `ttl`: `0`
    - `priority`: `high`
    - `channel`: `alarm_stream`
    - `url`: Link to the aircraft's Flightradar24 page
    - `image`: Aircraft photo

---

## System: Log Flights to CSV File

**ID:** `1778989108269`  
**Alias:** System: Log Flights to CSV File  
**Description:** Logs flight data to a CSV file whenever a new flight is detected.

### Triggers
- **Event Type:** `flightradar24_entry`

### Actions
- **Shell Command:** `shell_command.export_flight`
- **Data Logged:**
  - Timestamp
  - Callsign
  - Aircraft model
  - Airline short name
  - Origin city
  - Destination city
  - Closest distance

---

## System: Auto-Clean Surveillance Databases

**ID:** `1779008184140`  
**Alias:** ⚙️ SYSTEM: Auto-Clean Surveillance Databases  
**Description:** Automatically trims the airplane and helicopter CSV files daily at 3:00 AM to prevent them from growing too large.

### Triggers
- **Trigger Type:** Time
- **Time:** `03:00:00`

### Actions
- **Shell Commands:**
  - `shell_command.cleanup_flight_log`
  - `shell_command.cleanup_helicopter_log`

---

## Critical Threat Alarm

**ID:** `1779011494115`  
**Alias:** ⚡🔥🌋 CRITICAL THREAT ALARM  
**Description:** Sends high-priority notifications for critical threats such as lightning, hazardous air quality, or earthquakes. Notifications bypass phone silent mode.

### Triggers
1. **Lightning Proximity:**  
   - **Entity:** `sensor.redwan_s_home_lightning_distance`
   - **Condition:** Distance below 5 km
2. **Hazardous Air Quality:**  
   - **Entity:** `sensor.dhaka_us_consulate_bangladesh_pm2_5`
   - **Condition:** PM2.5 above 200
3. **Earthquake Detection:**  
   - **Source:** `usgs_earthquakes_feed`
   - **Zone:** `zone.dhaka_city`
   - **Event:** `enter`

### Actions
- **Lightning Alert:**
  - **Devices:** `mobile_app_redwan_s_s23`, `mobile_app_ahlia_s_redmi_note_8`
  - **Title:** ⚡ DANGER: LIGHTNING PROXIMITY
  - **Message:** Lightning detected within 5 km! Protect servers from power surge.
- **Fire Alert:**
  - **Devices:** `mobile_app_redwan_s_s23`, `mobile_app_ahlia_s_redmi_note_8`
  - **Title:** 🔥 DANGER: HAZARDOUS AIR/FIRE
  - **Message:** Massive PM2.5 spike detected at US Consulate. Possible urban fire nearby.
- **Earthquake Alert:**
  - **Devices:** `mobile_app_redwan_s_s23`, `mobile_app_ahlia_s_redmi_note_8`
  - **Title:** 🌋 CRITICAL: EARTHQUAKE DETECTED
  - **Message:** A seismic event has just struck the Dhaka region! Take cover immediately!
  - **Additional Data:**
    - `vibrationPattern`: `100, 1000, 100, 1000, 100, 1000`

---

## Space Weather Radio Interruption Warning

**ID:** `1779029065143`  
**Alias:** 📡 SENTRY: Space Weather Radio Interruption Warning  
**Description:** Sends a notification when the Planetary Kp-Index exceeds level 6, indicating a solar storm.

### Triggers
- **Entity:** `sensor.planetary_k_index`
- **Condition:** Value above 6

### Actions
- **Notification:**
  - **Device:** `mobile_app_redwan_s_s23`
  - **Title:** ☀️ CRITICAL: SOLAR STORM DETECTED
  - **Message:** Kp-Index has breached level 6. Potential degradation to satellite, GPS, and HF communication infrastructure.
  - **Additional Data:**
    - `priority`: `high`
    - `channel`: `alarm_stream`

---

## ISS Overhead Alert

**ID:** `1779192276256`  
**Alias:** 🛰️ SENTRY: ISS Overhead Alert  
**Description:** Notifies the user when the International Space Station (ISS) is visible over Dhaka.

### Triggers
- **Trigger Type:** State change
- **Entity:** `binary_sensor.iss`
- **From State:** `off`
- **To State:** `on`

### Actions
- **Notification:**
  - **Device:** `mobile_app_redwan_s_s23`
  - **Title:** 🛰️ ISS OVERHEAD NOW!
  - **Message:** The International Space Station is currently passing over Dhaka! Go outside and look up.  
    Includes the number of humans currently in orbit.
  - **Additional Data:**
    - `ttl`: `0`
    - `priority`: `high`
    - `importance`: `high`
    - `channel`: `iss_tracker`
    - `vibrationPattern`: `0, 400, 200, 400, 1000, 400, 200, 400`

---

## System: Log Helicopter to CSV Archive

**ID:** `1779279092548`  
**Alias:** 🚁 SYSTEM: Log Helicopter to CSV Archive  
**Description:** Logs new helicopter arrivals to a local system log.

### Triggers
- **Entity:** `sensor.helicopter_surveillance_log_10km`
- **Condition:** A new helicopter is detected, and it is not already logged.

### Actions
- **System Log:**
  - **Level:** Warning
  - **Message:** Logs details about the helicopter, including timestamp, callsign, aircraft model, airline, origin city, destination city, distance, altitude, and ground speed.

--- 

## Notes
- All automations are configured with specific triggers, conditions, and actions to ensure accurate and timely notifications or actions.
- Notifications are sent to the specified mobile devices using the Home Assistant mobile app.
- Critical alerts are configured to bypass silent mode and use high-priority notification channels.
- CSV logging and database cleanup ensure efficient storage management for flight and helicopter data.