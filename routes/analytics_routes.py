from flask import Blueprint, jsonify
from models import PuzzleLog
from database import db
from sqlalchemy import func

# Define a Blueprint for the analytics routes
analytics_bp = Blueprint("analytics", __name__)


# Route to fetch overall analytics for puzzle sessions
@analytics_bp.route("/analytics", methods=["GET"])
def get_analytics():
    try:
        # Calculate the total number of unique sessions
        total_sessions = db.session.query(
            func.count(func.distinct(PuzzleLog.session_id))
        ).scalar()

        # Query puzzle analytics: total completions, average duration, maximum attempts
        rows = db.session.query(
            PuzzleLog.puzzle_id,
            func.count().label("completions"),
            func.avg(PuzzleLog.duration_seconds).label("avg_duration"),
            func.max(PuzzleLog.attempt_number).label("max_attempts")
        ).group_by(PuzzleLog.puzzle_id).order_by(PuzzleLog.puzzle_id).all()

        # Format the query results into a JSON-compatible structure
        puzzle_stats = [
            {
                "puzzle_id": row.puzzle_id,
                "completions": row.completions,
                "avg_duration_seconds": int(row.avg_duration),
                "max_attempts_by_any_session": row.max_attempts
            }
            for row in rows
        ]

        # Return the analytics as a JSON response
        return jsonify({
            "total_sessions": total_sessions,
            "puzzles": puzzle_stats
        }), 200
    except Exception as e:
        # Catch and return any errors that occur
        return jsonify({"error": str(e)}), 500


# Route to fetch time statistics by attempt for each puzzle
@analytics_bp.route("/analytics/time-by-attempt", methods=["GET"])
def time_by_attempt():
    try:
        # Query for the average duration grouped by puzzle and attempt number
        results = db.session.query(
            PuzzleLog.puzzle_id,
            PuzzleLog.attempt_number,
            func.avg(PuzzleLog.duration_seconds).label("avg_duration")
        ).group_by(PuzzleLog.puzzle_id, PuzzleLog.attempt_number
                   ).order_by(PuzzleLog.puzzle_id, PuzzleLog.attempt_number).all()

        # Organize query results as a dictionary where each puzzle has a list of attempts with stats
        stats = {}
        for puzzle_id, attempt_number, avg_duration in results:
            if puzzle_id not in stats:
                stats[puzzle_id] = []
            stats[puzzle_id].append({
                "attempt_number": attempt_number,
                "avg_duration_seconds": int(avg_duration)
            })

        # Return the time-by-attempt analytics as a JSON response
        return jsonify(stats), 200
    except Exception as e:
        # Catch and return any errors that occur
        return jsonify({"error": str(e)}), 500


