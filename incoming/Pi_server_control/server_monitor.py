# -*- coding: utf-8 -*-
import time
import math
import datetime
import subprocess
import threading
import serial
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    import psutil
except ImportError:
    pass

try:
    import bangla
    BANGLA_AVAILABLE = True
except ImportError:
    BANGLA_AVAILABLE = False

time.sleep(5) 

import board
import busio
import digitalio
from adafruit_bme280.basic import Adafruit_BME280_SPI
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from mpu6050 import mpu6050

# ==========================================
# SYSTEM & API CONFIGURATION
# ==========================================
HA_URL = "http://192.168.0.40:8123"
HA_TOKEN = "REDACTED_BY_SYSADMIN"
HA_FEELS_LIKE = "sensor.openweathermap_apparent_temperature"

TELEGRAM_BOT_TOKEN = "REDACTED_BY_SYSADMIN"
TELEGRAM_CHAT_ID = "REDACTED_BY_SYSADMIN"
EMERGENCY_NUMBERS = ["+8801794684164", "+8801342570575"] 

GMAIL_USER = "nabilredwoan2005@gmail.com"
GMAIL_APP_PASSWORD = "REDACTED_BY_SYSADMIN"
ALERT_RECIPIENTS = ["redwannabil116@gmail.com"] 

# ==========================================
# HARDWARE INITIALIZATION
# ==========================================
sim = serial.Serial('/dev/serial0', 9600, timeout=1)
i2c = busio.I2C(board.SCL, board.SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
font = ImageFont.load_default()
mpu = mpu6050(0x68)

spi = board.SPI()
bme_cs = digitalio.DigitalInOut(board.D25) 
bme280 = Adafruit_BME280_SPI(spi, bme_cs)

bg_data = {
    "ping": "--", "iface": "--", "feels_like": "--",
    "docker": ["Checking...", "", ""], "hijri": "Syncing...",
    "bme_t": "--", "bme_h": "--", "bme_p": "--", 
    "richter": "0.0", "earthquake_armed": False,
    "accel_x": 0.0, "accel_y": 0.0, "accel_z": 0.0,
    "eq_status": "✅ Safe"
}
alarm_active = False

# ==========================================
# ALARM & ALERT SYSTEMS 
# ==========================================
def send_gmail_alert(message):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = ", ".join(ALERT_RECIPIENTS)
        msg['Subject'] = "🚨 CRITICAL SERVER ALERT"
        msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        
        clean_password = "REDACTED_BY_SYSADMIN"
        server.login(GMAIL_USER, clean_password)
        server.send_message(msg)
        server.quit()
    except Exception as e: 
        print(f"[GMAIL ERROR] {e}")

def telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message}, timeout=10)
    except: pass

def trigger_buzzer():
    pass 

def emergency_sos(message):
    for number in EMERGENCY_NUMBERS:
        try:
            sim.write(b'AT+CMGF=1\r\n'); time.sleep(0.5)
            sim.write(f'AT+CMGS="{number}"\r\n'.encode()); time.sleep(0.5)
            sim.write(message.encode() + b'\x1a'); time.sleep(3)
            sim.write(f"ATD{number};\r\n".encode()); time.sleep(20)
            sim.write(b"ATH\r\n"); time.sleep(1)
        except: pass

def reset_alarm_lock():
    global alarm_active
    time.sleep(60) 
    alarm_active = False

def trigger_full_alarm(message):
    global alarm_active
    if not alarm_active:
        alarm_active = True
        threading.Thread(target=reset_alarm_lock, daemon=True).start()
        threading.Thread(target=trigger_buzzer, daemon=True).start()
        threading.Thread(target=telegram_alert, args=(message,), daemon=True).start()
        threading.Thread(target=send_gmail_alert, args=(message,), daemon=True).start()
        threading.Thread(target=emergency_sos, args=(message,), daemon=True).start()

