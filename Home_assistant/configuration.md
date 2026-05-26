# Home Assistant Configuration

This repository contains the `configuration.yaml` file for a Home Assistant setup. The configuration is designed to provide a robust and feature-rich smart home experience, including automation, monitoring, and integration with various devices and services.

---

## Features

### 1. **Default Integrations**
The `default_config` integration is included to load the default set of Home Assistant integrations. This ensures that basic functionalities such as the frontend, automation, and logging are enabled.

---

### 2. **Frontend Themes**
The `frontend` configuration loads custom themes from the `themes` directory. This allows for customization of the Home Assistant user interface.

```yaml
frontend:
  themes: !include_dir_merge_named themes
```

---

### 3. **Automation, Scripts, and Scenes**
The configuration includes separate YAML files for managing automations, scripts, and scenes. These files are referenced using the `!include` directive.

```yaml
automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
```

---

### 4. **HTTP Configuration**
The `http` section is configured to support reverse proxy setups and includes a list of trusted proxies.

```yaml
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 127.0.0.1
    - "::1"
    - 172.17.0.2
    - 172.17.0.0/16
    - 192.168.0.0/16
    - 10.0.0.0/8
```

---

### 5. **Allowlist for External Directories**
The `homeassistant` section allows access to specific external directories, such as `/config/www`.

```yaml
homeassistant:
  allowlist_external_dirs:
    - /config/www
```

---

### 6. **Shell Commands**
Custom shell commands are defined for various tasks, including backups, restarting services, and managing flight and helicopter logs.

Examples:
- Trigger Home Assistant backup
- Restart Nextcloud and CCTV services
- Export flight data to a CSV file
- Auto-delete old flight and helicopter logs to retain only the latest 1000 entries

```yaml
shell_command:
  run_ha_backup: "ssh -o StrictHostKeyChecking=no -i /config/ssh_keys/id_rsa..."
  restart_nextcloud: "ssh -o StrictHostKeyChecking=no -i /config/ssh_keys/id_rsa..."
  restart_cctv: "ssh -o StrictHostKeyChecking=no -i /config/ssh_keys/id_rsa..."
  export_flight: >
    sh -c "echo '{{ log_data }}' >> /config/www/flight_history.csv"
  cleanup_flight_log: >
    sh -c "tail -n 1000 /config/www/flight_history.csv > /config/www/tmp.csv && mv /config/www/tmp.csv /config/www/flight_history.csv"
  cleanup_helicopter_log: >
    sh -c "tail -n 1000 /config/www/helicopter_history.csv > /config/www/tmp_heli.csv && mv /config/www/tmp_heli.csv /config/www/helicopter_history.csv"
```

---

### 7. **Command Line Sensors**
Command-line sensors are configured to monitor specific system metrics, such as:
- Raspberry Pi fan speed
- NVMe health
- CCTV SSD health

```yaml
command_line:
  - sensor:
      name: "RPi5 Fan Speed"
      command: "ssh -o StrictHostKeyChecking=no -i /config/ssh_keys/id_rsa redwannabil@127.0.0.1 'cat /sys/devices/platform/cooling_fan/hwmon/hwmon*/fan1_input 2>/dev/null || echo 0'"
      unit_of_measurement: "RPM"
      scan_interval: 15
  - sensor:
      name: "Main NVMe Health"
      command: "cat /config/nvme_health.txt"
      unit_of_measurement: "%"
      icon: mdi:harddisk
      scan_interval: 60
  - sensor:
      name: "CCTV SSD Health"
      command: "cat /config/sda_health.txt"
      unit_of_measurement: "%"
      icon: mdi:harddisk
      scan_interval: 60
```

---

### 8. **MQTT Integration**
The MQTT integration is used to monitor room occupancy via a binary sensor.

```yaml
mqtt:
  binary_sensor:
    - name: "CSI Room Occupancy"
      state_topic: "home/room/occupancy"
      payload_on: "ON"
      payload_off: "OFF"
      device_class: occupancy
```

---

### 9. **Recorder Configuration**
The `recorder` integration is configured to optimize database performance by:
- Keeping only 2 days of history
- Committing data every 30 seconds
- Excluding specific domains and entities from being recorded

