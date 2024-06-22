from .. import db

class GroupPreferencies(db.Model):
    __tablename__ = 'group_preferencies'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    preference_order = db.Column(db.Integer, nullable=False)
    last_update = db.Column(db.Date, nullable=False)

    groups = db.relationship('group', backref=db.backref('preferences_groupe', lazy=True))
    projects = db.relationship('project', backref=db.backref('preferences_groupe', lazy=True))
    def __repr__(self):
        return f'<GroupPreferencies {self.group_id, self.project_id, self.preference_order, self.last_update}>'