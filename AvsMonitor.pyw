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
required_packages = ['watchdog']

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
        if event.is_directory:  # Check if a new directory was created
            self._log_event(f"Directory created: {event.src_path}")
        else:  # Handle file creations
            self._log_event(f"File created: {event.src_path}")
            self.check_suspicious_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self._log_event(f"File deleted: {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            self._log_event(f"File renamed/moved from {event.src_path} to {event.dest_path}")

    def _log_event(self, message):
        self.text_widget.config(state=NORMAL)
        self.text_widget.insert(END, message + "\n")
        self.text_widget.see(END)
        self.text_widget.config(state=DISABLED)

    def check_suspicious_file(self, file_path):
        suspicious_extensions = ['.exe', '.dll', '.scr', '.bat']
        if any(file_path.endswith(ext) for ext in suspicious_extensions):
            self._log_event(f"Suspicious file detected: {file_path}")

class DirectoryMonitor:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.observers = {}  # Dictionary to hold observers for each path
        self.running_threads = {}  # To track thread health state

    def monitor_directory(self, path):
        event_handler = FileEventHandler(self.text_widget)
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        self.observers[path] = observer
        self.running_threads[path] = True
        
        self._log_event(f"Monitoring the directory: {path}")

        try:
            while self.running_threads[path]:
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()  # Ensure the observer thread exits cleanly
            del self.observers[path]
            del self.running_threads[path]

    def start(self, path):
        if path not in self.running_threads:  # Start monitoring if not already started
            threading.Thread(target=self.monitor_directory, args=(path,), daemon=True).start()

    def stop(self, path):
        if path in self.running_threads:  # Only stop if it is running
            self.running_threads[path] = False  # Signal to stop the thread

    def _log_event(self, message):
        self.text_widget.config(state=NORMAL)
        self.text_widget.insert(END, message + "\n")
        self.text_widget.see(END)
        self.text_widget.config(state=DISABLED)

def get_download_folder():
    return os.path.join(os.path.expanduser("~"), "Downloads")

def get_temp_folder():
    return os.path.join(os.environ.get("TEMP", "/tmp"))

def create_gui():
    root = Tk()
    root.title("AVS Monitor Essentials")
    
    root.resizable(False, False)

    label = Label(root, text="AVS Monitor Essentials")
    label.pack(pady=10)

    description = Label(root, text="Monitoring your Downloads and Temp folders.")
    description.pack(pady=5)

    text_widget = Text(root, wrap='word', height=20, width=60)
    text_widget.pack(padx=10, pady=10)
    text_widget.config(state=DISABLED)

    monitor = DirectoryMonitor(text_widget)

    # State flags for monitoring
    downloads_monitoring = False
    temp_monitoring = False

    def toggle_downloads_monitoring():
        nonlocal downloads_monitoring
        
        if downloads_monitoring:
            monitor.stop(get_download_folder())
            downloads_monitoring = False
            downloads_button.config(text="Start Monitoring Downloads")
            text_widget.config(state=NORMAL)
            text_widget.insert(END, "Downloads monitoring stopped.\n")
            text_widget.config(state=DISABLED)
        else:
            text_widget.config(state=NORMAL)
            text_widget.delete(1.0, END)  # Clear the text box
            monitor.start(get_download_folder())
            downloads_monitoring = True
            downloads_button.config(text="Stop Monitoring Downloads")
            text_widget.insert(END, "Downloads monitoring started...\n")
            text_widget.config(state=DISABLED)

    def toggle_temp_monitoring():
        nonlocal temp_monitoring
        
        if temp_monitoring:
            monitor.stop(get_temp_folder())
            temp_monitoring = False
            temp_button.config(text="Start Monitoring Temp")
            text_widget.config(state=NORMAL)
            text_widget.insert(END, "Temp monitoring stopped.\n")
            text_widget.config(state=DISABLED)
        else:
            text_widget.config(state=NORMAL)
            text_widget.delete(1.0, END)  # Clear the text box
            monitor.start(get_temp_folder())
            temp_monitoring = True
            temp_button.config(text="Stop Monitoring Temp")
            text_widget.insert(END, "Temp monitoring started...\n")
            text_widget.config(state=DISABLED)

    downloads_button = Button(root, text="Start Monitoring Downloads", command=toggle_downloads_monitoring)
    downloads_button.pack(pady=5)

    temp_button = Button(root, text="Start Monitoring Temp", command=toggle_temp_monitoring)
    temp_button.pack(pady=5)

    stop_button = Button(root, text="Exit", command=root.quit)
    stop_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
