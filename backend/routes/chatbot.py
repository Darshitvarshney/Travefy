# import requests
# from flask import Blueprint, request, jsonify
# from dotenv import load_dotenv
# import os

# load_dotenv()

# chatbot_bp = Blueprint('chatbot', __name__)

# API_KEY = os.getenv("GEMINI_API_KEY")

# @chatbot_bp.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     user_message_raw = data.get('message')
#     prefix = """You are a helpful **travel assistant**. 
#     - You only answer questions related to **travel, tourism, locations, weather, transportation, hotels, and travel tips**. 
#     - If the question is unrelated to travel, reply with : 
#     "I’m a travel assistant and can only help with travel-related queries." - Provide concise and relevant information.
#     - Priporitize the palaces of India 
#     - Don't ask questions from user just answer their ques straight away. 
#     - Use bullet points or numbered lists for clarity where appropriate. 
#     - If the user asks for recommendations, provide 3-5 options with brief descriptions. 
#     - If the user asks for travel itineraries, suggest a 3-5 day plan with key activities and sights. 
#     - If the user asks about travel safety, provide up-to-date tips and advice.
# """
#     suffix = " Answer in brief and points rather than paragraphs by deafault unless asked for detailed explanation."
#     user_message = prefix + user_message_raw + suffix


#     if not user_message:
#         return jsonify({'error': 'Message is required'}), 400

#     try:
#         gemini_model = "models/gemini-1.5-flash-8b"
#         gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={API_KEY}"

#         payload = {
#             "contents": [
#                 {"parts": [{"text": user_message}]}
#             ]
#         }

#         res = requests.post(gemini_url, json=payload).json()

#         if "candidates" not in res:
#             return jsonify({"error": res.get("error", "No candidates in response")}), 500

#         reply = res["candidates"][0]["content"]["parts"][0]["text"]

#         return jsonify({'reply': reply,"status":200,"data":""}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500



import requests
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

chatbot_bp = Blueprint('chatbot', __name__)

API_KEY = os.getenv("GEMINI_API_KEY")

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message_raw = data.get('message')
    prefix = """You are a professional travel assistant. 
- Only answer questions related to travel, tourism, destinations, weather, transportation, hotels, and travel tips. 
- If the question is unrelated to travel, respond with: 
  "I’m a travel assistant and can only help with travel-related queries."
- Prioritize highlighting the palaces of India when relevant. 
- Provide direct answers without asking follow-up questions. 
- Use bullet points or numbered lists for clarity where appropriate. 
- For recommendations, provide 3–5 options with brief descriptions. 
- For itineraries, suggest concise 3–5 day plans with key activities and sights. 
- For travel safety, provide up-to-date, practical advice.
"""

    suffix = " Answer in brief and points rather than paragraphs by default unless asked for detailed explanation."
    user_message = prefix + (user_message_raw or "") + suffix

    if not user_message_raw:
        return jsonify({'error': 'Message is required'}), 400

    try:
        gemini_model = "models/gemini-2.0-flash"  # example — replace with your valid model
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/{gemini_model}:generateContent?key={API_KEY}"


        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "contents": [
                {"parts": [{"text": user_message}]}
            ]
        }

        response = requests.post(gemini_url, headers=headers, json=payload)

        # Debugging: print raw response if not JSON
        try:
            res = response.json()
        except Exception:
            return jsonify({
                "error": "Non-JSON response from Gemini API",
                "raw_response": response.text
            }), 500

        if "candidates" not in res:
            return jsonify({"error": res.get("error", "No candidates in response")}), 500

        reply = res["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({'reply': reply, "status": 200, "data": ""}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
