# config.py

import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://Yerim:0316@localhost/WOODA'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 성능을 위해 비활성화