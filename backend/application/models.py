"""Data models."""
from . import db

class Task(db.Model):
    """Data model for tasks."""
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64), index=False, unique=True, nullable=False)
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    active = db.Column(db.Boolean, index=False, unique=False, default=False)

    def __init__(self, description, created, active):
        self.description = description
        self.created = created
        self.active = active

    def __repr__(self):
        return self.description
