import hashlib
import os
import time
import json

# -------------------------------
# FUNCTION: Generate file hash
# -------------------------------

def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    
    try:
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None


# -------------------------------
# FUNCTION: Load previous hashes
# -------------------------------

def load_hashes():
    if os.path.exists("file_hashes.json"):
        with open("file_hashes.json", "r") as f:
            return json.load(f)
    return {}


# -------------------------------
# FUNCTION: Save updated hashes
# -------------------------------

def save_hashes(hashes):
    with open("file_hashes.json", "w") as f:
        json.dump(hashes, f, indent=4)


# -------------------------------
# MAIN MONITOR FUNCTION
# -------------------------------

def monitor_files(folder_path):
    print(f"\n[+] Monitoring folder: {folder_path}")
    print("[+] Press CTRL + C to stop\n")

    previous_hashes = load_hashes()

    while True:
        current_hashes = {}

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = calculate_hash(file_path)

                if file_hash:
                    current_hashes[file_path] = file_hash

                    # Compare with previous hash
                    if file_path in previous_hashes:
                        if previous_hashes[file_path] != file_hash:
                            print(f"[!] ALERT: File Modified → {file_path}")
                    else:
                        print(f"[+] New File Added → {file_path}")

        # Check deleted files
        for old_file in previous_hashes:
            if old_file not in current_hashes:
                print(f"[!] ALERT: File Deleted → {old_file}")

        save_hashes(current_hashes)
        previous_hashes = current_hashes

        time.sleep(5)   # check every 5 seconds


# -------------------------------
# SCRIPT ENTRY POINT
# -------------------------------

if __name__ == "__main__":
    folder = input("Enter folder path to monitor: ")
    
    if os.path.exists(folder):
        monitor_files(folder)
    else:
        print("Invalid folder path!")
