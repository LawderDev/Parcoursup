from ..models.group_preferencies import GroupPreferencies

def get_group_preferencies_by_group_id(group_id):
    return GroupPreferencies.query.get(group_id)