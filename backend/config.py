import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-12345'
    
    # Конфигурация PostgreSQL или SQLite для разработки
    DATABASE_TYPE = os.environ.get('DATABASE_TYPE', 'sqlite')
    
    if DATABASE_TYPE == 'postgresql':
        DB_USER = os.environ.get('DB_USER') or 'defect_user'
        DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'defect_password'
        DB_HOST = os.environ.get('DB_HOST') or 'localhost'
        DB_PORT = os.environ.get('DB_PORT') or '5432'
        DB_NAME = os.environ.get('DB_NAME') or 'defect_management'
        SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    else:
        # Используем SQLite для простоты разработки
        SQLALCHEMY_DATABASE_URI = 'sqlite:///defect_management.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }