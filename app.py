from flask import Flask
import firebase_admin
from firebase_admin import firestore
from scraper import get_scraped_data

# Initialize Firebase app
cred = firebase_admin.credentials.Certificate("db.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

@app.route("/update_data", methods=["POST"])
def update_data():
    # Get data from request
    scraped_data = get_scraped_data()

    query = db.collection("news")

    try:
        for item in scraped_data:
            # Check if the item's "link" already exists in the collection
            existing_item = query.where("link", "==", item["link"]).get()

            if not existing_item:  # If no existing item found, add the new one
                db.collection("news").add(item)

        return "Data saved successfully", 200
    except Exception as e:
        # Log the error for better debugging
        print(f"Error saving data: {str(e)}")
        return "Error saving data", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)