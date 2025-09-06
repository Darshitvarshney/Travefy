from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import re 

from backend.model.Usermodel import User
User_bp = Blueprint('User', __name__)
@User_bp.route('/register', methods=['POST'])
def register_User():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    local_of = data.get('local_of')
    if not email or not password or not name or not local_of:
        return jsonify({"message": "Fill All Entries", "status": 400, "data": ""}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"message": "Invalid email format", "status": 400, "data": ""}), 400

    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters long", "status": 400, "data": ""}), 400

    if User.objects(email=email).first():
        return jsonify({"message": "Email already registered", "status": 400, "data": ""}), 400

    hashed_password = generate_password_hash(password)
    new_User = User(name = name ,email=email, password=hashed_password, local_of=local_of)
    new_User.save()

    return jsonify({"message": "User registered successfully", "status": 201, "data": ""}), 201

@User_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required", "status": 400, "data": ""}), 400
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"message": "Invalid email format", "status": 400, "data": ""}), 400
    
    user = User.objects(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid email or password", "status": 401, "data": ""}), 401

    user_data = {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "local_of": user.local_of
    }

    return jsonify({"message": "Login successful", "status": 200, "data": user_data}), 200