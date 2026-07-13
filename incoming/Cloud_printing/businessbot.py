import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import time
import threading
import subprocess
from PyPDF2 import PdfReader, PdfWriter

# --- CONFIGURATION ---
BOT_TOKEN = "REDACTED_BY_SYSADMIN"
ADMIN_ID = 1435882929 
PRINTER_NAME = 'EpsonMobile'

bot = telebot.TeleBot(BOT_TOKEN)

# Dictionaries and Hardware Locks
user_states = {}
jobs = {}
scanner_hardware_lock = threading.Lock()

print("🚀 Business Print/Scan Bot is Online!")

# --- TEXT TEMPLATES ---
PAYMENT_TEXT = """Please make your payment first using one of the following methods:
Bkash/Nagad: 01575148867
AB Bank: 1111175174300
Name: REDWAN NABIL
Branch: Board Bazar

After paying, please reply with the mobile number or bank A/C number you used to send the money."""

PRINT_PRESETS = """★ Printing Preferences
Page Size: A4
Quality: Standard (Plain 80gsm paper)
Pages: All pages in your PDF will be printed.

Note: You cannot change these settings here. If you need custom preferences, please contact the admin directly: t.me/Redwan_Nabil2003.

Please choose your print format and color preference to proceed:"""

SCAN_PRESETS = """★ Scanning Preferences
Format: PDF
Size: A4
Color: Full Color
Resolution: 600 DPI (High Quality)
Price: 3৳ per scan

Note: You cannot change these settings here. If you need custom preferences, please contact the admin directly: t.me/Redwan_Nabil2003 (@Redwan_Nabil2003).

Are you sure you want to submit your documents to the admin?"""


# --- FEATURE: PRINTER STATUS CHECKER ---
def is_printer_online():
    try:
        status = subprocess.check_output(f"lpstat -p {PRINTER_NAME}", shell=True, stderr=subprocess.STDOUT).decode('utf-8').lower()
        if "disabled" in status or "unplugged" in status or "not connected" in status or "offline" in status:
            return False
        return True
    except:
        return False

# --- FEATURE: EXECUTION PAUSER ---
def ensure_printer_online_and_notify(user_id, job):
    if not is_printer_online():
        bot.send_message(ADMIN_ID, f"🔔 **ATTENTION ADMIN!**\nCustomer '{job['name']}' is ready to {job['type']}.\nPlease turn ON your printer/scanner!", parse_mode="Markdown")
        bot.send_message(user_id, "⚠️ Printer is currently off. Your job will start automatically as soon as the admin turns it on. Please wait...")
        
        while not is_printer_online():
            time.sleep(5)
            
        bot.send_message(user_id, "✅ Printer turned on, starting your job now...")

# --- START AND GROUP HANDLING ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Just send me a PDF file to start printing, or type /scan to request a scan.")

@bot.message_handler(commands=['print'])
def handle_print_command(message):
    if message.chat.type in ['group', 'supergroup']:
        bot.reply_to(message, "Please check your inbox, I sent you a message!")
    try:
        bot.send_message(message.from_user.id, "Please submit your PDF file now (ensure it is in .pdf format).")
    except Exception:
        bot.reply_to(message, "⚠️ Please start a private message with me first by clicking the Start button!")

