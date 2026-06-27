import sqlite3
import datetime

def init_db():
    conn = sqlite3.connect('siem.db')
    cursor = conn.cursor()
    
    # Login attempts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL,
            ip_address TEXT
        )
    ''')
    
    # Security logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS security_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            event_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            location TEXT,
            port INTEGER,
            status TEXT,
            confidence INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()

def save_login_attempt(username, status, ip_address="unknown"):
    conn = sqlite3.connect('siem.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO login_attempts (username, timestamp, status, ip_address)
        VALUES (?, ?, ?, ?)
    ''', (username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status, ip_address))
    conn.commit()
    conn.close()

def save_security_logs(logs):
    conn = sqlite3.connect('siem.db')
    cursor = conn.cursor()
    for log in logs:
        cursor.execute('''
            INSERT INTO security_logs 
            (timestamp, ip_address, event_type, severity, location, port, status, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            log['timestamp'], log['ip_address'], log['event_type'],
            log['severity'], log['location'], log['port'],
            log['status'], log.get('confidence', 0)
        ))
    conn.commit()
    conn.close()

def get_logs_from_db():
    conn = sqlite3.connect('siem.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM security_logs ORDER BY id DESC LIMIT 20')
    rows = cursor.fetchall()
    conn.close()
    
    logs = []
    for row in rows:
        logs.append({
            "id": row[0],
            "timestamp": row[1],
            "ip_address": row[2],
            "event_type": row[3],
            "severity": row[4],
            "location": row[5],
            "port": row[6],
            "status": row[7],
            "confidence": row[8]
        })
    return logs

def get_login_history():
    conn = sqlite3.connect('siem.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM login_attempts ORDER BY id DESC LIMIT 10')
    rows = cursor.fetchall()
    conn.close()
    return rows