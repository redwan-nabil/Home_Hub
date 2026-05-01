import telebot
import psutil
import speedtest
import subprocess
import os
import smtplib
import random
import string
import socket
import time
from email.message import EmailMessage

# --- 1. CREDENTIALS & CONFIGURATION ---
BOT_TOKEN = "REDACTED_BY_SYSADMIN"
ADMIN_ID = 1435882929

# Email Config
SENDER_EMAIL = "nabilredwoan2005@gmail.com"      
EMAIL_APP_PASSWORD = "REDACTED_BY_SYSADMIN"
RECEIVER_EMAIL = "redwannabil116@gmail.com"    

bot = telebot.TeleBot(BOT_TOKEN)
pending_auth = {} 

# --- 2. NETWORK SYNC (Wait for Internet on Boot) ---
def wait_for_internet():
    """Pauses the script on boot until the network is fully connected."""
    print("Checking for internet connection...")
    while True:
        try:
            # Try to connect to Telegram's servers
            socket.create_connection(("api.telegram.org", 443), timeout=5)
            print("Internet connected!")
            break
        except OSError:
            print("Network not ready. Retrying in 5 seconds...")
            time.sleep(5)

# --- 3. 2FA EMAIL FUNCTION ---
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

# --- 4. SYSTEM SECURE COMMANDS ---
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
            # Aggressive but safe shutdown sequence for NAS/CCTV
            bot.send_message(ADMIN_ID, "🛑 Shutting down Docker containers and syncing disks...")
            os.system("sudo systemctl stop docker") # Stop all heavy apps safely
            os.system("sudo sync")                  # Flush RAM to hard drives
            bot.send_message(ADMIN_ID, "🔌 Powering off now.")
            os.system("sudo shutdown -h now")       # Execute instant shutdown
            
        elif command == "clear cache":
            try:
                os.system("sudo rm -f /tmp/print_*.pdf /tmp/scanned_*.pdf /home/redwannabil/*.pdf")
                os.system("sudo journalctl --vacuum-time=1d")
                os.system("sudo apt-get clean")
                os.system("sudo sync; echo 3 | sudo tee /proc/sys/vm/drop_caches")
                bot.send_message(message.chat.id, "✅ Deep clean complete! RAM and Storage freed.")
            except Exception as e:
                bot.send_message(message.chat.id, f"❌ Error during cleanup: {e}")
            
    else:
        bot.reply_to(message, "❌ INCORRECT CODE. Authorization failed.")
        del pending_auth[ADMIN_ID]

# --- 5. SYSTEM PERFORMANCE ---
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
            pmic_power = sum(currents[name] * volts[name] for name in currents if name in volts)
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

# --- 6. STARTUP SEQUENCE ---
if __name__ == "__main__":
    wait_for_internet() # Halts execution until Wi-Fi/Ethernet connects
    
    # Send the boot message directly to your phone
    try:
        bot.send_message(ADMIN_ID, "🚀 *System Online:* Raspberry Pi has successfully booted and the Control Bot is ready.", parse_mode="Markdown")
    except Exception as e:
        print(f"Failed to send boot message: {e}")
        
    print("⚙️ Pi Admin Control Bot is running...")
    bot.infinity_polling()