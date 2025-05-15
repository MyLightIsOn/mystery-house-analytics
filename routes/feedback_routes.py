from flask import Blueprint, request, jsonify
from database import db
from models import Feedback

# Define a Blueprint for the feedback routes
feedback_bp = Blueprint("feedback", __name__)

@feedback_bp.route("/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()

    # Required fields from the frontend
    required_fields = {"experience", "learned", "favorite", "moreGames"}
    if not data or not required_fields.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Create a new Feedback entry using the model
        feedback = Feedback(
            experience=data["experience"],
            learned=int(data["learned"]),
            favorite=data["favorite"],
            more_games=data["moreGames"],
            session_id=data.get("session_id", "unknown")
        )

        # Save to the database
        db.session.add(feedback)
        db.session.commit()

        return jsonify({"status": "submitted"}), 200

    except Exception as e:
        # Roll back in case of error to avoid corrupt transactions
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
