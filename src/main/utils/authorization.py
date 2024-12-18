from src.main.db.models import User, Group

def check_group_permission(user_id, group_id):
    user = User.query.filter_by(user_id=user_id).first()
    group = Group.query.filter_by(group_id=group_id).first()
    if user in group.users:
        return True
    return False