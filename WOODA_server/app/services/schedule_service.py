from app.models import Schedule, Friend, User
from app import db
from datetime import datetime

# 일정 생성 서비스 함수
def create_schedule(user_id, event, date, location=None):
    schedule = Schedule(user_id=user_id, event=event, date=datetime.strptime(date, "%Y-%m-%d"), location=location)
    db.session.add(schedule)
    db.session.commit()
    return schedule

# 모든 일정 조회 서비스 함수 (자신과 친구의 일정 포함)
def get_all_schedules_with_friends(user_id):
    # 현재 사용자의 친구 목록을 가져옵니다.
    friend_ids = db.session.query(Friend.friend_id).filter(Friend.user_id == user_id).all()
    friend_ids = [fid[0] for fid in friend_ids]  # 리스트 형식으로 변환

    # 현재 사용자 ID와 친구들의 ID를 포함하여 일정 조회
    user_ids = [user_id] + friend_ids  # 자신의 ID와 친구의 ID 리스트
    schedules = Schedule.query.filter(Schedule.user_id.in_(user_ids)).all()
    
    return schedules

# 특정 일정 조회 서비스 함수
def get_schedule_by_id(schedule_id, user_id):
    return Schedule.query.filter_by(id=schedule_id, user_id=user_id).first()

# 일정 수정 서비스 함수
def update_schedule(schedule_id, user_id, event, date, location=None):
    schedule = get_schedule_by_id(schedule_id, user_id)
    if schedule:
        schedule.event = event
        schedule.date = datetime.strptime(date, "%Y-%m-%d")
        schedule.location = location
        db.session.commit()
        return schedule
    return None

# 일정 삭제 서비스 함수
def delete_schedule(schedule_id, user_id):
    schedule = get_schedule_by_id(schedule_id, user_id)
    if schedule:
        db.session.delete(schedule)
        db.session.commit()
        return True
    return False
