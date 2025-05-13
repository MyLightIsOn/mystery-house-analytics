from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load the database URL from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")


# Get a database connection
def get_connection():
    # Environment variable `ENV` can be set to 'production' or 'development'
    if os.getenv("ENV") == "production":
        # Production connection with sslmode
        return psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")
    else:
        # Local environment connection without sslmode
        return psycopg2.connect(os.getenv("DATABASE_URL"))


@app.route("/log", methods=["POST"])
def log_puzzle():
    data = request.get_json()  # Get JSON data from the POST request
    required = {"session_id", "puzzle_id", "start_time", "end_time"}

    # Check if the request contains required fields
    if not data or not required.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Parse start and end time and calculate duration
        start = datetime.fromisoformat(data["start_time"].replace("Z", ""))
        end = datetime.fromisoformat(data["end_time"].replace("Z", ""))
        duration = int((end - start).total_seconds())
        device_type = data.get("device_type", "unknown")  # Default to 'unknown' if not provided

        with get_connection() as conn:
            with conn.cursor() as cur:
                # Count previous attempts for the same session and puzzle
                cur.execute(
                    """
                    SELECT COUNT(*) FROM puzzle_logs
                    WHERE session_id = %s AND puzzle_id = %s
                    """,
                    (data["session_id"], data["puzzle_id"])
                )
                attempt_number = cur.fetchone()[0] + 1  # Increment attempt count

                # Insert the new log into the database
                cur.execute(
                    """
                    INSERT INTO puzzle_logs (
                        session_id, puzzle_id, start_time, end_time, duration_seconds, 
                        attempt_number, device_type
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        data["session_id"],
                        data["puzzle_id"],
                        start,
                        end,
                        duration,
                        attempt_number,
                        device_type
                    )
                )

        # Respond with success and the attempt number
        return jsonify({"status": "logged", "attempt_number": attempt_number}), 200

    except Exception as e:
        # Return error details if something fails
        return jsonify({"error": str(e)}), 500


@app.route("/analytics", methods=["GET"])
def get_analytics():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Calculate total distinct sessions (unique session IDs)
                cur.execute("SELECT COUNT(DISTINCT session_id) FROM puzzle_logs")
                total_sessions = cur.fetchone()[0]

                # Fetch details of puzzle completions, average duration, and max attempts
                cur.execute("""
                    SELECT
                        puzzle_id,
                        COUNT(*) AS completions,
                        AVG(duration_seconds)::INT AS avg_duration,
                        MAX(attempt_number) AS max_attempts
                    FROM puzzle_logs
                    GROUP BY puzzle_id
                    ORDER BY puzzle_id
                """)
                rows = cur.fetchall()

                # Format data into JSON
                puzzle_stats = [
                    {
                        "puzzle_id": row[0],
                        "completions": row[1],
                        "avg_duration_seconds": row[2],
                        "max_attempts_by_any_session": row[3]
                    }
                    for row in rows
                ]

                return jsonify({
                    "total_sessions": total_sessions,
                    "puzzles": puzzle_stats
                }), 200

    except Exception as e:
        # Return error details if something fails
        return jsonify({"error": str(e)}), 500


# Run the Flask app (in debug mode) when the script is executed directly
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # fallback for local dev
    app.run(host="0.0.0.0", port=port)