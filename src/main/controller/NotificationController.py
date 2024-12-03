from flask import jsonify, Blueprint
from src.main.db.models import Notification
from flask_jwt_extended import jwt_required, get_jwt_identity

notification_bp = Blueprint('notification_bp', __name__, url_prefix='/api/notifications')


@notification_bp.route('/me', methods=['GET'])
@jwt_required()
def get_mine_notifications():
    identity = get_jwt_identity()
    notifications = Notification.query.filter_by(user_id=identity).all()
    if notifications == None:
        return jsonify({"message":"No notifications"}), 404
    notifications_list = [notification.to_dict() for notification in notifications]
    return jsonify(notifications_list), 200
