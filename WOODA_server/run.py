from app import create_app, db  # db도 import

# 애플리케이션 생성
app = create_app()

app.secret_key = 'your_unique_and_secret_key' 
 
# 애플리케이션 실행 전에 데이터베이스 초기화
with app.app_context():
    db.create_all()  # 테이블 생성
    print("Database initialized.")

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)
