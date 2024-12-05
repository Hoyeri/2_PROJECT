from flask import Blueprint, request, jsonify
from app.services.auth_service import create_user, verify_user
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# 블루프린트 정의
bp = Blueprint('auth', __name__)

# 회원가입 엔드포인트
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 유효성 검사
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    # 사용자 생성 서비스 호출
    user = create_user(username, password)
    if user:
        return jsonify({"message": "User registered successfully"}), 201
    else:
        return jsonify({"message": "Username already exists"}), 409

# 로그인 엔드포인트
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 사용자 검증 서비스 호출
    user = verify_user(username, password)
    if user:
        token = create_access_token(identity=user.id)
        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# 로그아웃 엔드포인트
@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

# 로그인 상태 확인 엔드포인트 (테스트용)
@bp.route('/status', methods=['GET'])
@jwt_required()
def status():
    return jsonify({"message": f"Logged in as {current_user.username}"}), 200
