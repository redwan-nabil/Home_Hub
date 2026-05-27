#!/bin/bash

# --- CONFIGURATION ---
MAIN_IF="eth0"               # Main Fiber Ethernet connection
ROUTER_IP="192.168.0.1"      # Main TP-Link Router IP
TEST_IP="8.8.8.8"            # Google DNS to test real internet
USB_HUB="2"                  # Your modem's target USB Hub
USB_PORT="1"                 # Your modem's target USB Port

echo "🚀 Ultimate Power-Saving Watchdog Started..."

# SAFETY STARTUP: Force backup Wi-Fi OFF and kill USB power to save solar battery
sudo systemctl stop hostapd
sudo uhubctl -l $USB_HUB -p $USB_PORT -a off > /dev/null 2>&1
MODEM_IS_ON=false

# Default sleep interval when everything is healthy
# Pinging once every 30 seconds uses a negligible ~51 bits/sec of bandwidth
SLEEP_TIME=30

while true; do
    # Ping Google quickly (timeout after 2 seconds)
    ping -c 1 -W 2 -I $MAIN_IF $TEST_IP > /dev/null 2>&1
    INTERNET_STATUS=$?

    if [ $INTERNET_STATUS -ne 0 ]; then
        # ==========================================
        # 🚨 FIBER IS DEAD - ACTIVATE BACKUP
        # ==========================================
        if [ "$MODEM_IS_ON" = false ]; then
            echo "$(date): Fiber down! Dropping to fast check..."
            
            # Double-check quickly to ensure it wasn't a temporary single packet drop
            sleep 3
            ping -c 1 -W 2 -I $MAIN_IF $TEST_IP > /dev/null 2>&1
            if [ $? -ne 0 ]; then
                echo "$(date): Fiber confirmed dead. Restoring 5V power to USB modem..."
                
                # 1. Physically power ON the USB Port
                sudo uhubctl -l $USB_HUB -p $USB_PORT -a on > /dev/null 2>&1
                MODEM_IS_ON=true
                
                # 2. Wait 45 seconds for the ZTE modem to boot up
                echo "Waiting 45s for cellular network registration..."
                sleep 45
                
                # 3. Fire up the RaspAP Wi-Fi hotspot engine
                sudo systemctl start hostapd
                
                # 4. Drop the dead fiber route so traffic flows through the 4G SIM
                sudo ip route del default via $ROUTER_IP dev $MAIN_IF 2>/dev/null
                echo "⚡ Emergency Network is fully ONLINE."
                
                # While on backup, keep checks slightly faster to catch when fiber returns
                SLEEP_TIME=15
            fi
        fi
    else
        # ==========================================
        # ✅ FIBER IS ALIVE - NORMAL OPERATION
        # ==========================================
        # Set sleep time back to a relaxed 30 seconds since internet is stable
        SLEEP_TIME=30
        
        if [ "$MODEM_IS_ON" = true ]; then
            echo "$(date): Fiber restored! Cleaning up emergency system..."
            
            # 1. Turn off the RaspAP Wi-Fi hotspot to save power
            sudo systemctl stop hostapd
            
            # 2. Restore the TP-Link router as the primary pathway
            sudo ip route add default via $ROUTER_IP dev $MAIN_IF 2>/dev/null
            
            # 3. ABSOLUTE ZERO POWER: Electrically cut 5V power to the modem
            sudo uhubctl -l $USB_HUB -p $USB_PORT -a off > /dev/null 2>&1
            MODEM_IS_ON=false
            echo "🔒 Modem powered completely OFF. System running on Fiber."
        fi
    fi
    
    # Adaptive sleep execution
    sleep $SLEEP_TIME
done
