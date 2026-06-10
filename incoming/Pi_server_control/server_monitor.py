# -*- coding: utf-8 -*-
import time
import datetime
import subprocess
import threading
import board
import busio
import adafruit_ssd1306
import adafruit_dht
from PIL import Image, ImageDraw, ImageFont
import psutil
import requests
import bangla

# ==========================================
# HOME ASSISTANT CONFIGURATION
# ==========================================
HA_URL = "http://192.168.0.40:8123"
HA_TOKEN = "REDACTED_BY_SYSADMIN"
HA_FEELS_LIKE = "sensor.openweathermap_apparent_temperature"

# Initialize I2C, Display, and Sensor (GPIO 17)
i2c = busio.I2C(board.SCL, board.SDA)
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
font = ImageFont.load_default()
dht_sensor = adafruit_dht.DHT11(board.D17, use_pulseio=False)

# Background Data Buffer
bg_data = {
    "ping": "--", "iface": "--", "dht_t": "--", "dht_h": "--", "feels_like": "--",
    "docker": ["Checking...", "", ""],
    "hijri": "Syncing..."
}

# ==========================================
# BULLETPROOF BANGLA DATE
# ==========================================
def get_safe_bangla_date():
    try:
        b_dict = bangla.get_date()
        b_nums = {"০":"0", "১":"1", "২":"2", "৩":"3", "৪":"4", "৫":"5", "৬":"6", "৭":"7", "৮":"8", "৯":"9"}
        b_months = {
            "বৈশাখ":"Boishakh", "জ্যৈষ্ঠ":"Joishtho", "আষাঢ়":"Ashar", "আষাঢ়":"Ashar",
            "শ্রাবণ":"Shrabon", "ভাদ্র":"Bhadro", "আশ্বিন":"Ashwin", "কার্তিক":"Kartik", 
            "অগ্রহায়ণ":"Agrahayon", "অগ্রহায়ণ":"Agrahayon", "পৌষ":"Poush", "মাঘ":"Magh", 
            "ফাল্গুন":"Falgun", "চৈত্র":"Choitro"
        }
        
        day_raw = str(b_dict.get('date', ''))
        year_raw = str(b_dict.get('year', ''))
        month_b = str(b_dict.get('month', ''))
        
        day = "".join([b_nums.get(c, c) for c in day_raw])
        year = "".join([b_nums.get(c, c) for c in year_raw])
        
        month_eng = "Unknown"
        for k, v in b_months.items():
            if k in month_b:
                month_eng = v
                break
                
        return f"{day} {month_eng} {year}"
    except:
        return "--"

