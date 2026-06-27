import random
import datetime
import requests
from faker import Faker

fake = Faker()
API_KEY = "504c3a01fa44b2508c910d2ad74625152ea1faa28359738b1692ec442f166b80500f62704ef9ff42"

def get_real_threats():
    try:
        url = "https://api.abuseipdb.com/api/v2/blacklist"
        headers = {
            "Key": API_KEY,
            "Accept": "application/json"
        }
        params = {
            "confidenceMinimum": 90,
            "limit": 20
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        logs = []
        for item in data["data"]:
            logs.append({
                "id": random.randint(1000, 9999),
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ip_address": item["ipAddress"],
                "event_type": get_attack_type(item["abuseConfidenceScore"]),
                "severity": get_severity(item["abuseConfidenceScore"]),
                "location": item.get("countryCode", "Unknown"),
                "port": random.randint(1, 9999),
                "status": "DETECTED",
                "confidence": item["abuseConfidenceScore"]
            })
        return logs
    except:
        return get_fake_logs()

def get_attack_type(score):
    if score >= 95:
        return "DDoS Attempt"
    elif score >= 90:
        return "Brute Force"
    else:
        return "Port Scan"

def get_severity(score):
    if score >= 95:
        return "CRITICAL"
    elif score >= 90:
        return "HIGH"
    else:
        return "MEDIUM"

def get_fake_logs():
    # Fallback - API fail thay to fake data
    attack_types = ["Failed Login", "Port Scan", "DDoS Attempt", "SQL Injection", "Brute Force"]
    severity_map = {
        "Failed Login": "MEDIUM",
        "Port Scan": "HIGH",
        "DDoS Attempt": "CRITICAL",
        "SQL Injection": "CRITICAL",
        "Brute Force": "HIGH"
    }
    event = random.choice(attack_types)
    return [{
        "id": random.randint(1000, 9999),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": fake.ipv4(),
        "event_type": event,
        "severity": severity_map[event],
        "location": fake.country(),
        "port": random.randint(1, 9999),
        "status": "DETECTED",
        "confidence": random.randint(80, 100)
    }]

def generate_multiple_logs(count=20):
    return get_real_threats()