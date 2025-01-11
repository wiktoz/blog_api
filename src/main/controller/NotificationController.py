from flask import jsonify, Blueprint, request
from src.main.db.models import Notification
from src.main.extensions import db
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

# notification read, input: notification_id, boolean POST
@notification_bp.route('/read', methods=['POST'])
@jwt_required()
def read_notification():
    notification_id = request.json.get('notification_id')
    viewed = request.json.get('viewed')
    identity = get_jwt_identity()
    notification = Notification.query.filter_by(notification_id=notification_id).first()
    if notification == None:
        return jsonify({"message":"No such notification"}), 404
    if str(notification.user_id) != str(identity):
        return jsonify({"message":"No permission"}), 403
    notification.viewed = viewed
    db.session.commit()
    return jsonify({"message":"Notification read"}), 200
