from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import re 

from backend.model.Usermodel import User
from backend.model.consentmodel import location
from backend.utils.token import generate_token, token_user_required

User_bp = Blueprint('User', __name__)
@User_bp.route('/register', methods=['POST'])
def register_User():
    try :
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        local_of = data.get('local_of')
        DOB = data.get('DOB')
        phone = data.get('phone')
        gender = data.get('gender')


        if not email or not password or not name or not local_of or not DOB or not phone or not gender  :
            return jsonify({"message": "Fill All Entries", "status": 400, "data": ""}), 400

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"message": "Invalid email format", "status": 400, "data": ""}), 400

        if len(password) < 6:
            return jsonify({"message": "Password must be at least 6 characters long", "status": 400, "data": ""}), 400

        if User.objects(email=email).first():
            return jsonify({"message": "Email already registered", "status": 400, "data": ""}), 400

        hashed_password = generate_password_hash(password)
        new_User = User(name = name ,email=email, password=hashed_password, local_of=local_of, DOB=DOB, phone=phone,gender=gender)
        new_User.save()
        token = generate_token(new_User)
        return jsonify({
        "message": "Signup successful",
        "status": 200,
        "token": token,
        "data": {
            "id": str(new_User.id),
            "name": new_User.name,
            "email": new_User.email
        }
    }), 200
    except Exception as e:
        return jsonify({"message": "Error in Sign Up", "status": 500, "error": str(e)}), 500
@User_bp.route('/login', methods=['POST'])
def login():
    try:

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

        # user_data = {
        #     "id": str(user.id),
        #     "name": user.name,
        #     "email": user.email,
        #     "local_of": user.local_of
        # }

        token = generate_token(user)
        return jsonify({
            "message": "Login successful",
            "status": 200,
            "token": token,
            "data": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email
            }
        }), 200
    except Exception as e:
        return jsonify({"message": "Error in Login in", "status": 500, "error": str(e)}), 500


@User_bp.route('/location', methods=['POST'])
def consent_location():
    try:
        data = request.get_json()
        agreed = data.get('agreed')

        if agreed is None:
            return jsonify({"message": "Agreed field is required", "status": 400, "data": ""}), 400

        new_consent = location(agreed=agreed)
        new_consent.save()

        return jsonify({"message": "Location consent recorded", "status": 201, "data": ""}), 201
    except Exception as e:
        return jsonify({"message": "Error in recording consent", "status": 500, "error": str(e)}), 500
    
@User_bp.route('/Update_Profile', methods=['PUT'])
def Update_Profile():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        name = data.get('name')
        local_of = data.get('local_of')
        DOB = data.get('DOB')
        phone = data.get('phone')

        if not user_id:
            return jsonify({"message": "User ID is required", "status": 400, "data": ""}), 400

        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({"message": "User not found", "status": 404, "data": ""}), 404

        if name:
            user.name = name    
        if local_of:
            user.local_of = local_of    
        if DOB:
            user.DOB = DOB  
        if phone:
            user.phone = phone

        user.save()
        return jsonify({
            "message": "Profile updated successfully",
            "status": 200,
            "data": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "local_of": user.local_of,
                "DOB": user.DOB,
                "phone": user.phone,
                "gender": user.gender
            }
        }), 200
    except Exception as e:
        return jsonify({"message": "Error in updating profile", "status": 500, "error": str(e)}), 500
