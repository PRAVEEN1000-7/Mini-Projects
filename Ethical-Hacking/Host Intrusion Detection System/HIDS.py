import hashlib
import os
import psutil
import smtplib
import socket
import time
from email.message import EmailMessage
from datetime import datetime

# Configuration
FILES_TO_MONITOR = {
    "example.txt": None,
    "important_config.conf": None,
}
SUSPICIOUS_PROCESSES = ["nc", "netcat", "nmap", "wireshark", "tcpdump", "metasploit"]
PORTS_TO_SCAN = [22, 80, 443, 8080, 3306, 5900]
LOG_FILE = "hids_log.txt"
CHECK_INTERVAL = 20
EMAIL_ALERTS = True

EMAIL_SENDER = "youremail@example.com"
EMAIL_PASSWORD = "yourpassword"
EMAIL_RECEIVER = "receiver@example.com"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] {message}\n")
    print(f"{timestamp} {message}")

def send_email_alert(subject, body):
    if not EMAIL_ALERTS:
        return
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        log_event("Alert email sent.")
    except Exception as e:
        log_event(f"Failed to send email alert: {e}")

def calculate_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        log_event(f"Error reading {filepath}: {e}")
        return None

def check_files_integrity():
    for file in FILES_TO_MONITOR:
        current_hash = calculate_file_hash(file)
        if current_hash is None:
            log_event(f"Cannot access {file}. It may be missing or locked.")
            continue
        if FILES_TO_MONITOR[file] is None:
            FILES_TO_MONITOR[file] = current_hash
            log_event(f"Initial hash set for {file}: {current_hash}")
        elif FILES_TO_MONITOR[file] != current_hash:
            alert_msg = f"File {file} modified!\nOld hash: {FILES_TO_MONITOR[file]}\nNew hash: {current_hash}"
            log_event(f"ALERT: {alert_msg}")
            send_email_alert(f"File Integrity Alert: {file}", alert_msg)
            FILES_TO_MONITOR[file] = current_hash
        else:
            log_event(f"{file} is unchanged.")

def monitor_suspicious_processes():
    suspicious_found = []
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            pname = proc.info['name'].lower() if proc.info['name'] else ""
            if any(tool in pname for tool in SUSPICIOUS_PROCESSES):
                suspicious_found.append((proc.info['pid'], proc.info['name']))
    except Exception as e:
        log_event(f"Error during process scan: {e}")
    if suspicious_found:
        alert_msg = "Suspicious processes detected:\n"
        for pid, name in suspicious_found:
            alert_msg += f" - PID: {pid} Name: {name}\n"
        log_event(f"ALERT: {alert_msg.strip()}")
        send_email_alert("Suspicious Processes Detected", alert_msg)
    else:
        log_event("No suspicious processes found.")

def scan_ports():
    open_ports = []
    for port in PORTS_TO_SCAN:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex(("127.0.0.1", port))
            if result == 0:
                open_ports.append(port)
    if open_ports:
        msg = f"Open ports detected: {', '.join(str(p) for p in open_ports)}"
        log_event(f"ALERT: {msg}")
        send_email_alert("Open Ports Detected", msg)
    else:
        log_event("No monitored ports are open.")

def main():
    log_event("=== HIDS Monitoring Started ===")
    while True:
        check_files_integrity()
        monitor_suspicious_processes()
        scan_ports()
        log_event("--- Sleeping ---\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
