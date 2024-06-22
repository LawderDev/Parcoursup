from ..models.group import Group
from .. import db

def get_group_by_id(group_id):
    return Group.query.get(group_id)

def create_group():
    new_group = Group()
    db.session.add(new_group)
    db.session.commit()
    return new_group