# ==========================================
# BACKGROUND THREAD (Climate, Network, Hijri API)
# ==========================================
def background_tasks():
    headers = {"Authorization": f"Bearer {HA_TOKEN}", "Content-Type": "application/json"}
    last_hijri_fetch = 0
    
    while True:
        # 1. Internet Hijri Sync
        if time.time() - last_hijri_fetch > 3600:
            try:
                now = datetime.datetime.now()
                r = requests.get("http://api.aladhan.com/v1/timingsByCity?city=Dhaka&country=Bangladesh", timeout=5).json()
                maghrib_str = r['data']['timings']['Maghrib'] 
                m_hour, m_min = map(int, maghrib_str.split(':'))
                
                h_day = r['data']['date']['hijri']['day']
                h_month = r['data']['date']['hijri']['month']['en']
                h_year = r['data']['date']['hijri']['year']
                
                # Roll to tomorrow after Maghrib
                if now.hour > m_hour or (now.hour == m_hour and now.minute >= m_min):
                    tom_str = (now + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
                    r_tom = requests.get(f"http://api.aladhan.com/v1/gToH?date={tom_str}", timeout=5).json()
                    h_day = r_tom['data']['hijri']['day']
                    h_month = r_tom['data']['hijri']['month']['en']
                    h_year = r_tom['data']['hijri']['year']
                
                # FIX: Use shorter month names so they physically fit on the screen
                month_map = {
                    "Rabi' al-Awwal": "Rabi I", 
                    "Rabi' al-Thani": "Rabi II",
                    "Jumada al-Ula": "Jumada I", 
                    "Jumada al-Akhirah": "Jumada II",
                    "Dhu al-Qi'dah": "Zilqad", 
                    "Dhu al-Hijjah": "Zilhajj",
                    "Sha'ban": "Shaban"
                }
                h_month = month_map.get(h_month, h_month.replace("'", "").replace("-", " "))
                    
                bg_data["hijri"] = f"{h_day} {h_month} {h_year}"
                last_hijri_fetch = time.time()
            except:
                if bg_data["hijri"] == "Syncing...": bg_data["hijri"] = "API Offline"

        # 2. DHT11 Read & Auto-Push
        try:
            t = dht_sensor.temperature
            h = dht_sensor.humidity
            if t is not None and h is not None and h > 0 and t > 5:
                bg_data["dht_t"] = int(t) 
                bg_data["dht_h"] = int(h)
                requests.post(f"{HA_URL}/api/states/sensor.server_room_temperature", headers=headers, json={"state": t, "attributes": {"unit_of_measurement": "°C", "device_class": "temperature", "friendly_name": "Server Room Temp"}}, timeout=2)
                requests.post(f"{HA_URL}/api/states/sensor.server_room_humidity", headers=headers, json={"state": h, "attributes": {"unit_of_measurement": "%", "device_class": "humidity", "friendly_name": "Server Room Humidity"}}, timeout=2)
        except: pass

        # 3. Fetch 'Feels Like'
        try:
            r = requests.get(f"{HA_URL}/api/states/{HA_FEELS_LIKE}", headers=headers, timeout=3)
            if r.status_code == 200:
                bg_data["feels_like"] = int(float(r.json().get('state', 0))) 
        except: pass

        # 4. Network Pings
        try:
            iface_raw = subprocess.check_output("ip route | awk '/default/ {print $5}' | head -n 1", shell=True).decode().strip()
            if iface_raw.startswith("w"):
                try:
                    ssid = subprocess.check_output("iwgetid -r", shell=True).decode().strip()
                    bg_data["iface"] = f"WiFi: {ssid}"
                except: bg_data["iface"] = "WiFi Connected"
            elif iface_raw.startswith("e"):
                bg_data["iface"] = "ETH Connected"
            else: bg_data["iface"] = f"NET: {iface_raw}"

            ping_raw = subprocess.check_output("ping -c 1 -W 1 8.8.8.8 | grep time=", shell=True).decode().strip()
            bg_data["ping"] = ping_raw.split("time=")[1].split(" ")[0] + "ms"
        except:
            bg_data["ping"] = "Offline"
            bg_data["iface"] = "No Internet Connection"

        # 5. Docker Health Check
        try:
            containers = subprocess.check_output("docker ps --format '{{.Names}}'", shell=True).decode().lower()
            missing = []
            for target in ["homeassistant", "nextcloud", "mosquitto", "cloudflare", "pihole"]:
                if target not in containers and target.replace("hole", "-hole") not in containers:
                    missing.append(target)

            if not missing: bg_data["docker"] = ["All Containers", "Running Well", ""]
            else: bg_data["docker"] = ["Alert! Down:", ", ".join(missing)[:20], ""]
        except: bg_data["docker"] = ["Docker Daemon", "Offline", ""]

        time.sleep(5)

threading.Thread(target=background_tasks, daemon=True).start()

# ==========================================
# HELPER: DYNAMIC AUTO-CENTER TEXT
# ==========================================
def draw_centered(draw_obj, y_pos, text, font):
    try:
        w = draw_obj.textlength(text, font=font)
    except AttributeError:
        w, _ = draw_obj.textsize(text, font=font)
    x = max(0, (128 - w) // 2)
    draw_obj.text((x, y_pos), text, font=font, fill=255)

# ==========================================
# MAIN DISPLAY LOOP
# ==========================================
def format_speed(bps):
    return f"{bps/(1024*1024):.1f}M/s" if bps > 1024*1024 else f"{bps/1024:.1f}K/s"

last_net, last_disk, last_time = psutil.net_io_counters(), psutil.disk_io_counters(), time.time()
page = 0
last_turn = time.time()

# Prime the CPU tracker
psutil.cpu_percent()

while True:
    now = datetime.datetime.now()
    
    # Midnight to 5:00 AM Blackout
    if (now.hour == 0 and now.minute >= 30) or (1 <= now.hour < 5):
        disp.fill(0); disp.show(); time.sleep(60); continue

    curr_time = time.time()
    dt = curr_time - last_time
    curr_net, curr_disk = psutil.net_io_counters(), psutil.disk_io_counters()
    net_up, net_down = (curr_net.bytes_sent - last_net.bytes_sent) / dt, (curr_net.bytes_recv - last_net.bytes_recv) / dt
    disk_write, disk_read = (curr_disk.write_bytes - last_disk.write_bytes) / dt, (curr_disk.read_bytes - last_disk.read_bytes) / dt
    last_net, last_disk, last_time = curr_net, curr_disk, curr_time

    img = Image.new("1", (128, 64))
    d = ImageDraw.Draw(img)
    
    # ==========================================
    # HEADER: Left Time, Right Date (With 2-Digit Year)
    # ==========================================
    time_str = now.strftime("%-I:%M:%S %p")
    date_str = now.strftime("%d %b %y") # e.g., "10 Jun 26"
    
    # Time pinned to the left
    d.text((0, 0), time_str, font=font, fill=255)
    
    # Date pinned to the right
    try:
        date_w = d.textlength(date_str, font=font)
    except AttributeError:
        date_w, _ = d.textsize(date_str, font=font)
    d.text((128 - date_w, 0), date_str, font=font, fill=255)
    
    # Divider line
    d.line((0, 12, 128, 12), fill=255)
    
    # ==========================================
    # PAGE FLIPPER
    # ==========================================
    if time.time() - last_turn > 15: 
        page = (page + 1) % 5
        last_turn = time.time()
        
    lines = ["", "", ""]
    if page == 0:
        cpu = f"CPU: {psutil.cpu_percent():.1f}%"
        ram = subprocess.check_output("free -m | awk 'NR==2{printf \"RAM: %s/%sMB\", $3,$2}'", shell=True).decode().strip()
        temp = subprocess.check_output("vcgencmd measure_temp | cut -d '=' -f 2", shell=True).decode().strip()
        lines = [cpu, ram, f"Pi Temp: {temp}"]
    elif page == 1:
        disk_usage = subprocess.check_output("df -h / | awk '$NF==\"/\"{printf \"OS: %d/%dGB\", $3,$2}'", shell=True).decode().strip()
        lines = [disk_usage, f"Read:  {format_speed(disk_read)}", f"Write: {format_speed(disk_write)}"]
    elif page == 2:
        if bg_data["iface"] == "No Internet Connection": lines = ["No Internet", "Connection", "Offline"]
        else: lines = [bg_data["iface"], f"D:{format_speed(net_down)} | U:{format_speed(net_up)}", f"Ping: {bg_data['ping']}"]
    elif page == 3:
        lines = [
            f"Server temp: {bg_data['dht_t']} C",
            f"Humidity: {bg_data['dht_h']} %",
            f"Feels like: {bg_data['feels_like']} C"
        ]
    elif page == 4:
        lines = bg_data["docker"]

    # Body lines
    for i in range(3): 
        if i < len(lines):
            d.text((0, 15 + (i*11)), lines[i], font=font, fill=255)
        
    # ==========================================
    # FOOTER: Centered Bangla / Hijri
    # ==========================================
    d.line((0, 49, 128, 49), fill=255)
    cycle = int(time.time() / 15) % 2
    if cycle == 0: 
        footer_text = bg_data["hijri"]
    else: 
        footer_text = get_safe_bangla_date()

    draw_centered(d, 52, footer_text, font)
    
    # Render Frame
    disp.image(img)
    disp.show()
    time.sleep(1)
