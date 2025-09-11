from flask import Flask, jsonify
from flask_cors import CORS
from mongoengine import connect
from dotenv import load_dotenv
import os

from backend.routes.User import User_bp
from backend.routes.otp import otp_bp
from backend.routes.chatbot import chatbot_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

# Use env variable
mongo_uri = os.getenv("MONGO_URI")
connect(host=mongo_uri)

app.register_blueprint(User_bp, url_prefix="/api/User")
app.register_blueprint(otp_bp, url_prefix="/api/otp")
app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")

@app.route("/api/health", methods=["GET"])
def index():
    return jsonify({"message": "Backend Running Successfully!!!", "status": 200, "data": ""}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5050, use_reloader=True)
