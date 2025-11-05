import os
import hashlib
import json
import time
from datetime import datetime

# Folder yang akan dipantau
WATCH_FOLDER = './secure_files'
# File database hash dan log
HASH_DB = 'hash_db.json'
LOG_FILE = 'security.log'

# ====== Fungsi bantu ======
def get_file_hash(filepath):
    """Menghasilkan hash SHA256 dari sebuah file."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def log_event(level, message, filename=""):
    """Menulis log ke security.log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {level}: {message}"
    if filename:
        log_message += f' "{filename}"'
    print(log_message)  # simulasi alert ke konsol
    with open(LOG_FILE, 'a') as log:
        log.write(log_message + "\n")

def load_hash_db():
    """Membaca database hash dari file JSON."""
    if not os.path.exists(HASH_DB):
        return {}
    with open(HASH_DB, 'r') as f:
        return json.load(f)

def save_hash_db(db):
    """Menyimpan database hash ke file JSON."""
    with open(HASH_DB, 'w') as f:
        json.dump(db, f, indent=4)

# ====== Proses utama ======
def check_integrity():
    current_hashes = {}
    hash_db = load_hash_db()

    # Deteksi file baru & ubah hash
    for filename in os.listdir(WATCH_FOLDER):
        filepath = os.path.join(WATCH_FOLDER, filename)
        if os.path.isfile(filepath):
            file_hash = get_file_hash(filepath)
            current_hashes[filename] = file_hash

            if filename not in hash_db:
                log_event("ALERT", "Unknown file detected.", filename)
            elif hash_db[filename] != file_hash:
                log_event("WARNING", "File integrity failed!", filename)
            else:
                log_event("INFO", "File verified OK.", filename)

    # Deteksi file yang dihapus
    for filename in hash_db:
        if filename not in current_hashes:
            log_event("ALERT", "File deleted!", filename)

    # Simpan hash terbaru sebagai baseline
    save_hash_db(current_hashes)

# ====== Monitoring log ======
def monitor_log():
    """Membaca log dan menampilkan statistik kondisi terbaru."""
    if not os.path.exists(LOG_FILE):
        print("Belum ada log.")
        return

    # Ambil log dari eksekusi terakhir (berdasarkan timestamp terbaru di awal batch)
    with open(LOG_FILE, 'r') as log:
        lines = [line.strip() for line in log if line.strip()]

    # Ambil hanya log terakhir yang berdekatan waktunya (eksekusi terakhir)
    last_time = None
    recent_logs = []
    for line in reversed(lines):
        timestamp = line.split(']')[0].strip('[')
        if not last_time:
            last_time = timestamp
        if timestamp == last_time:
            recent_logs.insert(0, line)
        else:
            break

    # Hitung statistik dari batch terbaru
    safe_files = sum(1 for line in recent_logs if "INFO" in line and "verified OK" in line)
    corrupted_files = sum(1 for line in recent_logs if "WARNING" in line or "ALERT" in line)
    last_anomaly_time = None
    for line in reversed(lines):
        if "WARNING" in line or "ALERT" in line:
            last_anomaly_time = line.split(']')[0].strip('[')
            break

    print("\n=== Monitoring Summary ===")
    print(f"Jumlah file aman     : {safe_files}")
    print(f"Jumlah file rusak    : {corrupted_files}")
    print(f"Waktu terakhir anomali: {last_anomaly_time if last_anomaly_time else 'Tidak ada'}")
    print("==========================")

# ====== Main ======
if __name__ == "__main__":
    print("=== Sistem Deteksi Integritas File ===")
    check_integrity()
    monitor_log()
