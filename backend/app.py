from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required
from log_generator import generate_multiple_logs
from auth import init_auth, login
from database import init_db, save_security_logs, get_logs_from_db, save_login_attempt
import random

app = Flask(__name__)
CORS(app)
init_auth(app)
init_db()  # Database initialize karo

@app.route('/api/login', methods=['POST'])
def login_route():
    username = request.json.get("username")
    result = login(request)
    # Login attempt database ma save karo
    status = "SUCCESS" if result[1] == 200 else "FAILED"
    save_login_attempt(username, status)
    return result

@app.route('/api/logs', methods=['GET'])
@jwt_required()
def get_logs():
    # Nava logs fetch karo ane database ma save karo
    new_logs = generate_multiple_logs(20)
    save_security_logs(new_logs)
    # Database ma thi return karo
    logs = get_logs_from_db()
    return jsonify(logs)

@app.route('/api/stats', methods=['GET'])
@jwt_required()
def get_stats():
    stats = {
        "total_events": random.randint(500, 1000),
        "critical_alerts": random.randint(5, 20),
        "blocked_ips": random.randint(10, 50),
        "active_threats": random.randint(1, 10)
    }
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)