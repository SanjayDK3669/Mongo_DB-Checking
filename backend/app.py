from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # Allow frontend access

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


# 🔗 MongoDB Connection (replace with your MongoDB URI)
client = MongoClient(MONGO_URI)  # or use your MongoDB Atlas URI
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route("/")
def home():
    return "MongoDB Contact Form Backend is Running!"

@app.route("/submit", methods=["POST"])
def submit_form():
    try:
        data = request.get_json()

        name = data.get("name")
        phone = data.get("phone")
        email = data.get("email")
        message = data.get("message")

        if not all([name, phone, email, message]):
            return jsonify({"error": "All fields are required"}), 400

        # Save to MongoDB
        contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "message": message
        }
        collection.insert_one(contact)

        return jsonify({"message": "Data saved successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
