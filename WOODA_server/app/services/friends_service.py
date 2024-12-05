from app.models import User, Friend
from app import db
from datetime import datetime

# 친구 추가 서비스 함수
def add_friend(user_id, friend_username):
    # 친구 추가 대상 사용자 조회
    friend = User.query.filter_by(username=friend_username).first()
    if not friend:
        return False, "User not found"

    # 이미 친구 관계가 있는지 확인
    existing_friend = Friend.query.filter_by(user_id=user_id, friend_id=friend.id).first()
    if existing_friend:
        return False, "Already friends"

    # 친구 관계 생성
    new_friend = Friend(user_id=user_id, friend_id=friend.id, date_added=datetime.utcnow())
    db.session.add(new_friend)
    db.session.commit()
    return True, "Friend added successfully"

# 친구 목록 조회 서비스 함수
def get_friends(user_id):
    # 사용자 ID로 친구 목록을 조회하여 친구 ID와 이름을 반환
    friends = db.session.query(User.id, User.username).join(Friend, Friend.friend_id == User.id).filter(Friend.user_id == user_id).all()
    return friends

# 친구 삭제 서비스 함수
def remove_friend(user_id, friend_username):
    # 친구 삭제 대상 사용자 조회
    friend = User.query.filter_by(username=friend_username).first()
    if not friend:
        return False, "User not found"

    # 친구 관계 조회 및 삭제
    existing_friend = Friend.query.filter_by(user_id=user_id, friend_id=friend.id).first()
    if existing_friend:
        db.session.delete(existing_friend)
        db.session.commit()
        return True, "Friend removed successfully"
    return False, "Friend not found"
