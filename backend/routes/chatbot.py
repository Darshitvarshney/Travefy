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
    prefix = """You are a helpful **travel assistant**. 
    - You only answer questions related to **travel, tourism, locations, weather, transportation, hotels, and travel tips**. 
    - If the question is unrelated to travel, reply with : 
    "I’m a travel assistant and can only help with travel-related queries." - Provide concise and relevant information.
    - Priporitize the palaces of India 
    - Don't ask questions from user just answer their ques straight away. 
    - Use bullet points or numbered lists for clarity where appropriate. 
    - If the user asks for recommendations, provide 3-5 options with brief descriptions. 
    - If the user asks for travel itineraries, suggest a 3-5 day plan with key activities and sights. 
    - If the user asks about travel safety, provide up-to-date tips and advice.
"""
    suffix = " Answer in brief and points rather than paragraphs by deafault unless asked for detailed explanation."
    user_message = prefix + user_message_raw + suffix


    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        gemini_model = "models/gemini-1.5-flash-8b-latest"
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/{gemini_model}:generateContent?key={API_KEY}"


        payload = {
            "contents": [
                {"parts": [{"text": user_message}]}
            ]
        }

        res = requests.post(gemini_url, json=payload).json()

        if "candidates" not in res:
            return jsonify({"error": res.get("error", "No candidates in response")}), 500

        reply = res["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({'reply': reply,"status":200,"data":""}), 200
    #     return jsonify({
    #     "message": "Chatbot response",
    #     "status": 200,
    #     "data": reply
    # }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
