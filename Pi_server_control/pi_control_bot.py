import telebot
import psutil
import speedtest
import subprocess
import os
import smtplib
import random
import string
import requests
import time
import threading
from email.message import EmailMessage

# --- 1. CREDENTIALS & CONFIGURATION ---
BOT_TOKEN = "REDACTED_BY_SYSADMIN"
ADMIN_ID = 1435882929

# Email Config
SENDER_EMAIL = "nabilredwoan2005@gmail.com"      
EMAIL_APP_PASSWORD = "REDACTED_BY_SYSADMIN"
RECEIVER_EMAIL = "redwannabil116@gmail.com"    

# Weather & Radar Config
WEATHER_API_KEY = "REDACTED_BY_SYSADMIN"
PHONE_IP = "192.168.0.117"  # My phone's Wi-Fi IP
CITY = "Dhaka,BD"

bot = telebot.TeleBot(BOT_TOKEN)
pending_auth = {} 

print("⚙️ Pi Admin Control Bot with 2FA & Weather Radar is running...")

# --- 2. 2FA EMAIL FUNCTION ---
def send_otp_email(otp, command):
    msg = EmailMessage()
    msg.set_content(f"Security Alert: A '{command}' command was triggered on your Raspberry Pi.\nYour 6-digit authorization code is: {otp}\n\nIf you did not request this, someone is trying to access your bot!")
    msg['Subject'] = f"Security Alert: A '{command}' command was triggered on your Raspberry Pi."
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, EMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# --- 3. SYSTEM SECURE COMMANDS ---
@bot.message_handler(commands=['reboot', 'shutdown', 'clear'])
def request_secure_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⛔ Access Denied.")
        return

    if message.text.startswith('/clear'):
        if message.text.strip().lower() != '/clear cache':
            bot.send_message(message.chat.id, "⚠️ Invalid command. Did you mean '/clear cache'?")
            return
        command = "clear cache"
    else:
        command = message.text.replace('/', '')
    
    otp = ''.join(random.choices(string.digits, k=6))
    bot.send_message(ADMIN_ID, f"🔒 Security lock engaged. Generating one-time password for '{command}'...")
    
    if send_otp_email(otp, command):
        pending_auth[ADMIN_ID] = {'command': command, 'otp': otp}
        bot.send_message(ADMIN_ID, "📧 The code has been sent to your email! Please reply to me with the 6-digit code to confirm, or type 'cancel'.")
    else:
        bot.send_message(ADMIN_ID, "❌ Failed to send email. Check your email credentials.")

@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID and ADMIN_ID in pending_auth)
def verify_otp(message):
    auth_data = pending_auth[ADMIN_ID]
    user_input = message.text.strip()
    command = auth_data['command']

    if user_input.lower() == 'cancel':
        bot.reply_to(message, "✅ Action cancelled. Server remains online.")
        del pending_auth[ADMIN_ID]
        
    elif user_input == auth_data['otp']:
        bot.reply_to(message, f"✅ Security code verified! Executing {command}...")
        del pending_auth[ADMIN_ID] 
        
        if command == "reboot":
            os.system("sudo reboot")
        elif command == "shutdown":
            os.system("sudo shutdown -h now")
        elif command == "clear cache":
            try:
                os.system("sudo rm -f /tmp/print_*.pdf /tmp/scanned_*.pdf /home/redwannabil/*.pdf")
                os.system("sudo journalctl --vacuum-time=1d")
                os.system("sudo apt-get clean")
                os.system("sudo sync; echo 3 | sudo tee /proc/sys/vm/drop_caches")
                bot.send_message(message.chat.id, "✅ Deep clean complete!")
            except Exception as e:
                bot.send_message(message.chat.id, f"❌ Error during cleanup: {e}")
            
    else:
        bot.reply_to(message, "❌ INCORRECT CODE. Authorization failed.")
        del pending_auth[ADMIN_ID]

