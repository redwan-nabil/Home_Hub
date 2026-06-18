#ifndef SHARED_PAYLOAD_H
#define SHARED_PAYLOAD_H

#include <Arduino.h>

// ==========================================
// ESP-NOW SHARED DATA STRUCTURE
// ==========================================
// Warning: This struct must be exactly the same on both Sender and Receiver

typedef struct struct_message {
    uint8_t device_id;       // Unique ID for the node (e.g., 2 = Kitchen)
    uint8_t alert_type;      // 0 = Safe, 1 = Warning, 2 = FIRE ALARM
    float temp;              // Temperature in Celsius
    float humidity;          // Humidity percentage
    float pressure;          // Air pressure in hPa
    int gas_ppm;             // Gas concentration in PPM
    float battery_volts;     // Battery voltage (e.g., 3.62)
} struct_message;

#endif