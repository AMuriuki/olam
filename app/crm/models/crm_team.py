from app import db

class Team(db.Model):
    id = db.column(db.Integer, primary_key=True)
    