# --- 4. SYSTEM PERFORMANCE ---
@bot.message_handler(commands=['performance'])
def check_performance(message):
    if message.from_user.id != ADMIN_ID:
        return
    status_msg = bot.reply_to(message, "🔄 Analyzing system performance... (Please wait ~20 seconds)")
    try:
        temp = subprocess.check_output(['vcgencmd', 'measure_temp']).decode('utf-8').replace('temp=', '').strip()
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        gpu_mem = subprocess.check_output(['vcgencmd', 'get_mem', 'gpu']).decode('utf-8').replace('gpu=', '').strip()
        
        # Calculate Total System Power Draw (Pi 5 PMIC Linear Correction)
        try:
            pmic_out = subprocess.check_output(['vcgencmd', 'pmic_read_adc']).decode('utf-8')
            currents = {}
            volts = {}
            
            # Parse all the Volts and Amps from the PMIC output
            for line in pmic_out.strip().split('\n'):
                if 'current' in line:
                    parts = line.split()
                    name = parts[0].replace('_A', '')
                    val = float(parts[1].split('=')[1].replace('A', ''))
                    currents[name] = val
                elif 'volt' in line:
                    parts = line.split()
                    name = parts[0].replace('_V', '')
                    val = float(parts[1].split('=')[1].replace('V', ''))
                    volts[name] = val
            
            # Calculate the total wattage of all 12 measurable branches
            pmic_power = sum(currents[name] * volts[name] for name in currents if name in volts)
            
            # Apply community standard linear correction for the unmeasured 5V rail
            total_power_watts = (pmic_power * 1.1451) + 0.5879
            power_str = f"{total_power_watts:.2f} W (Total System)"
        except Exception:
            power_str = "Unavailable"

        st = speedtest.Speedtest(secure=True)
        st.get_best_server()
        download_speed = st.download() / 1_000_000 
        upload_speed = st.upload() / 1_000_000  
        ping = st.results.ping

        perf_text = (
            f"📊 *Raspberry Pi Performance:*\n\n"
            f"🌡️ *Temperature:* {temp}\n"
            f"⚡ *Power Draw:* {power_str}\n"
            f"🧠 *CPU Usage:* {cpu_usage}%\n"
            f"💾 *RAM Usage:* {ram_usage}%\n"
            f"🎮 *GPU Memory:* {gpu_mem}\n\n"
            f"🌐 *Internet Speed:*\n"
            f"⬇️ Download: {download_speed:.2f} Mbps\n"
            f"⬆️ Upload: {upload_speed:.2f} Mbps\n"
            f"🏓 Ping: {ping:.1f} ms"
        )
        bot.edit_message_text(perf_text, chat_id="REDACTED_BY_SYSADMIN"
    except Exception as e:
        bot.edit_message_text(f"❌ Error fetching performance data: {e}", chat_id="REDACTED_BY_SYSADMIN"

# --- 5. EMERGENCY THUNDERSTORM RADAR (BACKGROUND THREAD) ---
def is_admin_working():
    try:
        output = subprocess.check_output("who", shell=True).decode('utf-8')
        return "redwannabil" in output
    except:
        return False

def is_admin_home():
    try:
        subprocess.check_output(f"ping -c 2 -W 2 {PHONE_IP}", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def radar_scan_loop():
    print("📡 Background Radar Thread Started!")
    while True:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}"
        try:
            response = requests.get(url).json()
            weather_id = response['weather'][0]['id']

            # Codes 200-232 are Thunderstorms
            if 200 <= weather_id <= 232:
                if is_admin_working():
                    bot.send_message(ADMIN_ID, "⚠️ THUNDERSTORM DETECTED! You are actively working on the Pi, so I am aborting auto-shutdown. Please save your work and unplug manually!")
                else:
                    if is_admin_home():
                        bot.send_message(ADMIN_ID, "🚨 THUNDERSTORM_ALARM 🚨")
                        bot.send_message(ADMIN_ID, "⚡ HEAVY DANGER! Thunderstorm overhead. I am executing an emergency shutdown. UNPLUG THE ADAPTER IN 30 SECONDS!")
                    else:
                        bot.send_message(ADMIN_ID, "🚨 THUNDERSTORM_ALARM 🚨")
                        bot.send_message(ADMIN_ID, "⚡ Storm approaching! You are not home. I am shutting down to protect the drives. Someone needs to physically UNPLUG THE ADAPTER!")
                    
                    time.sleep(5)
                    subprocess.call("sudo systemctl stop docker", shell=True)
                    time.sleep(5)
                    subprocess.call("sudo shutdown -h now", shell=True)
        except Exception as e:
            print(f"Radar error: {e}")
            
        # Wait 15 minutes (900 seconds) before checking the sky again
        time.sleep(900)

# --- 6. START THE BOT AND THE RADAR ---
if __name__ == "__main__":
    # Start the Radar in the background
    radar_thread = threading.Thread(target=radar_scan_loop, daemon=True)
    radar_thread.start()
    
    # Start the Telegram Bot in the foreground
    bot.infinity_polling()