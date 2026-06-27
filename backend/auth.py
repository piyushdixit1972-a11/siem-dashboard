from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import bcrypt

# Users dictionary (database vagar)
users = {
    "admin": bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
}

def init_auth(app):
    app.config["JWT_SECRET_KEY"] = "siem-secret-key-2026"
    jwt = JWTManager(app)
    return jwt

def login(request):
    username = request.json.get("username")
    password = request.json.get("password")
    
    if username in users:
        if bcrypt.checkpw(password.encode(), users[username]):
            token = create_access_token(identity=username)
            return jsonify({"token": token}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401