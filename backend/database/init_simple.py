import os
import sys
from datetime import datetime

# Добавляем путь к backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User, Project, Defect

def init_simple_database():
    """Простая инициализация базы данных с SQLite"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("Создание таблиц базы данных...")
            db.create_all()
            print("Таблицы созданы успешно!")
            
            # Проверяем, есть ли пользователи
            if User.query.count() == 0:
                print("Создание тестовых данных...")
                
                # Создаем пользователей
                users = [
                    User(email='manager@example.com', first_name='Иван', last_name='Петров', role='manager'),
                    User(email='engineer@example.com', first_name='Алексей', last_name='Сидоров', role='engineer'),
                    User(email='observer@example.com', first_name='Сергей', last_name='Иванов', role='observer')
                ]
                
                for user in users:
                    user.set_password('password123')
                
                db.session.add_all(users)
                db.session.commit()
                print("Пользователи созданы")
                
                # Создаем проекты
                projects = [
                    Project(name='ЖК "Северный"', description='Жилой комплекс', location='ул. Северная', is_active=True),
                    Project(name='БЦ "Центральный"', description='Бизнес-центр', location='пр. Центральный', is_active=True)
                ]
                
                db.session.add_all(projects)
                db.session.commit()
                print("Проекты созданы")
                
                # Создаем тестовые дефекты
                defects = [
                    Defect(
                        title='Трещина в стене',
                        description='Обнаружена трещина на 3 этаже',
                        status='in_progress',
                        priority='high',
                        creator_id=1,
                        assignee_id=2,
                        project_id=1,
                        due_date=datetime(2024, 12, 31)
                    )
                ]
                
                db.session.add_all(defects)
                db.session.commit()
                print("Тестовые дефекты созданы")
                
                print("\n" + "="*50)
                print("БАЗА ДАННЫХ УСПЕШНО ИНИЦИАЛИЗИРОВАНА!")
                print("="*50)
                print("\nТестовые пользователи:")
                print("Менеджер: manager@example.com / password123")
                print("Инженер: engineer@example.com / password123") 
                print("Наблюдатель: observer@example.com / password123")
                print("\nБаза данных: defect_management.db")
                
            else:
                print("База данных уже содержит данные.")
                
        except Exception as e:
            print(f"Ошибка при инициализации: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    init_simple_database()