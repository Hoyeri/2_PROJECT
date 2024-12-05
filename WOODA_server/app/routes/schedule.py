from flask import Blueprint, request, jsonify
from app.services.schedule_service import (
    create_schedule, get_schedule_by_id, get_all_schedules_with_friends, update_schedule, delete_schedule
)
from flask_jwt_extended import jwt_required, get_jwt_identity

# 블루프린트 정의
bp = Blueprint('schedule', __name__)

# 일정 생성 엔드포인트
@bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    event = data.get('event')
    date = data.get('date')
    location = data.get('location')

    # 유효성 검사
    if not event or not date:
        return jsonify({"message": "Event and date are required"}), 400

    # 일정 생성 서비스 호출
    user_id = get_jwt_identity()
    schedule = create_schedule(user_id=user_id, event=event, date=date, location=location)
    return jsonify({"message": "Schedule created successfully", "schedule_id": schedule.id}), 201

# 모든 일정 조회 (자신과 친구의 일정 포함)
@bp.route('/all', methods=['GET'])
@jwt_required()
def get_all():
    user_id = get_jwt_identity()
    schedules = get_all_schedules_with_friends(user_id=user_id)
    return jsonify([{
        "id": schedule.id,
        "event": schedule.event,
        "date": schedule.date,
        "location": schedule.location,
        "owner": schedule.owner.username  # 일정 소유자의 이름 포함
    } for schedule in schedules])

# 특정 일정 조회 엔드포인트
@bp.route('/<int:schedule_id>', methods=['GET'])
@jwt_required()
def get_schedule(schedule_id):
    user_id = get_jwt_identity()
    schedule = get_schedule_by_id(schedule_id, user_id=user_id)
    if schedule:
        return jsonify({
            "id": schedule.id,
            "event": schedule.event,
            "date": schedule.date,
            "location": schedule.location
        })
    else:
        return jsonify({"message": "Schedule not found"}), 404

# 일정 수정 엔드포인트
@bp.route('/update/<int:schedule_id>', methods=['PUT'])
@jwt_required()
def update(schedule_id):
    data = request.get_json()
    event = data.get('event')
    date = data.get('date')
    location = data.get('location')

    # 유효성 검사
    if not event or not date:
        return jsonify({"message": "Event and date are required"}), 400

    # 일정 수정 서비스 호출
    user_id = get_jwt_identity()
    updated_schedule = update_schedule(schedule_id, user_id=user_id, event=event, date=date, location=location)
    if updated_schedule:
        return jsonify({"message": "Schedule updated successfully"})
    else:
        return jsonify({"message": "Schedule not found or unauthorized"}), 404

# 일정 삭제 엔드포인트
@bp.route('/delete/<int:schedule_id>', methods=['DELETE'])
@jwt_required()
def delete(schedule_id):
    user_id = get_jwt_identity()
    success = delete_schedule(schedule_id, user_id=user_id)
    if success:
        return jsonify({"message": "Schedule deleted successfully"})
    else:
        return jsonify({"message": "Schedule not found or unauthorized"}), 404
