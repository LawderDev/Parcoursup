from ..models.user import User
from .. import db

def get_user_by_id(user_id):
    return User.query.get(user_id)

def create_user(username, email):
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    return new_user