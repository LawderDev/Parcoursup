from .. import db
from app.models.student_group import student_group

class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    groupes = db.relationship('Group', secondary=student_group, back_populates='student')
    def __repr__(self):
        return f'<User {self.firstname, self.lastname}>'