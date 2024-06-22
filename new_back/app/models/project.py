from .. import db

class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    nb_min_student = db.Column(db.Integer, nullable=False)
    nb_max_student = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Project {self.name}>'