from .. import db
from app.models.student_group import student_group

class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    students = db.relationship('Student', secondary=student_group, back_populates='group')
    def __repr__(self):
        return f'<Group {self.id}>'