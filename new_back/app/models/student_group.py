from .. import db

class StudentGroup(db.Model):
    __tablename__ = 'student_group'

    student_id =db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    group_id = db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)

    def __repr__(self):
        return f'<StudentGroup {self.student_id, self.group_id}>'