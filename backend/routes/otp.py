import random
import smtplib
from flask import Blueprint, request, jsonify
import re
from werkzeug.security import generate_password_hash, check_password_hash
from backend.model.otpmodel import OTPModel
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

otp_bp = Blueprint('otp', __name__) 

# Load env variables
load_dotenv()

@otp_bp.route('/otp_send', methods=['POST'])
def otp_send():
    try :
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({"message": "Email is required", "status": 400, "data": ""}), 400
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"message": "Invalid email format", "status": 400, "data": ""}), 400

        otp_code = str(random.randint(100000, 999999))

        sender_email = os.getenv("EMAIL_USER")
        sender_password = os.getenv("EMAIL_PASS")
        receiver_email = email

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            message = f"""From: Travefy Team <{sender_email}>
    To: {email}
    Subject: Your One-Time Password (OTP) for Travefy

    Hello,

    We received a request to generate an OTP for your Travefy account. 
    Your One-Time Password (OTP) is:

        {otp_code}

    Please use this OTP within the next 10 minutes. 
    If you did not request this, please ignore this email.

    Thank you,
    The Travefy Team
    """
            server.sendmail(sender_email, receiver_email, message)
            server.quit()

            hashed_otp = generate_password_hash(otp_code)
            expiry_time = datetime.utcnow() + timedelta(minutes=10)
            OTPModel.objects(email=receiver_email).delete()
            email_otp = OTPModel(email=receiver_email, otp=hashed_otp, expiry_time=expiry_time)
            email_otp.save()

            return jsonify({"message": "OTP sent successfully", "status": 200, "data": ""}), 200

        except Exception as e:
            return jsonify({"message": f"Failed to send OTP: {str(e)}", "status": 500, "data": ""}), 500
    except Exception as e:
        return jsonify({"message": "Error in sending OTP", "status": 500, "error": str(e)}), 500

@otp_bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    try:
        data = request.get_json()
        email = data.get('email')
        otp_input = data.get('otp')

        otp_record = OTPModel.objects(email=email).first()
        if not otp_record:
            return jsonify({"message": "No OTP request found", "status": 404, "data": ""}), 404

        # Check expiry
        if datetime.utcnow() > otp_record.expiry_time:
            return jsonify({"message": "OTP expired", "status": 400, "data": ""}), 400

        # Check OTP
        if check_password_hash(otp_record.otp, otp_input):
            return jsonify({"message": "OTP verified successfully", "status": 200, "data": ""}), 200
        else:
            return jsonify({"message": "Invalid OTP", "status": 400, "data": ""}), 400
    except Exception as e:
        return jsonify({"message": "Error in verifying OTP", "status": 500, "error": str(e)}), 500