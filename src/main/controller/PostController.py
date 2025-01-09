from flask import jsonify, Blueprint, request
from src.main.db.models import Post, Rating, Comment, Photo, Notification
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.main.extensions import db
from src.main.utils.body_validator import check_data
from src.main.utils.authorization import check_group_permission

post_bp = Blueprint('post_bp', __name__, url_prefix='/api/posts')


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
    group = post.group_id
    if not check_group_permission(get_jwt_identity(), group):
        return jsonify({"message":"No permission"}), 403
    if post != None:
        return jsonify(post.to_dict()), 200
    return jsonify({"message":"No such post"}), 404

@post_bp.route('/<post_uuid>', methods=['DELETE'])
@jwt_required()
def delete_post(post_uuid):
    post = Post.query.filter_by(post_id=post_uuid).first()
    if post != None:
        if not check_group_permission(get_jwt_identity(), post.group_id):
            return jsonify({"message":"No permission. Invalid group"}), 403
        if str(post.user_id) != str(get_jwt_identity()):
            return jsonify({"message":"No permission. You are not the author!"}), 403
        comments = Comment.query.filter_by(post_id=post_uuid).all()
        if comments != None:
            for comment in comments:
                db.session.delete(comment)
        ratings = Rating.query.filter_by(post_id=post_uuid).all()
        if ratings != None:
            for rating in ratings:
                db.session.delete(rating)
        photos = Photo.query.filter_by(post_id=post_uuid).all()
        if photos != None:
            for photo in photos:
                db.session.delete(photo)
        notifications = Notification.query.filter_by(post_id=post_uuid).all()
        if notifications != None:
            for notification in notifications:
                db.session.delete(notification)
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message":"Post deleted"}), 200
    return jsonify({"message":"No such post"}), 404

@post_bp.route('/<post_uuid>/rate', methods=['GET'])
@jwt_required()
def calculate_average_rating(post_uuid):
    post = Post.query.filter_by(post_id=post_uuid).first()
    if post == None:
        return jsonify({"message":"No such post"}), 404
    if not check_group_permission(get_jwt_identity(), post.group_id):
        return jsonify({"message":"No permission"}), 403
    ratings = Rating.query.filter_by(post_id=post_uuid).all()
    if ratings == None:
        return jsonify({"message":"No ratings"}), 404
    total = 0
    for rating in ratings:
        total += rating.rating
    average = total / len(ratings)
    return jsonify({"average":average}), 200


@post_bp.route('/<post_uuid>/rate', methods=['POST'])
@jwt_required()
def rate_post(post_uuid):
    data = request.get_json()
    required_data = ['value']
    response = check_data(data, required_data)

    if not response:
        return jsonify({"message":"Missing data"}), 400
    # Check if rating is between 1 and 5
    value = data.get("value")
    if value < 1 or value > 5:
        return jsonify({"message":"Invalid rating"}), 400
    
    # Check if post exists
    post = Post.query.filter_by(post_id=post_uuid).first()
    if post == None:
        return jsonify({"message":"No such post"}), 404
    
    # Check if user has permission to rate the post
    user_id = get_jwt_identity()
    if not check_group_permission(user_id, post.group_id):
        return jsonify({"message":"No permission to rate this post"}), 403
    
    rating = Rating(rating=value, post_id=post_uuid, user_id=user_id)
    db.session.add(rating)
    db.session.commit()
    return jsonify({"message":"Rating added"}), 200

@post_bp.route('/<post_uuid>/rate', methods=['DELETE'])
@jwt_required()
def delete_rating(post_uuid):
    user_id = get_jwt_identity()
    post = Post.query.filter_by(post_id=post_uuid).first()
    # Check if post exists
    if post == None:
        return jsonify({"message":"No such post"}), 404
    
    # Check if user has permission to delete the rating
    if not check_group_permission(user_id, post.group_id):
        return jsonify({"message":"No permission to delete this rating"}), 403
    

    rating = Rating.query.filter_by(post_id=post_uuid, user_id=user_id).first()
    if rating != None:
        db.session.delete(rating)
        db.session.commit()
        return jsonify({"message":"Rating deleted"}), 200
    return jsonify({"message":"No such rating"}), 404

@post_bp.route('/<post_uuid>/comments', methods=['POST'])
@jwt_required()
def comment_post(post_uuid):
    post = Post.query.filter_by(post_id=post_uuid).first()
    user_id = get_jwt_identity()
    if post == None:
        return jsonify({"message":"No such post"}), 404
    if not check_group_permission(user_id, post.group_id):
        return jsonify({"message":"No permission to comment on this post"}), 403
    data = request.get_json()
    required_data = ['content']
    response = check_data(data, required_data)
    if not response:
        return jsonify({"message":"Missing data"}), 400
    content = data.get("content")
    comment = Comment(content=content, post_id=post_uuid, user_id=user_id)

    notification = Notification(user_id=post.user_id, content=f"Someone commented on your post {post.title}", post_id=post_uuid)
    db.session.add(notification)
    db.session.commit()
    comments = Comment.query.filter_by(post_id=post_uuid).all()
    if comments != None:
        for comment in comments:
            if comment.user_id != user_id:
                notification = Notification(user_id=comment.user_id, content=f"Someone commented on post {post.title}", post_id=post_uuid)
                db.session.add(notification)
                db.session.commit()
    db.session.add(comment)
    db.session.commit()
    return jsonify({"message":"Comment added"}), 200

@post_bp.route('/<post_uuid>/comments', methods=['GET'])
@jwt_required()
def get_comments(post_uuid):
    comments = Comment.query.filter_by(post_id=post_uuid).all()
    if comments == None:
        return jsonify({"message":"No comments"}), 404
    post = Post.query.filter_by(post_id=post_uuid).first()
    if post == None:
        return jsonify({"message":"No such post"}), 404
    if not check_group_permission(get_jwt_identity(), post.group_id):
        return jsonify({"message":"No permission"}), 403
    comments_list = [comment.to_dict() for comment in comments]
    return jsonify(comments_list), 200


@post_bp.route('/<post_uuid>/comments', methods=['DELETE'])
@jwt_required()
def delete_comment(post_uuid):
    data = request.get_json()
    required_data = ['comment_id']
    response = check_data(data, required_data)
    if not response:
        return jsonify({"message":"Missing data"}), 400
    comment_id = data.get("comment_id")
    comment = Comment.query.filter_by(comment_id=comment_id).first()
    if comment == None:
        return jsonify({"message":"No such comment"}), 404
    post = Post.query.filter_by(post_id=post_uuid).first()
    if post == None:
        return jsonify({"message":"No such post"}), 404
    if not check_group_permission(get_jwt_identity(), post.group_id):
        return jsonify({"message":"No permission"}), 403
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message":"Comment deleted"}), 200