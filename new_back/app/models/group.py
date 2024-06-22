from .. import db
from .student_group import student_group

class Groupe(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    students = db.relationship('student', secondary=student_group, back_populates='group')
    def __repr__(self):
        return f'<Group {self.id}>'