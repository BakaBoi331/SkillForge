from . import db #Importing from current package - the db object created in __init__.py
from datetime import datetime, timezone

class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    current_level = db.Column(db.Integer, default=1, nullable=False)
    total_xp = db.Column(db.Integer, default=0, nullable=False)
    
    # cascade="all, delete-orphan" means if a skill is deleted, the database automatically cleans up all associated sessions.
    sessions = db.relationship('Session', backref='skill', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<Skill {self.name} - Lvl {self.current_level}>"

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    logged_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<Session {self.duration_minutes}m for Skill ID {self.skill_id}>"