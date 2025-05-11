from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

@app.route("/log", methods=["POST"])
def log_puzzle():
    data = request.get_json()
    required = {"session_id", "puzzle_id", "start_time", "end_time"}

    if not data or not required.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        start = datetime.fromisoformat(data["start_time"].replace("Z", ""))
        end = datetime.fromisoformat(data["end_time"].replace("Z", ""))
        duration = int((end - start).total_seconds())

        with get_connection() as conn:
            with conn.cursor() as cur:
                # Count previous attempts
                cur.execute(
                    """
                    SELECT COUNT(*) FROM puzzle_logs
                    WHERE session_id = %s AND puzzle_id = %s
                    """,
                    (data["session_id"], data["puzzle_id"])
                )
                attempt_number = cur.fetchone()[0] + 1

                # Insert new puzzle log
                cur.execute(
                    """
                    INSERT INTO puzzle_logs (
                        session_id, puzzle_id, start_time, end_time, duration_seconds, attempt_number
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        data["session_id"],
                        data["puzzle_id"],
                        start,
                        end,
                        duration,
                        attempt_number
                    )
                )

        return jsonify({"status": "logged", "attempt_number": attempt_number}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
