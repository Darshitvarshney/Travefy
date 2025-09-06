import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from bson import ObjectId
import os
from backend.model.Usermodel import User
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS"))  


def generate_token(User):
    payload = {
        "_id": str(User.id),
        "email": User.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRY_HOURS)
    }
    print(payload)
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")




def token_user_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Token is missing", "status": 401}), 401
        try:
            token = auth_header.split(" ")[1] if " " in auth_header else auth_header
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            User = User.objects(id=data["_id"]).first()
            if not User:
                return jsonify({"message": "Admin not found", "status": 404}), 404
            request.User = User
        except Exception as e:
            return jsonify({"message": "Invalid or expired token", "status": 401, "error": str(e)}), 401
        return f(*args, **kwargs)
    return decorated