# --- AUTOMATIC FILE CATCHER ---
@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_id = message.from_user.id
    
    if not message.document.file_name.lower().endswith('.pdf'):
        bot.send_message(user_id, "⚠️ Invalid file format. Please submit a valid PDF file.")
        return

    bot.send_message(user_id, "📥 Document received! Downloading...")
    
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = f"/home/redwannabil/print_{message.message_id}.pdf"
    
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
        
    # --- MAGIC FIX: BLANK PAGE INJECTION ---
    try:
        reader = PdfReader(file_path)
        total_pages = len(reader.pages)
        
        if total_pages > 1 and total_pages % 2 != 0:
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            
            last_page = reader.pages[-1]
            writer.add_blank_page(width=last_page.mediabox.width, height=last_page.mediabox.height)
            
            with open(file_path, "wb") as f:
                writer.write(f)
            
            total_pages += 1 
            
    except Exception as e:
        print("PDF Read Error:", e)
        total_pages = 1
        
    job_id = str(message.message_id)
    jobs[job_id] = {'user_id': user_id, 'file_path': file_path, 'type': 'print', 'name': message.from_user.first_name, 'total_pages': total_pages}
    user_states[user_id] = {'current_job': job_id}
    
    # --- UPDATED PRICE MENU ---
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🎨 Color 1-Side (6৳/pg)", callback_data=f"print_color_one_{job_id}"),
        InlineKeyboardButton("⚫⚪ B/W 1-Side (4৳/pg)", callback_data=f"print_bw_one_{job_id}")
    )
    markup.add(
        InlineKeyboardButton("🎨 Color 2-Side (10৳/pg)", callback_data=f"print_color_both_{job_id}"),
        InlineKeyboardButton("⚫⚪ B/W 2-Side (5৳/pg)", callback_data=f"print_bw_both_{job_id}")
    )
    markup.add(InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_job_{job_id}"))
    
    bot.send_message(user_id, PRINT_PRESETS, reply_markup=markup)

@bot.message_handler(content_types=['photo', 'video', 'audio', 'voice'])
def handle_wrong_format(message):
    bot.send_message(message.from_user.id, "⚠️ Please send your document as a **File** (.pdf) to print it, not as a photo or video.", parse_mode="Markdown")

# --- THE SCAN WORKFLOW ---
@bot.message_handler(commands=['scan'])
def handle_scan_command(message):
    if message.chat.type in ['group', 'supergroup']:
        bot.reply_to(message, "Please check your inbox, I sent you a message!")
        
    try:
        user_id = message.from_user.id
        job_id = str(message.message_id)
        jobs[job_id] = {'user_id': user_id, 'type': 'scan', 'name': message.from_user.first_name}
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Yes", callback_data=f"sure_scan_{job_id}"),
                   InlineKeyboardButton("No", callback_data=f"cancel_scan_{job_id}"))
        bot.send_message(user_id, SCAN_PRESETS, reply_markup=markup)
            
    except Exception:
        bot.reply_to(message, "⚠️ Please start a private message with me first!")

