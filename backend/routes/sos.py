from flask import Blueprint, request, jsonify
from backend.model.sosmodel import EmergencyContact
from datetime import datetime
import requests

sos_bp = Blueprint('sos', __name__)

# Save emergency contact
@sos_bp.route('/get_contacts', methods=['POST'])
def get_contacts():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()

        if not name or not phone:
            return jsonify({
                "message": "Name and phone are required",
                "status": 400,
                "data": ""
            }), 400

        contact = EmergencyContact(name=name, phone=phone)
        contact.save()

        return jsonify({
            "message": "Contact saved successfully",
            "status": 200,
            "data": {"name": contact.name, "phone": contact.phone}
        }), 200

    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": 500,
            "data": ""
        }), 500


# Send SOS message with location
@sos_bp.route('/sos', methods=['POST'])
def sos():
    try:
        data = request.get_json()
        lat = data.get("lat")
        lon = data.get("lon")

        emergency_contact = EmergencyContact.objects.first()
        if not emergency_contact:
            return jsonify({
                "message": "No emergency contact found",
                "status": 404,
                "data": ""
            }), 404

        if not lat or not lon:
            return jsonify({
                "message": "Latitude and Longitude are required",
                "status": 400,
                "data": ""
            }), 400

        message = (
            f"🚨 Emergency! {emergency_contact.name} needs help.\n"
            f"Location: https://www.google.com/maps?q={lat},{lon}\n"
            f"Time: {datetime.utcnow().isoformat()} UTC"
        )

        url = "https://textbelt.com/text"
        payload = {
            'phone': emergency_contact.phone,
            'message': message,
            'key': 'textbelt' 
        }
        response = requests.post(url, data=payload)
        response_data = response.json()

        emergency_contact.update(
            message=message,
            result=str(response_data),
            status=response_data.get("success", False),
            sent_at=datetime.utcnow()
        )

        return jsonify({
            "message": "SOS alert sent and saved successfully",
            "status": 200,
            "data": {
                "phone_number": emergency_contact.phone,
                "name": emergency_contact.name,
                "response": response_data
            }
        }), 200

    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": 500,
            "data": ""
        }), 500
