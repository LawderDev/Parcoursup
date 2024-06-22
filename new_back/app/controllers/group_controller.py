from ..models.group import Group
from .. import db

def get_user_by_id(user_id):
    return Group.query.get(user_id)

def create_group():
    new_group = Group()
    db.session.add(new_group)
    db.session.commit()
    return new_group