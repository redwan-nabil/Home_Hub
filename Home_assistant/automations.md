# 🚀 Release Notes

### Changes in `automations.yaml`:
1. **New Automation Added:**
   - **System: Log Flights to CSV File (`id: '1778989108269'`)**
     - Logs flight data from `flightradar24_entry` events into a CSV file for record-keeping.
   - **⚙️ SYSTEM: Auto-Clean Surveillance Databases (`id: '1779008184140'`)**
     - Automatically trims airplane and helicopter CSV files daily at 3:00 AM to prevent excessive file size.
   - **⚡🔥🌋 CRITICAL THREAT ALARM (`id: '1779011494115'`)**
     - Sends high-priority notifications for critical threats such as lightning proximity, hazardous air/fire, and earthquakes. Notifications bypass phone silent mode.
   - **📡 SENTRY: Space Weather Radio Interruption Warning (`id: '1779029065143'`)**
     - Alerts when the planetary Kp-Index exceeds 6, indicating potential disruptions to satellite, GPS, and HF communication.
   - **🛰️ SENTRY: ISS Overhead Alert (`id: '1779192276256'`)**
     - Notifies when the International Space Station (ISS) is overhead and visible from Dhaka.
   - **🚁 SYSTEM: Log Helicopter to CSV Archive (`id: '1779279092548'`)**
     - Logs new helicopter arrivals to the local system log for tracking and analysis.

2. **Enhancements to Existing Automations:**
   - No changes were made to the existing automations.

---

# Home Assistant Automations

This document provides an overview of the automations configured in the `automations.yaml` file for the Home Assistant instance. These automations are designed to enhance home automation, security, and monitoring capabilities.

---

## Table of Contents
1. [Automations Overview](#automations-overview)
2. [Automation Details](#automation-details)
   - [IUT Home](#iut-home)
   - [Home Assistant Update](#home-assistant-update)
   - [Critical Airspace Alert: Heli & Military (5km)](#critical-airspace-alert-heli--military-5km)
   - [System: Log Flights to CSV File](#system-log-flights-to-csv-file)
   - [⚙️ SYSTEM: Auto-Clean Surveillance Databases](#️-system-auto-clean-surveillance-databases)
   - [⚡🔥🌋 CRITICAL THREAT ALARM](#️-critical-threat-alarm)
   - [📡 SENTRY: Space Weather Radio Interruption Warning](#-sentry-space-weather-radio-interruption-warning)
   - [🛰️ SENTRY: ISS Overhead Alert](#️-sentry-iss-overhead-alert)
   - [🚁 SYSTEM: Log Helicopter to CSV Archive](#-system-log-helicopter-to-csv-archive)

---

## Automations Overview

This configuration includes automations for:
- Geofencing notifications.
- Home Assistant update alerts.
- Airspace monitoring for helicopters and military aircraft.
- Logging flight and helicopter data to CSV files.
- Automated cleanup of surveillance logs.
- High-priority alerts for critical environmental threats.
- Space weather warnings for radio and satellite disruptions.
- Notifications for International Space Station (ISS) visibility.

---

## Automation Details

### IUT Home
- **ID:** `1776752047278`
- **Description:** Sends a notification when the person `redwan_s_home` leaves the `zone.iut_home`.
- **Trigger:** Leaving the `zone.iut_home`.
- **Action:** Sends a notification to the device with ID `439bbeccddde0413130e97a847e10794`.

---

### Home Assistant Update
- **ID:** `1776778529372`
- **Description:** Notifies when a new Home Assistant update is available.
- **Trigger:** State change of `sensor.home_assistant_version_current_version` to `on`.
- **Action:** Sends a notification to `mobile_app_redwan_s_s23` with an update alert.

---

### Critical Airspace Alert: Heli & Military (5km)
- **ID:** `1778964460052`
- **Description:** Sends an alert when a helicopter or military aircraft is detected within 5km.
- **Trigger:** `flightradar24_entry` event with a distance of 5km or less.
- **Conditions:**
  - Aircraft model contains keywords like "helicopter," "bell," "robinson," or "aw1."
  - Airline contains keywords like "air force," "military," "army," or "navy."
- **Action:** Sends a high-priority notification to `mobile_app_redwan_s_s23` with details about the aircraft.

---

### System: Log Flights to CSV File
- **ID:** `1778989108269`
- **Description:** Logs flight data from `flightradar24_entry` events into a CSV file.
- **Trigger:** `flightradar24_entry` event.
- **Action:** Executes `shell_command.export_flight` to log flight data, including:
  - Timestamp
  - Callsign
  - Aircraft model
  - Airline short name
  - Origin and destination cities
  - Closest distance

---

### ⚙️ SYSTEM: Auto-Clean Surveillance Databases
- **ID:** `1779008184140`
- **Description:** Automatically trims airplane and helicopter CSV files daily to prevent excessive file size.
- **Trigger:** Time-based trigger at 03:00:00.
- **Actions:**
  - Executes `shell_command.cleanup_flight_log`.
  - Executes `shell_command.cleanup_helicopter_log`.

---

### ⚡🔥🌋 CRITICAL THREAT ALARM
- **ID:** `1779011494115`
- **Description:** Sends high-priority notifications for critical environmental threats, bypassing phone silent mode.
- **Triggers:**
  - Lightning detected within 5km (`sensor.redwan_s_home_lightning_distance`).
  - PM2.5 levels above 200 at US Consulate (`sensor.dhaka_us_consulate_bangladesh_pm2_5`).
  - Earthquake detected in Dhaka region (`usgs_earthquakes_feed`).
- **Actions:**
  - Sends high-priority notifications to `mobile_app_redwan_s_s23` and `mobile_app_ahlia_s_redmi_note_8` with specific messages for each threat type.

---

### 📡 SENTRY: Space Weather Radio Interruption Warning
- **ID:** `1779029065143`
- **Description:** Alerts when the planetary Kp-Index exceeds 6, indicating potential disruptions to satellite, GPS, and HF communication.
- **Trigger:** `sensor.planetary_k_index` exceeds 6.
- **Action:** Sends a high-priority notification to `mobile_app_redwan_s_s23` with details about the solar storm.

---

### 🛰️ SENTRY: ISS Overhead Alert
- **ID:** `1779192276256`
- **Description:** Notifies when the International Space Station (ISS) is overhead and visible from Dhaka.
- **Trigger:** State change of `binary_sensor.iss` from `off` to `on`.
- **Action:** Sends a high-priority notification to `mobile_app_redwan_s_s23` with details about the ISS and the number of humans currently in orbit.

---

### 🚁 SYSTEM: Log Helicopter to CSV Archive
- **ID:** `1779279092548`
- **Description:** Logs new helicopter arrivals to the local system log.
- **Trigger:** State change of `sensor.helicopter_surveillance_log_10km`.
- **Condition:** Ensures that the new helicopter is not already logged.
- **Action:** Writes helicopter data to the system log, including:
  - Timestamp
  - Callsign
  - Aircraft model
  - Airline short name
  - Origin and destination cities
  - Distance
  - Altitude
  - Ground speed

---

## Notes
- Ensure that all `shell_command` scripts referenced in the automations are properly configured in the `configuration.yaml` file.
- Test each automation after deployment to verify proper functionality.
- For critical alerts, ensure that mobile devices have notifications enabled for the Home Assistant app and that the app is configured to handle high-priority notifications.