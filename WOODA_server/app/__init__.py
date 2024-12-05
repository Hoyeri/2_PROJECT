from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# 데이터베이스와 로그인 관리자 초기화
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Flask 애플리케이션 생성 및 설정 로드
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    
    CORS(app)
    jwt = JWTManager(app)
    
    # 데이터베이스와 로그인 매니저를 앱에 초기화
    db.init_app(app)
    login_manager.init_app(app)

    # 블루프린트 등록
    from app.routes import auth_bp, diary_bp, schedule_bp, friends_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(diary_bp, url_prefix='/diary')
    app.register_blueprint(schedule_bp, url_prefix='/schedule')
    app.register_blueprint(friends_bp, url_prefix='/friends')
    
    # 사용자 로드 함수 정의
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # 순환 참조 방지를 위해 내부에서 임포트
        try:
            return User.query.get(user_id)
        except:
            return None


    return app