# ==========================================
# HIGH-SPEED SECURITY WATCHDOG (STA/LTA ALGORITHM)
# ==========================================
def security_watchdog_thread():
    time.sleep(15)
    headers = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}
    
    baseline_temp = 25.0
    try:
        readings_t = [bme280.temperature for _ in range(5)]
        baseline_temp = sum(readings_t) / len(readings_t)
    except: pass

    try:
        accel_init = mpu.get_accel_data()
        grav_x, grav_y, grav_z = accel_init['x'], accel_init['y'], accel_init['z']
    except:
        grav_x, grav_y, grav_z = 0.0, 0.0, 9.81
    
    alpha = 0.95 
    
    # STA/LTA Data Windows
    lta_window = []  # 30 seconds of background noise
    sta_window = []  # 1 second of sudden spikes
    
    while True:
        try:
            r = requests.get(f"{HA_URL}/api/states/input_boolean.earthquake_alarm_armed", headers=headers, timeout=2)
            bg_data["earthquake_armed"] = (r.json().get("state") == "on")
            
            # --- FIRE DETECTION ---
            current_temp = bme280.temperature
            if current_temp > 5.0:
                bg_data["bme_t"] = round(current_temp, 1)
                bg_data["bme_p"] = round(bme280.pressure, 1)
                bg_data["bme_h"] = round(bme280.humidity, 1)
                
                if (current_temp - baseline_temp) > 5.0:
                    trigger_full_alarm(f"🔥 CRITICAL: FIRE DETECTED! Spike from {baseline_temp:.1f}C to {current_temp:.1f}C")
                    baseline_temp = current_temp 
        except: pass

        # --- SEISMIC DETECTION (STA/LTA ENGINE) ---
        triggered_in_window = False
        max_richter_window = 0.0
        latest_x, latest_y, latest_z = 0.0, 0.0, 0.0

        for _ in range(20): # 2-second telemetry push block
            try:
                accel = mpu.get_accel_data()
                
                # Digital Gravity Filter
                grav_x = alpha * grav_x + (1.0 - alpha) * accel['x']
                grav_y = alpha * grav_y + (1.0 - alpha) * accel['y']
                grav_z = alpha * grav_z + (1.0 - alpha) * accel['z']

                dyn_x = accel['x'] - grav_x
                dyn_y = accel['y'] - grav_y
                dyn_z = accel['z'] - grav_z
                
                latest_x, latest_y, latest_z = accel['x'], accel['y'], accel['z']
                
                # Calculate physical energy
                dyn_mag = math.sqrt(dyn_x**2 + dyn_y**2 + dyn_z**2)
                energy = dyn_mag ** 2
                
                # Feed the algorithms
                lta_window.append(energy)
                sta_window.append(energy)
                
                if len(lta_window) > 300: lta_window.pop(0) # Keep at 30 seconds
                if len(sta_window) > 10: sta_window.pop(0)  # Keep at 1 second
                
                # Only run logic if we have gathered at least 10 seconds of background noise
                if len(lta_window) >= 100:
                    lta_avg = sum(lta_window) / len(lta_window)
                    sta_avg = sum(sta_window) / len(sta_window)
                    
                    # Guard against division by zero in a perfectly silent room
                    if lta_avg < 0.01: lta_avg = 0.01 
                    
                    ratio = sta_avg / lta_avg
                    
                    # P-WAVE TRIGGER: Sudden energy is 6x background noise AND physical shake is > 0.8m/s2
                    if ratio > 6.0 and dyn_mag > 0.8:
                        triggered_in_window = True
                        pga_gal = dyn_mag * 100
                        richter = round(((math.log10(pga_gal) - 0.014) / 0.3), 1)
                        if richter > max_richter_window: max_richter_window = richter

            except: pass
            time.sleep(0.1) 
            
        # Push telemetry updates outside the rapid loop
        bg_data["accel_x"] = round(latest_x, 2)
        bg_data["accel_y"] = round(latest_y, 2)
        bg_data["accel_z"] = round(latest_z, 2)
        
        if triggered_in_window:
            # Force at least a 4.5+ reading to trigger Home Assistant automations
            bg_data["richter"] = max_richter_window if max_richter_window >= 4.5 else 4.6 
            bg_data["eq_status"] = "🚨 DETECTED!"
            if bg_data["earthquake_armed"]:
                trigger_full_alarm(f"🌍 P-WAVE DETECTED! Mag: {bg_data['richter']}")
        else:
            # LOCK dashboard to absolute ZERO when safe to prevent all HA False Alarms
            bg_data["richter"] = 0.0
            bg_data["eq_status"] = "✅ Safe"