# --- INLINE BUTTON CLICKS ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    data = call.data.split('_')
    job_id = data[-1]
    action = "_".join(data[:-1]) 
    job = jobs.get(job_id)

    if not job:
        bot.answer_callback_query(call.id, "This job has expired.")
        return

    user_id = job['user_id']

    # --- COMBINED PRINT LOGIC ---
    if action in ["print_color_one", "print_bw_one", "print_color_both", "print_bw_both"]:
        is_color = "color" in action
        is_both = "both" in action
        
        job['color_pref'] = "Color" if is_color else "Black & White"
        job['cups_color'] = "COLOR" if is_color else "MONO"
        job['duplex'] = "Both-Sided" if is_both else "One-Sided"
        
        bot.edit_message_text(f"Great! You selected **{job['color_pref']} ({job['duplex']})**.", chat_id="REDACTED_BY_SYSADMIN"
        
        bot.send_message(user_id, PAYMENT_TEXT)
        user_states[user_id] = {'state': 'WAITING_FOR_PAYMENT', 'current_job': job_id}
        
    elif action == "sure_scan":
        bot.edit_message_text("Great!", chat_id="REDACTED_BY_SYSADMIN"
        bot.send_message(user_id, PAYMENT_TEXT)
        user_states[user_id] = {'state': 'WAITING_FOR_PAYMENT', 'current_job': job_id}

    elif action == "cancel_job":
        bot.edit_message_text("Print cancelled.", chat_id="REDACTED_BY_SYSADMIN"
        if os.path.exists(job['file_path']):
            os.remove(job['file_path'])
            
    elif action == "cancel_scan":
        bot.edit_message_text("Scan request cancelled.", chat_id="REDACTED_BY_SYSADMIN"

    # Admin verifies payment
    elif action == "admin_payyes":
        new_status = f"✅ Payment verified for {job['name']}."
        try:
            bot.edit_message_caption(new_status, chat_id="REDACTED_BY_SYSADMIN"
        except:
            bot.edit_message_text(new_status, chat_id="REDACTED_BY_SYSADMIN"
        
        bot.send_message(user_id, "Admin is processing your request...")
        
        if job['type'] == 'print':
            
            # --- START PRINT EXECUTION THREAD ---
            def process_print():
                ensure_printer_online_and_notify(user_id, job)
                
                bot.send_message(ADMIN_ID, f"🖨️ Sending to printer as {job['color_pref']}, {job.get('duplex', 'One-Sided')}...")
                bot.send_message(user_id, f"✅ Payment verified! Your document is printing now in {job['color_pref']} ({job.get('duplex', 'One-Sided')}).")
                
                if job.get('duplex') == 'Both-Sided':
                    total_pages = job.get('total_pages', 1)
                    
                    if total_pages == 1:
                        # Fallback to 1-sided if they requested both-sided on a 1 page document
                        os.system(f"lp -d {PRINTER_NAME} -o media=A4 -o sides=one-sided -o Ink={job['cups_color']} -o fit-to-page '{job['file_path']}'")
                        time.sleep(5) 
                        try:
                            if os.path.exists(job['file_path']):
                                os.remove(job['file_path'])
                        except: pass
                        bot.send_message(user_id, "🎉 Your print is ready! You can collect it now.")
                    else:
                        # ---------------------------------------------------------
                        # NORMAL ODD PAGES (1, 3, 5...)
                        # Stack ends up with Page 1 on Bottom, Page 3 on Top.
                        # ---------------------------------------------------------
                        os.system(f"lp -d {PRINTER_NAME} -o media=A4 -o page-set=odd -o Ink={job['cups_color']} -o fit-to-page '{job['file_path']}'")
                        
                        markup = InlineKeyboardMarkup()
                        markup.add(InlineKeyboardButton("✅ Done (Print Even Pages)", callback_data=f"admin_flippage_{job_id}"))
                        
                        instructions = (
                            "⚠️ **BOTH-SIDED PRINT PAUSED**\n\n"
                            "The odd pages are printing now.\n"
                            "1. Wait for them to finish completely.\n"
                            "2. Take the entire stack as it is (DO NOT shuffle them).\n"
                            "3. Flip the ENTIRE stack over so the printed sides are facing DOWN (blank sides UP).\n"
                            "4. Put the stack back into the paper feeder.\n\n"
                            "Click 'Done' when ready to print even pages."
                        )
                        bot.send_message(ADMIN_ID, instructions, parse_mode="Markdown", reply_markup=markup)
                else:
                    # Normal One-Sided Print
                    os.system(f"lp -d {PRINTER_NAME} -o media=A4 -o sides=one-sided -o Ink={job['cups_color']} -o fit-to-page '{job['file_path']}'")
                    time.sleep(5)
                    try:
                        if os.path.exists(job['file_path']):
                            os.remove(job['file_path'])
                    except: pass
                    bot.send_message(user_id, "🎉 Your print is ready! You can collect it now.")
            
            threading.Thread(target=process_print).start()
                
        elif job['type'] == 'scan':
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("✅ Start Scanning", callback_data=f"admin_startscan_{job_id}"),
                       InlineKeyboardButton("❌ Refuse", callback_data=f"admin_refuse_{job_id}"))
            bot.send_message(ADMIN_ID, f"🔔 Payment received. Place {job['name']}'s document on the scanner and click Start.", reply_markup=markup)

    # --- ADMIN FLIPS PAGE BUTTON ---
    elif action == "admin_flippage":
        # --- START FLIP PAGE EXECUTION THREAD ---
        def process_even_pages():
            ensure_printer_online_and_notify(user_id, job)
            
            try:
                bot.edit_message_text("🖨️ Sending even pages to printer...", chat_id="REDACTED_BY_SYSADMIN"
            except: pass
            
            # ---------------------------------------------------------
            # NORMAL EVEN PAGES (2, 4, 6...)
            # Since flipping the stack put Page 1 on top, it prints Page 2 on it first!
            # ---------------------------------------------------------
            os.system(f"lp -d {PRINTER_NAME} -o media=A4 -o page-set=even -o Ink={job['cups_color']} -o fit-to-page '{job['file_path']}'")
            
            time.sleep(5) 
            
            try:
                if os.path.exists(job['file_path']):
                    os.remove(job['file_path'])
            except: pass
            
            bot.send_message(user_id, "🎉 Your both-sided print is ready! You can collect it now.")
            bot.send_message(ADMIN_ID, "✅ Both-sided job complete.")
            
        threading.Thread(target=process_even_pages).start()

    elif action == "admin_payno":
        new_status = f"❌ Payment rejected for {job['name']}."
        try:
            bot.edit_message_caption(new_status, chat_id="REDACTED_BY_SYSADMIN"
        except:
            bot.edit_message_text(new_status, chat_id="REDACTED_BY_SYSADMIN"
            
        bot.send_message(user_id, "❌ Your payment could not be verified. Please try again or contact the admin.\n\n" + PAYMENT_TEXT)
        user_states[user_id] = {'state': 'WAITING_FOR_PAYMENT', 'current_job': job_id}

    # Admin Scan Handling
    elif action == "admin_startscan":
        
        # --- START SCAN EXECUTION THREAD (WITH HARDWARE LOCK) ---
        def process_scan():
            ensure_printer_online_and_notify(user_id, job)
            
            with scanner_hardware_lock:
                try:
                    bot.edit_message_text("⏳ Scanning in progress...", chat_id="REDACTED_BY_SYSADMIN"
                except: pass
                
                bot.send_message(user_id, "✅ Scanner is active. Processing your document now...")
                
                scan_file = f"/tmp/scanned_{job_id}.pdf"
                
                os.system(f"scanimage --mode Color --resolution 600 -x 210 -y 297 --format=pdf > {scan_file}")
                
                if os.path.exists(scan_file) and os.path.getsize(scan_file) > 1024:
                    bot.send_message(user_id, "Scan complete! Uploading...")
                    try:
                        with open(scan_file, 'rb') as doc:
                            bot.send_document(user_id, doc, timeout=300)
                        bot.send_message(ADMIN_ID, "✅ Scan sent to user.")
                    except Exception as e:
                        print(f"Telegram upload error: {e}")
                        bot.send_message(user_id, "❌ File too large for Telegram. Admin will send it manually.")
                else:
                    bot.send_message(user_id, "❌ Hardware error: Scanner was busy or failed to read the document.")
                    bot.send_message(ADMIN_ID, f"❌ Scanner hardware error for {job['name']}. Please try scanning manually.")
                
                # File cleanup handled by Garbage Collector below
            
        threading.Thread(target=process_scan).start()

# --- PAYMENT TEXT HANDLING ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    state_info = user_states.get(user_id)

    if message.text.startswith('/'):
        return

    if state_info and state_info.get('state') == 'WAITING_FOR_PAYMENT':
        payment_num = message.text
        job_id = state_info.get('current_job')
        job = jobs.get(job_id)
        
        bot.send_message(user_id, "⏳ Sending payment details to admin...")
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Yes", callback_data=f"admin_payyes_{job_id}"),
                   InlineKeyboardButton("No", callback_data=f"admin_payno_{job_id}"))
        
        job_type_str = f"Print ({job.get('color_pref', 'PDF')} | {job.get('duplex', 'One-Sided')})" if job['type'] == 'print' else "Scan"          
        admin_msg = f"📥 {job_type_str} Request from '{job['name']}'\nPayment Details: '{payment_num}'\n\nVerify payment?"

        if job['type'] == 'print':
            with open(job['file_path'], 'rb') as doc:
                bot.send_document(ADMIN_ID, doc, caption=admin_msg, reply_markup=markup)
        else:
            bot.send_message(ADMIN_ID, admin_msg, reply_markup=markup)
        
        user_states[user_id] = {'state': 'IDLE'}

# ==========================================
# ENTERPRISE N8N API BRIDGE (NEW)
# ==========================================
from flask import Flask, request, jsonify
import werkzeug

app = Flask(__name__)

@app.route('/n8n_webhook', methods=['POST'])
def handle_n8n_job():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400
        
    file = request.files['file']
    platform = request.form.get('platform', 'Unknown')
    customer_id = request.form.get('customer_id', 'Guest')
    
    # Save the file locally
    filename = werkzeug.utils.secure_filename(file.filename)
    file_path = f"/home/redwannabil/n8n_print_{customer_id}_{filename}"
    file.save(file_path)
    
    # Immediately notify Admin via Telegram
    bot.send_message(
        ADMIN_ID, 
        f"🌐 <b>OMNICHANNEL PRINT JOB</b>\nPlatform: {platform}\nCustomer ID: {customer_id}\nFile: {filename}\n\n<i>Sending to printer automatically...</i>",
        parse_mode="HTML"
    )
    
    # Send to CUPS Printer
    os.system(f"lp -d {PRINTER_NAME} -o media=A4 -o fit-to-page '{file_path}'")
    
    return jsonify({"status": "success", "message": "Job sent to printer spooler!"}), 200

def run_api():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# ==========================================
# AUTOMATED GARBAGE COLLECTOR THREAD
# ==========================================
def garbage_collector():
    """Silently cleans up abandoned or finished print/scan files older than 1 hour"""
    while True:
        try:
            now = time.time()
            directories = ['/home/redwannabil', '/tmp']
            
            for directory in directories:
                if not os.path.exists(directory):
                    continue
                    
                for filename in os.listdir(directory):
                    if filename.endswith(".pdf") and (filename.startswith("print_") or filename.startswith("n8n_print_") or filename.startswith("scanned_")):
                        filepath = os.path.join(directory, filename)
                        # If the file is older than 3600 seconds (1 hour)
                        if os.path.getctime(filepath) < (now - 3600):
                            os.remove(filepath)
                            print(f"[GARBAGE COLLECTOR] Wiped old file: {filepath}")
        except Exception as e:
            print(f"[GARBAGE ERROR] {e}")
            
        time.sleep(3600) # Sleep for 1 hour before checking again

# Start background threads
threading.Thread(target=run_api, daemon=True).start()
threading.Thread(target=garbage_collector, daemon=True).start()

bot.infinity_polling()