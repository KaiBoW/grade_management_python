from app import db

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    full_score = db.Column(db.Integer, default=100)
    
    scores = db.relationship('Score', backref='subject', lazy='dynamic') 