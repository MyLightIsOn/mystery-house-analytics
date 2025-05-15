from database import db

class PuzzleLog(db.Model):
    __tablename__ = 'puzzle_logs'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String, nullable=False)
    puzzle_id = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)
    attempt_number = db.Column(db.Integer, nullable=False)
    device_type = db.Column(db.String, default="unknown")
