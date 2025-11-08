# Advanced Context-Aware Logging Simulation

> **NOTICE — Ethical & Educational Use Only**
>
> This repository is a theoretical, educational simulation designed **only** for academic research and defensive cybersecurity training. It is **not** production-ready malware. Any attempt to modify, distribute, or use this code for illegal, unethical, or malicious purposes is strictly prohibited and violates this license.

---

## Project Status

* **Status:** Complete
* **Language:** Python 3.x
* **Target OS:** Windows (Simulated)

---

## Overview

This project simulates an efficient, context-aware log collection utility intended for educational and defensive demonstrations. It illustrates architectural principles such as stealth execution (simulated), context-aware logging (window-title based), asynchronous secure delivery of log files, and secure data hygiene.

**Key concepts demonstrated:**

* **Stealth Execution (simulation):** Uses a VBScript launcher (`run_logger.vbs`) to start the Python core with `pythonw.exe` so no console window appears in the simulated environment.
* **Context-Aware Logging:** Keystrokes are only recorded when the target application window is active (simulated by checking for the window title: `Notepad - MyNotes.txt`).
* **Asynchronous Secure Exfiltration:** Rotates log files every 50 keystrokes and sends them as attachments over TLS/SSL email on a background thread at a fixed interval.
* **Data Hygiene:** Successfully delivered log files are removed from disk to minimize footprint.

---

## Technology Stack

* **Core Language:** Python 3.x
* **Keylogging:** `pynput`
* **Networking / Delivery:** `smtplib` (secure TLS/SSL email)
* **Launcher:** VBScript (`run_logger.vbs`) + `pythonw.exe`

---

## Ethical and Safety Reminder

This repository is strictly for learning and defensive use. Do not run this code on machines you do not own or control. Do not modify it for malicious purposes. Always obtain explicit written consent before performing any monitoring or logging activities on another person's system.

---

## Setup and Configuration

### 1. Prerequisites

Ensure you have Python 3.x installed and then install the required Python library:

```bash
pip install pynput
```

### 2. Configure `keystroke_logger_simulation.py`

Open the script and update the email configuration section with your own details. For security, use an App Password from your email provider rather than your main account password.

```python
# --- EMAIL CONFIGURATION (MUST BE UPDATED) ---
SENDER_EMAIL = "your_sending_email@gmail.com"
RECEIVER_EMAIL = "your_receiving_email@example.com"
SENDER_PASSWORD = "your_app_password_here"     # REMOVE ALL SPACES from the App Password!
DELIVERY_INTERVAL_SECONDS = 120  # 2 minutes
# ...
```

> **Security note:** Treat the app password like a secret. Do not commit real credentials to public repositories. Use environment variables or a secrets manager in real projects.

### 3. File Structure

Place both files in the same directory:

```
/AdvancedLoggerProject/
├── keystroke_logger_simulation.py  (The core logic)
└── run_logger.vbs                  (The silent launcher)
```

---

## Usage (Simulated)

1. **Prepare the Target (simulation):** Create a file named `MyNotes.txt` and open it in Notepad. The script is configured to only log activity in this specific window title (`Notepad - MyNotes.txt`).

2. **Launch Silently:** Double-click `run_logger.vbs`. The Python script will start without showing a console window (uses `pythonw.exe` in simulation).

3. **Operation:** Start typing inside the Notepad window. Log files will be written to the `simulated_logs_advanced` subdirectory and rotated every 50 keystrokes.

4. **Delivery:** The background delivery thread will attempt to send rotated logs as TLS-encrypted email attachments at the configured interval (default: every 2 minutes).

5. **Stop Execution:** Press the `ESC` key globally to terminate the script gracefully.

---

## Important Limitations & Notes

* **This is a simulation:** The project checks for a specific window title to *simulate* context-aware logging. It is not designed for deployment in production systems.
* **Do not use on production or third-party systems.** Unauthorised logging or monitoring is illegal and unethical.
* **Credentials handling:** Never store plaintext credentials in public repositories. Use environment variables, vaults, or a configuration excluded from version control (e.g., add to `.gitignore`).

---

## License

This repository is provided for educational and defensive research purposes only. By using or modifying this code you agree not to use it for malicious or unauthorized monitoring. The author(s) disclaim any liability for misuse.

---

## Contact / Attribution

If you have questions about the simulation, defensive use cases, or safe testing practices, document them in the repository issues or contact the author via the project’s preferred channels.

---

*Prepared for academic and defensive cybersecurity training.*
