from flask import Blueprint, request, jsonify
from app.services.friends_service import add_friend, get_friends, remove_friend
from flask_jwt_extended import jwt_required, get_jwt_identity

# 블루프린트 정의
bp = Blueprint('friends', __name__)

# 친구 추가 엔드포인트
@bp.route('/add', methods=['POST'])
@jwt_required()
def add():
    data = request.get_json()
    friend_username = data.get('username')

    if not friend_username:
        return jsonify({"message": "Friend's username is required"}), 400

    user_id = get_jwt_identity()
    # 친구 추가 서비스 호출
    success, message = add_friend(user_id, friend_username)
    if success:
        return jsonify({"message": "Friend added successfully"}), 201
    else:
        return jsonify({"message": message}), 400

# 친구 목록 조회 엔드포인트
@bp.route('/list', methods=['GET'])
@jwt_required()
def list_friends():
    user_id = get_jwt_identity()
    friends = get_friends(user_id)
    return jsonify([{
        "id": friend.id,
        "username": friend.username,
    } for friend in friends])

# 친구 삭제 엔드포인트
@bp.route('/remove', methods=['DELETE'])
@jwt_required()
def remove():
    data = request.get_json()
    friend_username = data.get('username')

    if not friend_username:
        return jsonify({"message": "Friend's username is required"}), 400

    user_id = get_jwt_identity()
    # 친구 삭제 서비스 호출
    success, message = remove_friend(user_id, friend_username)
    if success:
        return jsonify({"message": "Friend removed successfully"}), 200
    else:
        return jsonify({"message": message}), 400
