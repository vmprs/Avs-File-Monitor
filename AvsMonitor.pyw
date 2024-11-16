import os
import time
import subprocess
import sys
import threading
from tkinter import Tk, Label, Button, Text, END, NORMAL, DISABLED
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Function to install missing modules
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install required packages
required_packages = ['watchdog', 'psutil']

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"{package} is not installed. Installing...")
        install(package)

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def on_created(self, event):
        if not event.is_directory:
            self.text_widget.config(state=NORMAL)
            self.text_widget.insert(END, f"File created: {event.src_path}\n")
            self.text_widget.see(END)
            self.text_widget.config(state=DISABLED)
            self.check_suspicious_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.text_widget.config(state=NORMAL)
            self.text_widget.insert(END, f"File deleted: {event.src_path}\n")
            self.text_widget.see(END)
            self.text_widget.config(state=DISABLED)

    def on_moved(self, event):
        if not event.is_directory:
            self.text_widget.config(state=NORMAL)
            self.text_widget.insert(END, f"File renamed/moved from {event.src_path} to {event.dest_path}\n")
            self.text_widget.see(END)
            self.text_widget.config(state=DISABLED)

    def check_suspicious_file(self, file_path):
        # Update the list of suspicious extensions to include .bat
        suspicious_extensions = ['.exe', '.dll', '.scr', '.bat']  # Added .bat here
        if any(file_path.endswith(ext) for ext in suspicious_extensions):
            self.text_widget.config(state=NORMAL)
            self.text_widget.insert(END, f"Suspicious file detected: {file_path}\n")
            self.text_widget.see(END)
            self.text_widget.config(state=DISABLED)

def get_download_folder():
    return os.path.join(os.path.expanduser("~"), "Downloads")

def get_temp_folder():
    return os.path.join(os.environ.get("TEMP", "/tmp"))

def monitor_directory(path, text_widget):
    event_handler = FileEventHandler(text_widget)
    observer = Observer()

    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    text_widget.config(state=NORMAL)
    text_widget.insert(END, f"Monitoring the directory: {path}\n")
    text_widget.config(state=DISABLED)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def start_monitoring(text_widget):
    download_folder = get_download_folder()
    temp_folder = get_temp_folder()

    threading.Thread(target=monitor_directory, args=(download_folder, text_widget), daemon=True).start()
    threading.Thread(target=monitor_directory, args=(temp_folder, text_widget), daemon=True).start()

def create_gui():
    root = Tk()
    root.title("AVS Monitor Essentials")
    
    root.resizable(False, False)

    label = Label(root, text="AVS Monitor Essentials")
    label.pack(pady=10)

    description = Label(root, text="Monitoring your Downloads and Temp folders for new files.")
    description.pack(pady=5)

    text_widget = Text(root, wrap='word', height=20, width=60)
    text_widget.pack(padx=10, pady=10)
    text_widget.config(state=DISABLED)

    start_button = Button(root, text="Start Monitoring", command=lambda: start_monitoring(text_widget))
    start_button.pack(pady=5)

    stop_button = Button(root, text="Exit", command=root.quit)
    stop_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()