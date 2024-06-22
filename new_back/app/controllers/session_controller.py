from ..models.session import Session

def get_session_by_id(session_id):
    return Session.query.get(session_id)