from datetime import datetime,  timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db


# 사용자 모델
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    
    # 사용자와 일기, 일정, 친구 관계 설정
    items = db.relationship('Item', back_populates='user')
    schedules = db.relationship('Schedule', backref='owner', lazy=True)
    
    # friends 관계에서 foreign_keys로 명확히 지정
    friends = db.relationship(
        'Friend', 
        foreign_keys='Friend.user_id',  # Friend 모델의 user_id를 외래 키로 지정
        backref='user', 
        lazy=True
    )
    
    friend_of = db.relationship(
        'Friend', 
        foreign_keys='Friend.friend_id',  # Friend 모델의 friend_id를 외래 키로 지정
        backref='friend', 
        lazy=True
    )


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='items')
    type = db.Column(db.String(20), nullable=False)  # "schedule" or "diary"
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)  # Optional
    date = db.Column(db.DateTime, nullable=False)  # 클라이언트에서 전달받은 시각 저장
    likes = db.Column(db.Integer, default=0)  # Default likes to 0

    user = db.relationship('User', back_populates='items')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "date": self.date.isoformat(),  # 클라이언트에서 받은 날짜 반환
            "likes": self.likes,
        }



# 일정 모델
class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(150))  # 일정 장소
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

# 친구 관계 모델
class Friend(db.Model):
    __tablename__ = 'friends'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Friend 모델의 user_id와 friend_id를 통해 사용자 간 친구 관계 설정
