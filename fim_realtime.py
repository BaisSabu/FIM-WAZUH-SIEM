import hashlib
import os
import json
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Files
BASELINE_FILE = "baseline.json"
LOG_FILE = "fim.log"

# Configure logging (Wazuh-friendly format)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Calculate file hash
def calculate_hash(file_path):
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except:
        return None

# Load baseline
def load_baseline():
    if not os.path.exists(BASELINE_FILE):
        return {}
    with open(BASELINE_FILE, "r") as f:
        return json.load(f)

# Save baseline
def save_baseline(data):
    with open(BASELINE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# FIM Event Handler
class FIMHandler(FileSystemEventHandler):

    def __init__(self, baseline):
        self.baseline = baseline

    def on_created(self, event):
        if not event.is_directory:
            file_hash = calculate_hash(event.src_path)
            print(f"[+] New file detected: {event.src_path}")
            logging.info(f"CREATED file={event.src_path}")
            self.baseline[event.src_path] = file_hash
            save_baseline(self.baseline)

    def on_modified(self, event):
        if not event.is_directory:
            new_hash = calculate_hash(event.src_path)
            old_hash = self.baseline.get(event.src_path)

            if old_hash and new_hash != old_hash:
                print(f"[!] File modified: {event.src_path}")
                logging.warning(f"MODIFIED file={event.src_path}")

            self.baseline[event.src_path] = new_hash
            save_baseline(self.baseline)

    def on_deleted(self, event):
        if not event.is_directory:
            if event.src_path in self.baseline:
                print(f"[-] File deleted: {event.src_path}")
                logging.error(f"DELETED file={event.src_path}")
                del self.baseline[event.src_path]
                save_baseline(self.baseline)

# Main
if __name__ == "__main__":
    path = input("Enter directory to monitor: ")

    if not os.path.exists(path):
        print("Invalid directory!")
        exit()

    baseline = load_baseline()

    # Create baseline if not exists
    if not baseline:
        print("[*] Creating baseline...")
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                baseline[file_path] = calculate_hash(file_path)
        save_baseline(baseline)
        print("[*] Baseline created.")

    print("[*] Real-time FIM started...")

    event_handler = FIMHandler(baseline)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