threading.Thread(target=security_watchdog_thread, daemon=True).start()

# ==========================================
# DATE CALCULATION LOGIC
# ==========================================
def get_safe_bangla_date():
    if not BANGLA_AVAILABLE: return "Bangla Lib Missing" 
    try:
        b_dict = bangla.get_date()
        b_nums = {"০":"0", "১":"1", "২":"2", "৩":"3", "৪":"4", "৫":"5", "৬":"6", "৭":"7", "৮":"8", "৯":"9"}
        b_months = {
            "বৈশাখ":"Boishakh", "জ্যৈষ্ঠ":"Joishtho", "আষাঢ়":"Ashar", "শ্রাবণ":"Shrabon", 
            "ভাদ্র":"Bhadro", "আশ্বিন":"Ashwin", "কার্তিক":"Kartik", "অগ্রহায়ণ":"Agrahayon", 
            "পৌষ":"Poush", "মাঘ":"Magh", "ফাল্গুন":"Falgun", "চৈত্র":"Choitro"
        }
        
        raw_day = str(b_dict.get('date', ''))
        raw_year = str(b_dict.get('year', ''))
        raw_month = str(b_dict.get('month', ''))
        
        day = "".join([b_nums.get(c, c) for c in raw_day])
        year = "".join([b_nums.get(c, c) for c in raw_year])
        
        month_eng = "Unknown"
        for k, v in b_months.items():
            if k in raw_month:
                month_eng = v
                break
                
        if month_eng != "Unknown":
            return f"{day} {month_eng} {year}"
        else:
            return f"{day} {raw_month} {year}" 
    except Exception as e: 
        return "Date Syncing..."

def sanitize_hijri_month(raw_month):
    if "Rabi" in raw_month and "Awwal" in raw_month: return "Rabi I"
    if "Rabi" in raw_month: return "Rabi II"
    if "Jumada" in raw_month and "Ula" in raw_month: return "Jumada I"
    if "Jumada" in raw_month: return "Jumada II"
    if "Qi" in raw_month: return "Zilqad"
    if "Hijjah" in raw_month: return "Zilhajj"
    if "Sha" in raw_month: return "Shaban"
    return "".join(c for c in raw_month if c.isalpha())

