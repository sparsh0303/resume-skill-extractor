from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    skills = db.Column(db.Text)  # Stored as comma-separated values
    experience = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'skills': self.skills.split(',') if self.skills else [],
            'experience': self.experience,
            'uploaded_at': self.uploaded_at.isoformat()
        }
