from ..models.project import Project

def get_project_id(project_id):
    return Project.query.get(project_id)