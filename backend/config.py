import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-12345'
    
    # Конфигурация PostgreSQL
    DB_USER = os.environ.get('PGUSER', 'postgres')
    DB_PASSWORD = os.environ.get('PGPASSWORD', '12345678')
    DB_HOST = os.environ.get('PGHOST', 'localhost')
    DB_PORT = os.environ.get('PGPORT', '5432')
    DB_NAME = os.environ.get('PGNAME', 'defect_management')
    
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Оптимизация для PostgreSQL
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }