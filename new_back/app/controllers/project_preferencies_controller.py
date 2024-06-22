from ..models.project_preferencies import ProjectPreferencies

def get_project_preferencies_by_project_id(project_id):
    return ProjectPreferencies.query.get(project_id)