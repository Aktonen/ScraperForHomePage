from flask import Flask, request
import firebase_admin
from firebase_admin import firestore

# Initialize Firebase app
cred = firebase_admin.credentials.Certificate("db.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

@app.route("/get_data", methods=["GET"])
def get_data():
    try:
        # Get all documents from the "news" collection
        docs = db.collection("news").get()

        # Convert documents to a list of dictionaries
        data = [doc.to_dict() for doc in docs]

        return f"Retrieved data: {data}", 200
    except Exception as e:
        # Log the error for better debugging
        print(f"Error retrieving data: {str(e)}")
        return "Error retrieving data", 500

@app.route("/update_data", methods=["POST"])
def update_data():
    # Get data from request
    scraped_data = request.get_json()

    try:
        # Create a new document with the data
        db.collection("news").document().set(scraped_data)
        return "Data saved successfully", 200
    except Exception as e:
        # Log the error for better debugging
        print(f"Error saving data: {str(e)}")
        return "Error saving data", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)