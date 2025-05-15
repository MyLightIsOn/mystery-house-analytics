from flask import Blueprint, request, jsonify
from datetime import datetime
from database import db
from models import PuzzleLog

# Define the Blueprint for this route group
log_bp = Blueprint("log", __name__)

@log_bp.route("/log", methods=["POST"])
def log_puzzle():
    data = request.get_json()

    # Validate required fields
    required = {"session_id", "puzzle_id", "start_time", "end_time"}
    if not data or not required.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Parse ISO timestamps and calculate puzzle duration
        start = datetime.fromisoformat(data["start_time"].replace("Z", ""))
        end = datetime.fromisoformat(data["end_time"].replace("Z", ""))
        duration = int((end - start).total_seconds())

        # Get optional device_type, default to "unknown"
        device_type = data.get("device_type", "unknown")

        # Count previous attempts by session and puzzle
        existing_attempts = PuzzleLog.query.filter_by(
            session_id=data["session_id"],
            puzzle_id=data["puzzle_id"]
        ).count()
        attempt_number = existing_attempts + 1

        # Create a new PuzzleLog instance
        log = PuzzleLog(
            session_id=data["session_id"],
            puzzle_id=data["puzzle_id"],
            start_time=start,
            end_time=end,
            duration_seconds=duration,
            attempt_number=attempt_number,
            device_type=device_type
        )

        # Save to the database
        db.session.add(log)
        db.session.commit()

        # Respond with success and attempt count
        return jsonify({"status": "logged", "attempt_number": attempt_number}), 200

    except Exception as e:
        # Roll back if something goes wrong
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
