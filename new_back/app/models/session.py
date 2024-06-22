from .. import db

class Session(db.Model):
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    deadline_group_creation = db.Column(db.Date, nullable=False)
    deadline_project_choice = db.Column(db.Date, nullable=False)
    nb_max_student = db.Column(db.Integer, nullable=False)
    nb_min_student = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(100), nullable=False)
    students = db.relationship('Student', backref='session', lazy=True)
    
    def __repr__(self):
        return f'<Session {self.id}>'