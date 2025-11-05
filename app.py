from flask import Flask, render_template_string
import os
from datetime import datetime

LOG_FILE = 'security.log'

app = Flask(__name__)

# HTML template langsung di dalam kode (biar simpel)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>File Integrity Monitor</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f2f2f2; color: #333; }
        h1 { color: #004aad; text-align: center; }
        table { margin: 20px auto; border-collapse: collapse; width: 80%; background: white; }
        th, td { padding: 10px; border: 1px solid #ccc; text-align: left; }
        th { background: #004aad; color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
        .info { color: green; font-weight: bold; }
        .warning { color: orange; font-weight: bold; }
        .alert { color: red; font-weight: bold; }
        .summary { text-align: center; margin: 20px; font-size: 1.1em; }
    </style>
</head>
<body>
    <h1>📁 File Integrity Monitoring Dashboard</h1>
    <div class="summary">
        <p>Total Jumlah File Aman: <span class="info">{{ safe_files }}</span></p>
        <p>Total Jumlah File Rusak: <span class="alert">{{ corrupted_files }}</span></p>
        <p>Waktu Terakhir Anomali: {{ last_anomaly if last_anomaly else 'Tidak ada' }}</p>
    </div>

    <table>
        <tr><th>Waktu</th><th>Level</th><th>Pesan</th><th>Nama File</th></tr>
        {% for log in logs %}
        <tr>
            <td>{{ log.time }}</td>
            <td class="{{ log.level|lower }}">{{ log.level }}</td>
            <td>{{ log.message }}</td>
            <td>{{ log.filename }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

def parse_logs():
    """Baca security.log dan ekstrak informasi."""
    if not os.path.exists(LOG_FILE):
        return [], 0, 0, None

    logs = []
    safe_files = 0
    corrupted_files = 0
    last_anomaly = None

    with open(LOG_FILE, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                timestamp = line.split(']')[0].strip('[')
                level = line.split(']')[1].split(':')[0].strip()
                message = line.split(':', 2)[2].split('"')[0].strip()
                filename = line.split('"')[1] if '"' in line else ""
                logs.append({
                    "time": timestamp,
                    "level": level,
                    "message": message,
                    "filename": filename
                })

                if level == "INFO" and "verified OK" in message:
                    safe_files += 1
                elif level in ("WARNING", "ALERT"):
                    corrupted_files += 1
                    last_anomaly = timestamp
            except Exception:
                continue

    return logs[::-1], safe_files, corrupted_files, last_anomaly

@app.route('/')
def index():
    logs, safe, corrupted, anomaly_time = parse_logs()
    return render_template_string(
        HTML_TEMPLATE,
        logs=logs,
        safe_files=safe,
        corrupted_files=corrupted,
        last_anomaly=anomaly_time
    )

if __name__ == '__main__':
    print("🌐 Web monitoring berjalan di http://127.0.0.1:5000/")
    app.run(debug=True)
