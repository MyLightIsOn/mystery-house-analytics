from database import db

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    experience = db.Column(db.Text, nullable=False)
    learned = db.Column(db.Integer, nullable=False)
    favorite = db.Column(db.Text, nullable=False)
    more_games = db.Column(db.Text, nullable=False)
    session_id = db.Column(db.String, default="unknown")
