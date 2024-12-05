from app.models import User
from app import db
import bcrypt
import werkzeug.security 

# 사용자 생성 서비스 함수 (회원가입)
def create_user(username, password):
    # 사용자 이름 중복 확인
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return None  # 이미 사용자명이 존재하면 None 반환

    # 비밀번호 해싱 및 사용자 생성
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

# 로그인
def verify_user(username, password):
    # 사용자명으로 사용자 조회
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return user  # 비밀번호가 맞으면 사용자 반환
    return None  # 사용자명이 없거나 비밀번호가 틀리면 None 반환
