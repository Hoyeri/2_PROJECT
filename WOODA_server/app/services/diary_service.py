from app.models import Diary, Friend
from app import db
from datetime import datetime

# 일기 생성 서비스 함수
def create_diary(user_id, title, content):
    diary = Diary(user_id=user_id, title=title, content=content, date_created=datetime())
    db.session.add(diary)
    db.session.commit()
    return diary

# 모든 일기 조회 서비스 함수 
def get_all_diaries_with_friends(user_id):
    friend_ids = db.session.query(Friend.friend_id).filter(Friend.user_id == user_id).all()
    friend_ids = [fid[0] for fid in friend_ids]  # 리스트 형식으로 변환

    # 현재 사용자 ID와 친구들의 ID 포함 일기 조회 
    user_ids = [user_id] + friend_ids
    diaries = Diary.query.filter(Diary.user_id.in_(user_ids)).order_by(Diary.date_created.desc()).all()
    
    return diaries

# 특정 일기 조회 함수
def get_diary_by_id(diary_id, user_id):
    return Diary.query.filter_by(id=diary_id, user_id=user_id).first()

# 일기 수정 서비스 함수
def update_diary(diary_id, user_id, title, content):
    diary = get_diary_by_id(diary_id, user_id)
    if diary:
        diary.title = title
        diary.content = content
        diary.date_created = datetime()  # 수정 시 업데이트 날짜 변경
        db.session.commit()
        return diary
    return None

# 일기 삭제 서비스 함수
def delete_diary(diary_id, user_id):
    diary = get_diary_by_id(diary_id, user_id)
    if diary:
        db.session.delete(diary)
        db.session.commit()
        return True
    return False
