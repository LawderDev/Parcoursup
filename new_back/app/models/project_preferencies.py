from .. import db

class ProjectPreferencies(db.Model):
    __tablename__ = 'project_preferencies'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    preference_order = db.Column(db.Integer, nullable=False)
   
    projects = db.relationship('project', backref=db.backref('preferences_groupe', lazy=True))
    groups = db.relationship('group', backref=db.backref('preferences_groupe', lazy=True))
    def __repr__(self):
        return f'<ProjectPreferencies {self.project_id, self.group_id, self.preference_order}>'