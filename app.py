from flask import Flask, request, jsonify
import csv
import os
from datetime import datetime
from flask_cors import CORS

# Create a Flask app instance
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# CSV file to store puzzle logs
CSV_FILE = 'puzzle_log.csv'

# Define the column names for the CSV file
FIELDNAMES = [
    'session_id',  # Unique identifier for the user's session
    'puzzle_id',  # Unique identifier for the puzzle
    'start_time',  # Timestamp when the puzzle was started
    'end_time',  # Timestamp when the puzzle was completed
    'duration_seconds',  # Duration spent on the puzzle (in seconds)
    'attempt_number'  # Number of times the user attempted the puzzle
]


def get_existing_attempts(session_id, puzzle_id):
    """
    Calculate the number of times a puzzle has been attempted by a specific session.

    Args:
        session_id (str): The session ID of the user.
        puzzle_id (str): The ID of the puzzle.

    Returns:
        int: The number of attempts for the given session and puzzle.
    """
    # Check if the CSV file exists; if not, return 0 attempts
    if not os.path.exists(CSV_FILE):
        return 0

    # Open the CSV file and count matching rows based on session_id and puzzle_id
    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return sum(1 for row in reader if row['session_id'] == session_id and row['puzzle_id'] == puzzle_id)


@app.route('/log', methods=['POST'])
def log_puzzle():
    """
    Log puzzle completion details from a POST request.

    The JSON payload should include:
        - session_id: The session ID of the user.
        - puzzle_id: The ID of the puzzle.
        - start_time: The ISO8601 timestamp when the puzzle started.
        - end_time: The ISO8601 timestamp when the puzzle ended.

    Returns:
        - 200 OK if the log is saved successfully.
        - 400 Bad Request if required fields are missing.
        - 500 Internal Server Error for unexpected errors.
    """
    # Retrieve the JSON data from the POST request
    data = request.get_json()

    # Set of required fields that must be present in the JSON payload
    required_fields = {'session_id', 'puzzle_id', 'start_time', 'end_time'}

    # Validate if all required fields are present
    if not data or not required_fields.issubset(data.keys()):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Parse start and end times from the JSON data
        start = datetime.fromisoformat(data['start_time'].replace('Z', ''))
        end = datetime.fromisoformat(data['end_time'].replace('Z', ''))

        # Calculate the duration the user spent on the puzzle (in seconds)
        duration = int((end - start).total_seconds())

        # Get the number of previous attempts and calculate the current attempt number
        attempt = get_existing_attempts(data['session_id'], data['puzzle_id']) + 1

        # Prepare a row of data to be logged
        row = {
            'session_id': data['session_id'],
            'puzzle_id': data['puzzle_id'],
            'start_time': data['start_time'],
            'end_time': data['end_time'],
            'duration_seconds': duration,
            'attempt_number': attempt
        }

        # Check if the CSV file already exists
        file_exists = os.path.exists(CSV_FILE)

        # Open the CSV file in append mode and write the log entry
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            if not file_exists:
                # Write the header to the CSV file if it doesn't exist
                writer.writeheader()
            writer.writerow(row)

        # Return a success response with the logged attempt number
        return jsonify({'status': 'logged', 'attempt_number': attempt}), 200

    except Exception as e:
        # Handle unexpected errors and return a 500 response
        return jsonify({'error': str(e)}), 500


# Run the Flask app (in debug mode) when the script is executed directly
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # fallback for local dev
    app.run(host="0.0.0.0", port=port)