# ==========================================
# BACKGROUND DATA THREAD
# ==========================================
def background_tasks():
    headers = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}
    last_hijri_fetch = 0
    
    while True:
        if time.time() - last_hijri_fetch > 3600:
            try:
                now = datetime.datetime.now()
                r = requests.get("http://api.aladhan.com/v1/timingsByCity?city=Dhaka&country=Bangladesh", timeout=5).json()
                m_hour, m_min = map(int, r['data']['timings']['Maghrib'].split(':'))
                
                h_day = r['data']['date']['hijri']['day']
                raw_month = r['data']['date']['hijri']['month']['en']
                h_year = r['data']['date']['hijri']['year']
                
                if now.hour > m_hour or (now.hour == m_hour and now.minute >= m_min):
                    tom_str = (now + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
                    r_tom = requests.get(f"http://api.aladhan.com/v1/gToH?date={tom_str}", timeout=5).json()
                    h_day = r_tom['data']['hijri']['day']
                    raw_month = r_tom['data']['hijri']['month']['en']
                    h_year = r_tom['data']['hijri']['year']
                
                bg_data["hijri"] = f"{h_day} {sanitize_hijri_month(raw_month)} {h_year}"
                last_hijri_fetch = time.time()
            except: pass

        try:
            if bg_data["bme_t"] != "--":
                requests.post(f"{HA_URL}/api/states/sensor.server_room_temperature", headers=headers, json={"state": bg_data["bme_t"], "attributes": {"unit_of_measurement": "°C", "device_class": "temperature", "friendly_name": "Server Room Temp"}}, timeout=2)
                requests.post(f"{HA_URL}/api/states/sensor.server_room_humidity", headers=headers, json={"state": bg_data["bme_h"], "attributes": {"unit_of_measurement": "%", "device_class": "humidity", "friendly_name": "Server Room Humidity"}}, timeout=2)
                requests.post(f"{HA_URL}/api/states/sensor.server_room_pressure", headers=headers, json={"state": bg_data["bme_p"], "attributes": {"unit_of_measurement": "hPa", "device_class": "pressure", "friendly_name": "Server Room Pressure"}}, timeout=2)
            
            requests.post(f"{HA_URL}/api/states/sensor.earthquake_magnitude", headers=headers, json={"state": bg_data["richter"], "attributes": {"unit_of_measurement": "Richter", "device_class": "vibration", "friendly_name": "Seismic Magnitude"}}, timeout=2)
            requests.post(f"{HA_URL}/api/states/sensor.mpu6050_x_axis", headers=headers, json={"state": bg_data["accel_x"], "attributes": {"unit_of_measurement": "m/s²", "icon": "mdi:axis-x-arrow", "friendly_name": "X-Axis Acceleration"}}, timeout=2)
            requests.post(f"{HA_URL}/api/states/sensor.mpu6050_y_axis", headers=headers, json={"state": bg_data["accel_y"], "attributes": {"unit_of_measurement": "m/s²", "icon": "mdi:axis-y-arrow", "friendly_name": "Y-Axis Acceleration"}}, timeout=2)
            requests.post(f"{HA_URL}/api/states/sensor.mpu6050_z_axis", headers=headers, json={"state": bg_data["accel_z"], "attributes": {"unit_of_measurement": "m/s²", "icon": "mdi:axis-z-arrow", "friendly_name": "Z-Axis Acceleration"}}, timeout=2)
            requests.post(f"{HA_URL}/api/states/sensor.earthquake_status", headers=headers, json={"state": bg_data["eq_status"], "attributes": {"icon": "mdi:pulse", "friendly_name": "Seismic Status"}}, timeout=2)
        except: pass

        try:
            r = requests.get(f"{HA_URL}/api/states/{HA_FEELS_LIKE}", headers=headers, timeout=3)
            if r.status_code == 200: bg_data["feels_like"] = int(float(r.json().get('state', 0))) 
        except: pass

        try:
            iface_raw = subprocess.check_output("ip route | awk '/default/ {print $5}' | head -n 1", shell=True).decode().strip()
            if iface_raw.startswith("w"):
                try: bg_data["iface"] = f"WiFi: {subprocess.check_output('iwgetid -r', shell=True).decode().strip()}"
                except: bg_data["iface"] = "WiFi Connected"
            elif iface_raw.startswith("e"): bg_data["iface"] = "ETH Connected"
            else: bg_data["iface"] = f"NET: {iface_raw}"
            ping_raw = subprocess.check_output("ping -c 1 -W 1 8.8.8.8 | grep time=", shell=True).decode().strip()
            bg_data["ping"] = ping_raw.split("time=")[1].split(" ")[0] + "ms"
        except:
            bg_data["ping"], bg_data["iface"] = "Offline", "No Internet"

        try:
            containers = subprocess.check_output("docker ps --format '{{.Names}}'", shell=True).decode().lower()
            missing = [t for t in ["homeassistant", "nextcloud", "mosquitto", "cloudflare"] if t not in containers]
            if not missing: bg_data["docker"] = ["All Containers", "Running Well", ""]
            else: bg_data["docker"] = ["Alert! Down:", ", ".join(missing)[:20], ""]
        except: bg_data["docker"] = ["Docker Daemon", "Offline", ""]

        time.sleep(5)

threading.Thread(target=background_tasks, daemon=True).start()

# ==========================================
# OLED DISPLAY ENGINE
# ==========================================
def draw_centered(draw_obj, y_pos, text, font):
    try: w = draw_obj.textlength(text, font=font)
    except AttributeError: w, _ = draw_obj.textsize(text, font=font)
    draw_obj.text((max(0, (128 - w) // 2), y_pos), text, font=font, fill=255)

def format_speed(bps):
    return f"{bps/(1024*1024):.1f}M/s" if bps > 1024*1024 else f"{bps/1024:.1f}K/s"

try:
    last_net, last_disk = psutil.net_io_counters(), psutil.disk_io_counters()
    psutil.cpu_percent()
except:
    pass

last_time = time.time()
page = 0
last_turn = time.time()

while True:
    now = datetime.datetime.now()
    
    if (now.hour == 0 and now.minute >= 30) or (1 <= now.hour < 5):
        disp.fill(0); disp.show(); time.sleep(60); continue

    curr_time = time.time()
    dt = curr_time - last_time
    
    try:
        curr_net, curr_disk = psutil.net_io_counters(), psutil.disk_io_counters()
        net_up, net_down = (curr_net.bytes_sent - last_net.bytes_sent) / dt, (curr_net.bytes_recv - last_net.bytes_recv) / dt
        disk_write, disk_read = (curr_disk.write_bytes - last_disk.write_bytes) / dt, (curr_disk.read_bytes - last_disk.read_bytes) / dt
        last_net, last_disk = curr_net, curr_disk
        cpu_perc = f"CPU: {psutil.cpu_percent():.1f}%"
    except:
        net_up, net_down, disk_write, disk_read = 0, 0, 0, 0
        cpu_perc = "CPU: --%"

    last_time = curr_time

    img = Image.new("1", (128, 64))
    d = ImageDraw.Draw(img)
    
    time_str = now.strftime("%-I:%M:%S %p")
    date_str = now.strftime("%d %b %y")
    d.text((0, 0), time_str, font=font, fill=255)
    try: date_w = d.textlength(date_str, font=font)
    except AttributeError: date_w, _ = d.textsize(date_str, font=font)
    d.text((128 - date_w, 0), date_str, font=font, fill=255)
    d.line((0, 12, 128, 12), fill=255)
    
    if time.time() - last_turn > 15: 
        page = (page + 1) % 5
        last_turn = time.time()
        
    lines = ["", "", ""]
    if page == 0:
        try: ram = subprocess.check_output("free -m | awk 'NR==2{printf \"RAM: %s/%sMB\", $3,$2}'", shell=True).decode().strip()
        except: ram = "RAM: --"
        try: temp = f"Pi Temp: {subprocess.check_output('vcgencmd measure_temp | cut -d \"=\" -f 2', shell=True).decode().strip()}"
        except: temp = "Pi Temp: --"
        lines = [cpu_perc, ram, temp]
    elif page == 1:
        try: disk_usage = subprocess.check_output("df -h / | awk '$NF==\"/\"{printf \"OS: %d/%dGB\", $3,$2}'", shell=True).decode().strip()
        except: disk_usage = "OS: --"
        lines = [disk_usage, f"Read:  {format_speed(disk_read)}", f"Write: {format_speed(disk_write)}"]
    elif page == 2:
        if bg_data["iface"] == "No Internet Connection": lines = ["No Internet", "Connection", "Offline"]
        else: lines = [bg_data["iface"], f"D:{format_speed(net_down)} | U:{format_speed(net_up)}", f"Ping: {bg_data['ping']}"]
    
    elif page == 3:
        try: richter_float = float(bg_data.get("richter", 0.0))
        except: richter_float = 0.0
        
        if richter_float > 2.0:
            lines = [
                "⚠️ SEISMIC ALERT ⚠️",
                f"Mag: {bg_data['richter']} Richter",
                f"Status: {bg_data['eq_status']}"
            ]
        else:
            lines = [
                f"Room Temp: {bg_data.get('bme_t','--')} C", 
                f"Hum: {bg_data.get('bme_h','--')}% | FL: {bg_data['feels_like']}C", 
                f"Room Pres: {bg_data.get('bme_p','--')} hPa"
            ]
            
    elif page == 4:
        lines = bg_data["docker"]

    for i in range(3): 
        if i < len(lines): d.text((0, 15 + (i*11)), lines[i], font=font, fill=255)
        
    d.line((0, 49, 128, 49), fill=255)
    if int(time.time() / 15) % 2 == 0: footer_text = bg_data["hijri"]
    else: footer_text = get_safe_bangla_date()

    draw_centered(d, 52, footer_text, font)
    disp.image(img)
    disp.show()
    time.sleep(1)
