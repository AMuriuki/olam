from app import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    