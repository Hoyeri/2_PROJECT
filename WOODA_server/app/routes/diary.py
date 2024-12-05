# diary.py
from flask import Blueprint, request, jsonify
from app.services.diary_service import (
    create_diary, get_diary_by_id, get_all_diaries_with_friends, update_diary, delete_diary
)
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity

# 블루프린트 정의
bp = Blueprint('diary', __name__)

# 일기 작성 엔드포인트
@bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    # 유효성 검사
    if not title or not content:
        return jsonify({"message": "Title and content are required"}), 400

    # 일기 생성 서비스 호출
    user_id = get_jwt_identity()  # JWT에서 사용자 ID 추출
    diary = create_diary(user_id=user_id, title=title, content=content)
    return jsonify({"message": "Diary created successfully", "diary_id": diary.id}), 201

# 모든 일기 조회 (자신과 친구의 일기 포함, 최신순 정렬)
@bp.route('/all', methods=['GET'])
@jwt_required()
def get_all():
    user_id = get_jwt_identity()
    diaries = get_all_diaries_with_friends(user_id=user_id)
    return jsonify([{
        "id": diary.id,
        "title": diary.title,
        "content": diary.content,
        "date_created": diary.date_created.strftime("%Y-%m-%d %H:%M:%S"),
        "author": diary.author.username  # 일기 작성자의 이름 포함
    } for diary in diaries])
    
# 특정 일기 조회 엔드포인트
@bp.route('/<int:diary_id>', methods=['GET'])
@jwt_required()
def get_diary(diary_id):
    user_id = get_jwt_identity()
    diary = get_diary_by_id(diary_id, user_id=user_id)
    if diary:
        return jsonify({
            "id": diary.id,
            "title": diary.title,
            "content": diary.content,
            "date_created": diary.date_created.strftime("%Y-%m-%d %H:%M:%S")
        })
    else:
        return jsonify({"message": "Diary not found"}), 404

# 일기 수정 엔드포인트
@bp.route('/update/<int:diary_id>', methods=['PUT'])
@jwt_required()
def update(diary_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    # 유효성 검사
    if not title or not content:
        return jsonify({"message": "Title and content are required"}), 400

    user_id = get_jwt_identity()
    updated_diary = update_diary(diary_id, user_id=user_id, title=title, content=content)
    if updated_diary:
        return jsonify({"message": "Diary updated successfully"})
    else:
        return jsonify({"message": "Diary not found or unauthorized"}), 404

# 일기 삭제 엔드포인트
@bp.route('/delete/<int:diary_id>', methods=['DELETE'])
@jwt_required()
def delete(diary_id):
    user_id = get_jwt_identity()
    success = delete_diary(diary_id, user_id=user_id)
    if success:
        return jsonify({"message": "Diary deleted successfully"})
    else:
        return jsonify({"message": "Diary not found or unauthorized"}), 404