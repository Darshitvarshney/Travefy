from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import re 

from backend.model.Usermodel import User
User_bp = Blueprint('User', __name__)
@User_bp.route('/register', methods=['POST'])
def register_User():
    data = request.get_json()
    email = data.get('email')

    password = data.get('password')
    local_of = data.get('local_of')
    if not email or not password:
        return jsonify({"message": "Email and password are required", "status": 400, "data": ""}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"message": "Invalid email format", "status": 400, "data": ""}), 400

    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters long", "status": 400, "data": ""}), 400

    if User.objects(email=email).first():
        return jsonify({"message": "Email already registered", "status": 400, "data": ""}), 400

    hashed_password = generate_password_hash(password)
    new_User = User(email=email, password=hashed_password, local_of=local_of)
    new_User.save()

    return jsonify({"message": "User registered successfully", "status": 201, "data": ""}), 201

