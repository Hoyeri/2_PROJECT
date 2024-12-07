# items.py
from app.models import Item
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from ..services.items_service import (
    create_item, fetch_items_by_date, get_item_by_id, get_all_items_with_friends, update_item, delete_item
)

from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity

# 블루프린트 정의
bp = Blueprint('items', __name__)

# 일기 작성 엔드포인트
@bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    type = data.get('type')
    title = data.get('title')
    date = data.get('date')
    description = data.get('description')
    image = data.get('image') or None
    
    # 유효성 검사
    if not title or not description:
        return jsonify({"message": "Title and description are required"}), 400
    
    _date = date
    
    # 일기 생성 서비스 호출
    user_id = get_jwt_identity()  # JWT에서 사용자 ID 추출
    item = create_item(user_id=user_id, type=type, title=title, description=description, date=_date, image=image)
    return jsonify({"message": "item created successfully", "item_id": item.id}), 201


@bp.route('/by-date', methods=['GET'])
@jwt_required()
def get_items_by_date_endpoint():
    user_id = get_jwt_identity()
    date_str = request.args.get('date')  # `date` 파라미터를 쿼리에서 추출
    if not date_str:
        return jsonify({"message": "Missing 'date' query parameter"}), 400
    # 날짜 형식 검증
    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400

    # 특정 날짜의 아이템 필터링
    items = fetch_items_by_date(user_id, selected_date)

    # 결과 반환
    return jsonify([item.to_dict() for item in items]), 200




# 모든 일기 조회 (자신과 친구의 일기 포함, 최신순 정렬)
@bp.route('/all', methods=['GET'])
@jwt_required()
def get_all():
    user_id = get_jwt_identity()
    items = get_all_items_with_friends(user_id=user_id)
    return jsonify([{
        "id": item.id,
        "type": item.type,
        "title": item.title,
        "date": item.date.strftime("%Y-%m-%d %H:%M:%S"),
        "description": item.description,
        "image": item.image,
        "likes": item.likes
    } for item in items])
    
# 특정 일기 조회 엔드포인트
@bp.route('/<int:item_id>', methods=['GET'])
@jwt_required()
def get_item(item_id):
    user_id = get_jwt_identity()
    item = get_item_by_id(item_id, user_id=user_id)
    if item:
        return jsonify({
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "date": item.date.strftime("%Y-%m-%d %H:%M:%S")
        })
    else:
        return jsonify({"message": "item not found"}), 404

# 일기 수정 엔드포인트
@bp.route('/update/<int:item_id>', methods=['PUT'])
@jwt_required()
def update(item_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    # 유효성 검사
    if not title or not description:
        return jsonify({"message": "Title and description are required"}), 400

    user_id = get_jwt_identity()
    updated_item = update_item(item_id, user_id=user_id, title=title, description=description)
    if updated_item:
        return jsonify({"message": "item updated successfully"})
    else:
        return jsonify({"message": "item not found or unauthorized"}), 404

# 일기 삭제 엔드포인트
@bp.route('/delete/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete(item_id):
    user_id = get_jwt_identity()
    success = delete_item(item_id, user_id=user_id)
    if success:
        return jsonify({"message": "item deleted successfully"})
    else:
        return jsonify({"message": "item not found or unauthorized"}), 404