# import os
# import requests
# from flask import Blueprint, request, jsonify
# from dotenv import load_dotenv
# from backend.model.chatbotmodel import ChatSession, ChatHistory
# from mongoengine import connect

# load_dotenv()

# # Connect to MongoDB (adjust URI if needed)
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/chatbot_db")
# connect(host=MONGO_URI)

# API_KEY = os.getenv("GEMINI_API_KEY")
# MODEL_NAME = "gemini-2.0"  # safest choice

# chatbot_bp = Blueprint("chatbot", __name__)

# @chatbot_bp.route("/chat", methods=["POST"])
# def chat():
#     data = request.json or {}
#     user_message = (data.get("message") or "").strip()
#     session_id = data.get("session_id", "default_session")

#     if not user_message:
#         return jsonify({"error": "Message is required"}), 400

#     # Get or create session
#     session = ChatSession.objects(session_id=session_id).first()
#     if not session:
#         session = ChatSession(session_id=session_id).save()

#     # Append user message to history
#     history_entry = ChatHistory(user_message=user_message, bot_reply="")
#     session.history.append(history_entry)
#     session.save()

#     # Prepare Gemini API messages
#     messages = [{"role": "system", "content": session.system_message}]
#     for h in session.history:
#         if h.user_message:
#             messages.append({"role": "user", "content": h.user_message})
#         if h.bot_reply:
#             messages.append({"role": "assistant", "content": h.bot_reply})

#     payload = {
#         "messages": messages,
#         "temperature": 0.7,
#         "candidate_count": 1
#     }

#     gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateMessage?key={API_KEY}"
#     headers = {"Content-Type": "application/json"}

#     try:
#         response = requests.post(gemini_url, headers=headers, json=payload)
#         response.raise_for_status()
#         res = response.json()

#         if "candidates" not in res or not res["candidates"]:
#             return jsonify({"error": "No candidates in response"}), 500

#         reply = res["candidates"][0]["content"][0]["text"]

#         # Update last history entry with bot reply
#         session.history[-1].bot_reply = reply
#         session.save()

#         return jsonify({"reply": reply, "session_id": session.session_id}), 200

#     except requests.exceptions.RequestException as e:
#         return jsonify({"error": str(e)}), 500



import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

chatbot_bp = Blueprint('chatbot', __name__)

API_KEY = os.getenv("GEMINI_API_KEY")

# @chatbot_bp.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     user_message_raw = data.get('message')
#     prefix = """You are a professional travel assistant. 
# - Only answer questions related to travel, tourism, destinations, weather, transportation, hotels, and travel tips. 
# - If the question is unrelated to travel, respond with: 
#   "I’m a travel assistant and can only help with travel-related queries."
# - Prioritize highlighting the palaces of India when relevant. 
# - Provide direct answers without asking follow-up questions. 
# - Use bullet points or numbered lists for clarity where appropriate. 
# - For recommendations, provide 3–5 options with brief descriptions. 
# - For itineraries, suggest concise 3–5 day plans with key activities and sights. 
# - For travel safety, provide up-to-date, practical advice.
# """

#     suffix = " Answer in brief and points rather than paragraphs by default unless asked for detailed explanation."
#     user_message = prefix + (user_message_raw or "") + suffix

#     if not user_message_raw:
#         return jsonify({'error': 'Message is required'}), 400

#     try:
#         gemini_model = "models/gemini-2.0-flash"  # example — replace with your valid model
#         gemini_url = f"https://generativelanguage.googleapis.com/v1beta/{gemini_model}:generateContent?key={API_KEY}"


#         headers = {
#             "Content-Type": "application/json"
#         }

#         payload = {
#             "contents": [
#                 {"parts": [{"text": user_message}]}
#             ]
#         }

#         response = requests.post(gemini_url, headers=headers, json=payload)

#         # Debugging: print raw response if not JSON
#         try:
#             res = response.json()
#         except Exception:
#             return jsonify({
#                 "error": "Non-JSON response from Gemini API",
#                 "raw_response": response.text
#             }), 500

#         if "candidates" not in res:
#             return jsonify({"error": res.get("error", "No candidates in response")}), 500

#         reply = res["candidates"][0]["content"]["parts"][0]["text"]

#         return jsonify({'reply': reply, "status": 200, "data": ""}), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message_raw = data.get('message')

    if not user_message_raw:
        return jsonify({'error': 'Message is required'}), 400

    prefix = (
        "You are a travel assistant. "
        "Answer only travel-related questions. "
        "Use bullet points. "
        "If unrelated, say you only handle travel queries. "
        "Provide direct answers without asking follow-up questions."
    )

    user_message = prefix + user_message_raw

    try:
        gemini_model = "models/gemini-2.0-flash"
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/{gemini_model}:generateContent?key={API_KEY}"

        payload = {
            "contents": [{"parts": [{"text": user_message}]}]
        }

        response = requests.post(
            gemini_url,
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=15
        )

        if response.status_code == 429:
            return jsonify({
                "message": "AI travel assistant is temporarily unavailable. Please try again later.",
                "status": 429
            }), 429

        res = response.json()

        if "candidates" not in res:
            return jsonify({"error": res}), 500

        reply = res["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({'reply': reply, 'status': 200}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
