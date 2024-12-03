from flask import jsonify, Blueprint
from src.main.db.models import Post
from flask_jwt_extended import jwt_required, get_jwt_identity

post_bp = Blueprint('post_bp', __name__, url_prefix='/api/posts')

@post_bp.route('/', methods=['GET'])
@jwt_required()
def get_posts():
    posts = Post.query.all()
    posts_list = [post.to_dict() for post in posts]
    if posts_list == None:
        return jsonify({"message":"No posts"}), 404
    return jsonify(posts_list), 200


@post_bp.route('/me', methods=['GET'])
@jwt_required()
def get_my_posts():
    identity = get_jwt_identity()
    posts = Post.query.filter_by(user_id=identity).all()
    if posts == None:
        return jsonify({"message":"No posts"}), 404
    posts_list = [post.to_dict() for post in posts]
    return jsonify(posts_list), 200


@post_bp.route('/<post_uuid>', methods=['GET'])
@jwt_required()
def get_post(post_uuid):
    post = Post.query.filter_by(post_id=post_uuid).first()
    if post != None:
        return jsonify(post.to_dict()), 200
    return jsonify({"message":"No such post"}), 404



