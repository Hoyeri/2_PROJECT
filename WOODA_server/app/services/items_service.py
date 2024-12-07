from app.models import Item, Friend
from app import db
from datetime import datetime, timezone
from sqlalchemy import and_
from datetime import datetime, timezone



# 일기 생성 서비스 함수
def create_item(user_id, type, title, date, description, image):
    """
    일기를 생성하는 서비스 함수
    :param user_id: 사용자 ID
    :param type: 항목 유형 ("schedule" 또는 "diary")
    :param title: 항목 제목
    :param date: 선택한 날짜 (ISO 8601 형식, 클라이언트에서 전달됨)
    :param description: 항목 내용
    :param image: 이미지 경로 (옵션)
    :return: 생성된 Item 객체
    """
    # 클라이언트에서 ISO 8601 형식으로 전달된 날짜를 UTC 시간대로 변환

    # date를 UTC로 변환
    parsed_date = datetime.fromisoformat(date).replace(tzinfo=timezone.utc)

    # 새로운 항목 생성
    item = Item(
        user_id=user_id,
        type=type,
        title=title,
        description=description,
        date=parsed_date,  # 클라이언트에서 전달된 날짜 사용
        image=image,
        likes=0,
    )
    db.session.add(item)
    db.session.commit()
    return item

# 모든 일기 조회 서비스 함수 
def get_all_items_with_friends(user_id):
    friend_ids = db.session.query(Friend.friend_id).filter(Friend.user_id == user_id).all()
    friend_ids = [fid[0] for fid in friend_ids]  # 리스트 형식으로 변환

    # 현재 사용자 ID와 친구들의 ID 포함 일기 조회 
    user_ids = [user_id] + friend_ids
    items = Item.query.filter(Item.user_id.in_(user_ids)).order_by(Item.date.desc()).all()
    
    return items

def fetch_items_by_date(user_id, selected_date):
    """
    특정 날짜의 아이템을 가져오는 함수.
    - user_id: 요청한 사용자의 ID
    - selected_date: 조회할 날짜 (datetime.date 객체)
    """
    # 선택된 날짜의 시작과 끝 시간 계산
    start_of_day = datetime.combine(selected_date, datetime.min.time())
    end_of_day = datetime.combine(selected_date, datetime.max.time())

    # 데이터베이스에서 필터링
    return Item.query.filter(
        Item.user_id == user_id,
        Item.date >= start_of_day,
        Item.date <= end_of_day
    ).all()



# 특정 일기 조회 함수
def get_item_by_id(item_id, user_id):
    return Item.query.filter_by(id=item_id, user_id=user_id).first()

# 일기 수정 서비스 함수
def update_item(item_id, user_id, title, description):
    item = get_item_by_id(item_id, user_id)
    if item:
        item.title = title
        item.description = description
        db.session.commit()
        return item
    return None

# 일기 삭제 서비스 함수
def delete_item(item_id, user_id):
    item = get_item_by_id(item_id, user_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return True
    return False
