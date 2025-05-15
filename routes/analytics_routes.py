from flask import Blueprint, jsonify
from models import PuzzleLog
from database import db
from sqlalchemy import func

# Define a Blueprint for the analytics routes
analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics", methods=["GET"])
def get_analytics():
    try:
        # Count distinct sessions
        total_sessions = db.session.query(
            func.count(func.distinct(PuzzleLog.session_id))
        ).scalar()

        # Grouped stats by puzzle_id: count, avg duration, max attempts
        rows = db.session.query(
            PuzzleLog.puzzle_id,
            func.count().label("completions"),
            func.avg(PuzzleLog.duration_seconds).label("avg_duration"),
            func.max(PuzzleLog.attempt_number).label("max_attempts")
        ).group_by(PuzzleLog.puzzle_id).order_by(PuzzleLog.puzzle_id).all()

        # Format results
        puzzle_stats = [
            {
                "puzzle_id": row.puzzle_id,
                "completions": row.completions,
                "avg_duration_seconds": int(row.avg_duration),
                "max_attempts_by_any_session": row.max_attempts
            }
            for row in rows
        ]

        return jsonify({
            "total_sessions": total_sessions,
            "puzzles": puzzle_stats
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
