🔒 Advanced Context-Aware Logging Simulation (Educational Project)
Project Status: Complete | Language: Python 3.x | Target OS: Windows (Simulated)
⚠️ ETHICAL AND EDUCATIONAL DISCLAIMER (MANDATORY READ)
This project is a theoretical, educational simulation designed for academic research and defensive cybersecurity training purposes only.
The code is strictly intended to demonstrate the architectural principles of system monitoring, file handling, and secure data transmission techniques. It is configured to run only in a highly controlled, simulated environment (by explicitly checking for a placeholder window title).
This repository does not contain production-ready malware. Any attempt to modify, distribute, or use this code for illegal, unethical, or malicious purposes is strictly prohibited and violates the terms of this license.
💡 Project Overview
This project simulates a highly efficient, stealthy, and persistent log collection utility. It moves beyond a basic console script to demonstrate real-world cybersecurity concepts such as:
Stealth Execution: Utilizing VBScript (run_logger.vbs) to execute the Python core silently in the background, suppressing any console window (pythonw.exe).
Context-Aware Logging: Keystrokes are only captured when the user is actively engaged with a specific target application (simulated by checking for the window title: "Notepad - MyNotes.txt").
Asynchronous Secure Exfiltration: Log files are rotated every 50 keystrokes and delivered via secure TLS/SSL email transmission every 2 minutes using a background thread (threading and smtplib).
Data Hygiene: Successfully delivered log files are automatically deleted from the system disk to maintain a low profile and prevent data buildup.
🛠️ Technology Stack
Core Language: Python 3.x
Keylogging: pynput library
Networking: smtplib (for secure email delivery via TLS)
Execution: VBScript (.vbs) and pythonw.exe
⚙️ Setup and Configuration
1. Prerequisites
Ensure you have Python 3.x installed and set up the necessary library:
pip install pynput


2. Configure keystroke_logger_simulation.py
You must update the email configuration section with your own details. For security, use an App Password from your email provider, not your main account password.
# --- EMAIL CONFIGURATION (MUST BE UPDATED) ---
SENDER_EMAIL = "your_sending_email@gmail.com"
RECEIVER_EMAIL = "your_receiving_email@example.com"
SENDER_PASSWORD = "your_app_password_here"     # REMOVE ALL SPACES from the App Password!
DELIVERY_INTERVAL_SECONDS = 120 # 2 minutes
# ...


3. File Structure
Place both files in the same directory:
/AdvancedLoggerProject/
├── keystroke_logger_simulation.py  (The core logic)
└── run_logger.vbs                  (The silent launcher)


🚀 Usage
Prepare the Target: Create a file named MyNotes.txt and open it in Notepad. The script will only log activity in this specific window.
Launch Silently: Double-click the run_logger.vbs file. No console window will appear. The Python script is now running silently in the background.
Operation: Start typing in the Notepad window. Logs will be generated in the simulated_logs_advanced subdirectory.
Delivery: Check your RECEIVER_EMAIL every 2 minutes for new log attachments.
Stop Execution: To terminate the background script gracefully, globally press the ESC key.
