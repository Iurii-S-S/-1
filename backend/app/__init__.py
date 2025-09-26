from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите в систему для доступа к этой странице.'
    CORS(app, supports_credentials=True)

    # Корневой маршрут
    @app.route('/')
    def index():
        return jsonify({
            "message": "Defect Management API", 
            "status": "running",
            "version": "1.0",
            "endpoints": [
                "/health",
                "/auth/login", 
                "/api/v1"
            ]
        })
    
    # Health check
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "database": "connected"})
    
    # Импорт и регистрация blueprint'ов
    try:
        from app.routes import main as main_blueprint  # Исправлено с . на backend.
        from app.auth import auth as auth_blueprint    # Исправлено с . на backend.
        from app.api import api as api_blueprint       # Исправлено с . на backend.
        
        app.register_blueprint(main_blueprint)
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        app.register_blueprint(api_blueprint, url_prefix='/api/v1')
        print("✅ Blueprints registered successfully")
        
    except Exception as e:  # Добавлено Exception
        print(f"⚠️ Blueprints error: {e}")
    
    # Создание таблиц при первом запуске
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")
    
    # Обработчик для загрузки пользователя
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Исправлено с . на backend.
        return User.query.get(int(user_id))
    
    # Обработчики ошибок
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Ресурс не найден'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Внутренняя ошибка сервера'}, 500
    
    return app