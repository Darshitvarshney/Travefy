from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import re 

from backend.model.Usermodel import User,Log,Curr_log
from backend.model.consentmodel import location
from backend.utils.token import generate_token, token_user_required
from datetime import datetime

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
@token_user_required
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
    
@User_bp.route('Log_Page', methods=['POST'])
def Log_Page():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        user = User.objects(id=user_id).first()
        user.log.append(Log(curr_log=[]))
        user.save()
        return jsonify({"message": "Travel log Created successfully", "status": 200, "data": ""}), 200
    except Exception as e:
        return jsonify({"message": "Error in making travel log", "status": 500, "error": str(e)}), 500



@User_bp.route('/Travel_Log', methods=['POST'])
def Travel_Log():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        place = data.get('place')
        mode_of_travel = data.get('mode_of_travel')
        rating = data.get('rating')
        review = data.get('review')
        photos = data.get('photos', [])
        expense = data.get('expense')
        time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        date = data.get('date')

        if not user_id or not place:
            return jsonify({
                "message": "User ID, place, and rating are required",
                "status": 400,
                "data": ""
            }), 400


        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({"message": "User not found", "status": 404, "data": ""}), 404

        new_log_entry = {
            "place": place,
            "rating": rating,
            "review": review,
            "photos": photos,
            "expense": expense,
            "time": time,
            "mode_of_tavel": mode_of_travel,
            "date": date
        }

        if not user.log:
            user.log.append(Log(curr_log=[]))

        current_log = user.log[-1]

        if not current_log.curr_log:
            current_log.curr_log = []

        current_log.curr_log.append(Curr_log(**new_log_entry))

        user.save()


        return jsonify({"message": "Travel log updated successfully", "status": 200, "data": ""}), 200
    except Exception as e:
        return jsonify({"message": "Error in updating travel log", "status": 500, "error": str(e)}), 500
    

@User_bp.route('/User_Existence', methods=['GET'])
def User_Existence():
    try:
        data = request.get_json()
        email = data.get('email')
        if not email:
            return jsonify({"message": "Email parameter is required", "status": 400, "data": ""}), 400

        user = User.objects(email=email).first()
        if user:
            return jsonify({
            "message": "User Exist",
            "status": 200,
            "data": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email
            }
        }), 200
        else:
            return jsonify({"message": "User does not exist", "status": 404, "data": {"exists": False}}), 404
    except Exception as e:
        return jsonify({"message": "Error in checking user existence", "status": 500, "error": str(e)}), 500
    

    
@User_bp.route('/Password_Change', methods=['PUT'])
def Password_Change():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not user_id or not new_password or not confirm_password:
            return jsonify({
                "message": "user_id, new_password, and confirm_password are required",
                "status": 400,
                "data": ""
            }), 400

        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({"message": "User not found", "status": 404, "data": ""}), 404

        if new_password != confirm_password:
            return jsonify({
                "message": "New password and confirm password do not match",
                "status": 400,
                "data": ""
            }), 400

    
        if check_password_hash(user.password, new_password):
            return jsonify({
                "message": "New password cannot be the same as the old password",
                "status": 400,
                "data": ""
            }), 400

        if len(new_password) < 6:
            return jsonify({
                "message": "New password must be at least 6 characters long",
                "status": 400,
                "data": ""
            }), 400

        user.password = generate_password_hash(new_password)
        user.save()

        return jsonify({
            "message": "Password changed successfully",
            "status": 200,
            "data": ""
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Error in changing password",
            "status": 500,
            "error": str(e)
        }), 500
    ############################################################
@User_bp.route('/Get_Travel_Log', methods=['GET'])
def Get_Travel_Log():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"message": "User ID is required", "status": 400, "data": ""}), 400

        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({"message": "User not found", "status": 404, "data": ""}), 404

        travel_logs = []
        for log in user.log:
            log_entries = []
            for entry in log.curr_log:
                log_entries.append({
                    "place": entry.place,
                    "rating": entry.rating,
                    "review": entry.review,
                    "photos": entry.photos,
                    "expense": entry.expense,
                    "time": entry.time,
                    "mode_of_travel": entry.mode_of_travel  
                })
            travel_logs.append({
                "log_id": str(log.id),
                "curr_log": log_entries
            })

        return jsonify({
            "message": "Travel logs retrieved successfully",
            "status": 200,
            "data": travel_logs
        }), 200

    except Exception as e:
        return jsonify({"message": "Error in retrieving travel logs", "status": 500, "error": str(e)}), 500
