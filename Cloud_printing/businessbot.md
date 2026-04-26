# BusinessBot README

## Overview

`businessbot.py` is a Telegram bot designed to streamline the process of printing and scanning documents for users. It provides an easy-to-use interface for customers to submit PDF files for printing or request document scanning. The bot integrates with a printer and scanner, allowing for automated job handling, payment verification, and communication between users and the administrator.

---

## Features

### 1. **Print Documents**
- Users can send PDF files to the bot for printing.
- Supports both **color** and **black & white** printing.
- Offers options for **one-sided** or **both-sided** printing.
- Automatically handles odd-page documents by injecting a blank page to ensure proper duplex printing.
- Notifies the administrator when the printer is offline and pauses the job until the printer is online.

### 2. **Scan Documents**
- Users can request document scanning in **PDF format**.
- Scanning preferences:
  - Format: PDF
  - Size: A4
  - Color: Full Color
  - Resolution: 600 DPI
  - Price: 3৳ per scan
- Ensures scanner hardware is not accessed by multiple jobs simultaneously using threading locks.
- Uploads scanned documents directly to the user via Telegram.

### 3. **Payment Handling**
- Users are required to make payments before their jobs are processed.
- Payment methods include Bkash, Nagad, and AB Bank.
- Users provide payment details, which are sent to the administrator for verification.
- The administrator can approve or reject payments via inline buttons.

### 4. **Admin Notifications**
- The bot notifies the administrator when:
  - A new job is submitted.
  - The printer or scanner is offline.
  - Payment details are provided by the user.
  - A job requires manual intervention (e.g., flipping pages for duplex printing).

### 5. **Error Handling**
- Handles invalid file formats (e.g., non-PDF files).
- Notifies users if the printer or scanner is offline.
- Provides clear instructions for resolving issues, such as starting a private chat with the bot or contacting the administrator.

---

## Requirements

### Dependencies
The following Python libraries are required to run the bot:
- `pyTelegramBotAPI` (install via `pip install pyTelegramBotAPI`)
- `PyPDF2` (install via `pip install PyPDF2`)

### Hardware Requirements
- A printer compatible with the `lp` command (e.g., EpsonMobile).
- A scanner compatible with the `scanimage` command.

### Environment
- Python 3.6 or higher.
- A Linux-based operating system with `lp` and `scanimage` commands installed.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/Cloud_printing.git
   cd Cloud_printing
   ```

2. **Install Dependencies**:
   ```bash
   pip install pyTelegramBotAPI PyPDF2
   ```

3. **Configure the Bot**:
   - Replace `REDACTED_BY_SYSADMIN` in the `BOT_TOKEN` variable with your actual Telegram Bot Token.
   - Replace `ADMIN_ID` with the Telegram user ID of the administrator.
   - Replace `PRINTER_NAME` with the name of your printer (e.g., `EpsonMobile`).

4. **Run the Bot**:
   ```bash
   python businessbot.py
   ```

---

## Usage

### Commands
- **`/start`**: Start the bot and receive a welcome message.
- **`/print`**: Initiate the printing process. The bot will prompt the user to upload a PDF file.
- **`/scan`**: Request a document scan. The bot will guide the user through the process.

### File Submission
- Users must send their documents as **PDF files**. Other file formats (e.g., images, videos) are not supported for printing.

### Payment
- After submitting a job, users will receive payment instructions. They must reply with their payment details (e.g., transaction ID or bank account number).
- The administrator will verify the payment and approve or reject the job.

### Admin Actions
- The administrator can:
  - Approve or reject payments.
  - Start scanning jobs.
  - Handle duplex printing by flipping pages for even-side printing.

---

## Technical Details

### Printer Status Checker
The bot uses the `lpstat` command to check the status of the printer. If the printer is offline, the bot notifies the administrator and pauses the job until the printer is online.

### PDF Handling
The bot uses the `PyPDF2` library to process PDF files. If a document has an odd number of pages, the bot automatically adds a blank page to ensure proper duplex printing.

### Threading
The bot uses threading to handle long-running tasks (e.g., printing and scanning) without blocking other operations.

### Security
- The bot token is stored in the `BOT_TOKEN` variable and should be kept confidential.
- User payment details are sent only to the administrator for verification.

---

## Folder Structure

```
Cloud_printing/
│
├── businessbot.py        # Main bot script
├── README.md             # Documentation
└── requirements.txt      # Python dependencies
```

---

## Known Limitations
1. The bot only supports PDF files for printing.
2. The bot relies on the `lp` and `scanimage` commands, which may not be available on all systems.
3. Large scanned files may exceed Telegram's file size limit, requiring manual intervention by the administrator.

---

## Future Improvements
1. Add support for more file formats (e.g., Word documents, images).
2. Implement a web-based admin dashboard for easier job management.
3. Add support for multiple printers and scanners.
4. Enhance error handling and logging for better debugging.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact
For any issues or feature requests, please contact the administrator at [t.me/Redwan_Nabil2003](https://t.me/Redwan_Nabil2003).