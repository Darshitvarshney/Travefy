from flask import Blueprint, request, jsonify
from backend.model.sosmodel import EmergencyContact
from datetime import datetime
import requests

sos_bp = Blueprint('sos', __name__)

# Save one or multiple emergency contacts
@sos_bp.route('/get_contacts', methods=['POST'])
def get_contacts():
    try:
        data = request.get_json()
        contacts_data = data.get('contacts', [])

        if not contacts_data or not isinstance(contacts_data, list):
            return jsonify({
                "message": "A list of contacts is required",
                "status": 400,
                "data": ""
            }), 400

        saved_contacts = []
        for c in contacts_data:
            name = c.get('name', '').strip()
            phone = c.get('phone', '').strip()

            if not name or not phone:
                continue  # skip invalid entries

            contact = EmergencyContact(name=name, phone=phone)
            contact.save()

            saved_contacts.append({"name": contact.name, "phone": contact.phone})

        if not saved_contacts:
            return jsonify({
                "message": "No valid contacts were provided",
                "status": 400,
                "data": ""
            }), 400

        return jsonify({
            "message": "Contacts saved successfully",
            "status": 200,
            "data": saved_contacts
        }), 200

    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": 500,
            "data": ""
        }), 500

# Send SOS message with location to all contacts
@sos_bp.route('/sos', methods=['POST'])
def sos():
    try:
        data = request.get_json()
        lat = data.get("lat")
        lon = data.get("lon")

        if not lat or not lon:
            return jsonify({
                "message": "Latitude and Longitude are required",
                "status": 400,
                "data": ""
            }), 400

        contacts = EmergencyContact.objects()  # fetch all contacts
        if not contacts:
            return jsonify({
                "message": "No emergency contacts found",
                "status": 404,
                "data": ""
            }), 404

        results = []
        for contact in contacts:
            message = (
                f"🚨 Emergency! {contact.name} needs help.\n"
                f"Location: https://www.google.com/maps?q={lat},{lon}\n"
                f"Time: {datetime.utcnow().isoformat()} UTC"
            )

            url = "https://textbelt.com/text"
            payload = {
                'phone': contact.phone,
                'message': message,
                'key': 'textbelt'   # Replace with your API key
            }
            response = requests.post(url, data=payload)
            response_data = response.json()

            # Update contact with message status
            contact.update(
                message=message,
                result=str(response_data),
                status=response_data.get("success", False),
                sent_at=datetime.utcnow()
            )

            results.append({
                "phone_number": contact.phone,
                "name": contact.name,
                "response": response_data
            })

        return jsonify({
            "message": "SOS alerts sent successfully",
            "status": 200,
            "data": results
        }), 200

    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": 500,
            "data": ""
        }), 500
