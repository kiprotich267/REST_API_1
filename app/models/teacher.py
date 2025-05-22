from app.extension import db
from datetime import datetime, timezone

class TeacherModel(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))
    name = db.Column(db.String(120), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    hire_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    courses= db.relationship('CourseModel', backref='teacher', lazy=True)

    def __repr__(self):
        return f"{self.first_name} - {self.name}"