```yaml
recorder:
  purge_keep_days: 2
  commit_interval: 30
  exclude:
    domains:
      - sun
      - weather
      - camera
      - update
    entities:
      - sensor.time
      - sensor.date
```

---

### 10. **Template Sensors**
Custom template sensors are defined for:
- Logging airspace and helicopter surveillance data
- Islamic prayer times and related calculations (e.g., active prayer time, time until next event, prayer progress percentage)

```yaml
template:
  - trigger:
      - platform: event
        event_type: flightradar24_exit
    sensor:
      - unique_id: local_airspace_surveillance_history
        name: "Airspace Surveillance Log (10km)"
        state: >-
          ...
  - trigger:
      - platform: state
        entity_id: sensor.flightradar24_helicopters_in_area
        attribute: flights
    sensor:
      - name: "Helicopter Surveillance Log 10km"
        unique_id: helicopter_surveillance_log_10km
        icon: mdi:history
        state: "{{ trigger.to_state.state }}"
        attributes:
          flights: >
            ...
  - sensor:
      - name: "Next Sahri Ends"
        icon: mdi:weather-night
        state: "{{ states('sensor.islamic_prayer_times_fajr_prayer') }}"
      - name: "Next Iftar"
        icon: mdi:weather-sunset-down
        state: "{{ states('sensor.islamic_prayer_times_maghrib_prayer') }}"
      - name: "Active Waqt Details"
        state: >
          ...
      - name: "Time Until Next Event Formatted"
        icon: mdi:timer-sand
        state: >
          ...
      - name: "Waqt Progress Percentage"
        unit_of_measurement: "%"
        state: >
          ...
```

---

### 11. **Notification Services**
File-based notification services are configured to log flight and helicopter data to CSV files.

```yaml
notify:
  - name: export_flight_history
    platform: file
    filename: /config/www/flight_history.csv
    timestamp: false
  - name: helicopter_csv_logger
    platform: file
    filename: /config/www/helicopter_history.csv
    timestamp: false
```

---

### 12. **Zones**
A custom zone is defined for a 10km airspace dome, with a specific latitude, longitude, and radius.

```yaml
zone:
  - name: "10km Airspace Dome"
    latitude: 23.6991875
    longitude: 90.4531719
    radius: 10000
    icon: mdi:radar
```

---

### 13. **Geolocation**
The `geo_location` integration is configured to track earthquakes with a magnitude of 4.5 or higher within a 1500km radius.

```yaml
geo_location:
  - platform: usgs_earthquakes_feed
    feed_type: "past_week_m45_earthquakes"
    radius: 1500
    minimum_magnitude: 4.5
    latitude: 23.6991875
    longitude: 90.4531719
```

---

## Prerequisites
- Home Assistant installed and running
- SSH keys configured for remote commands
- Required directories (`/config/www`, `/config/ssh_keys`, etc.) created
- MQTT broker configured and running
- FlightRadar24 integration for flight data
- Islamic prayer times integration for prayer-related sensors

---

## Installation
1. Clone this repository or copy the `configuration.yaml` file into your Home Assistant configuration directory.
2. Ensure all referenced files (e.g., `automations.yaml`, `scripts.yaml`, `scenes.yaml`, etc.) exist in the configuration directory.
3. Place your custom themes in the `themes` folder.
4. Configure your SSH keys and place them in the `/config/ssh_keys` directory.
5. Restart Home Assistant to apply the changes.

---

## Notes
- Ensure the IP addresses in the `trusted_proxies` list match your network setup.
- Update the latitude and longitude values in the `zone` and `geo_location` sections to match your location.
- Modify the `shell_command` and `command_line` commands as needed to fit your environment.

---

## Troubleshooting
- Check the Home Assistant logs for errors after restarting.
- Verify that all external files (e.g., `automations.yaml`, `scripts.yaml`, etc.) are correctly formatted and exist.
- Ensure the MQTT broker is running and accessible.
- Test SSH commands manually to confirm connectivity and permissions.

---

## License
This configuration is provided under the MIT License. Feel free to use and modify it as needed.