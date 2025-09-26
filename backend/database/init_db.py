import os
import sys
import psycopg2
from datetime import datetime
from config import Config

def init_database():
    """Инициализация PostgreSQL базы данных"""
    
    # Сначала создаем базу данных если она не существует
    try:
        # Подключаемся к базе данных postgres для создания новой БД
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database='postgres'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Проверяем существование базы данных
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (Config.DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f'CREATE DATABASE {Config.DB_NAME}')
            print(f"База данных {Config.DB_NAME} создана успешно")
        else:
            print(f"База данных {Config.DB_NAME} уже существует")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
        return

    # Теперь импортируем и инициализируем модели
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    from app import create_app, db
    from app.models import User, Project, Defect, Comment, Attachment

    app = create_app()
    
    with app.app_context():
        try:
            # Создаем все таблицы
            db.create_all()
            print("Таблицы созданы успешно")
            
            # Проверяем, есть ли уже пользователи
            if User.query.count() == 0:
                # Создание тестовых пользователей
                manager = User(
                    email='manager@example.com',
                    first_name='Иван',
                    last_name='Петров',
                    role='manager'
                )
                manager.set_password('manager123')
                
                engineer1 = User(
                    email='engineer1@example.com',
                    first_name='Алексей',
                    last_name='Сидоров',
                    role='engineer'
                )
                engineer1.set_password('engineer123')
                
                engineer2 = User(
                    email='engineer2@example.com',
                    first_name='Ольга',
                    last_name='Кузнецова',
                    role='engineer'
                )
                engineer2.set_password('engineer123')
                
                observer = User(
                    email='observer@example.com',
                    first_name='Сергей',
                    last_name='Иванов',
                    role='observer'
                )
                observer.set_password('observer123')
                
                db.session.add_all([manager, engineer1, engineer2, observer])
                db.session.commit()
                print("Тестовые пользователи созданы")
                
                # Создание тестовых проектов
                project1 = Project(
                    name='ЖК "Северный"',
                    description='Многоэтажный жилой комплекс в северном районе города',
                    location='ул. Северная, 123',
                    start_date=datetime(2024, 1, 15),
                    end_date=datetime(2024, 12, 31),
                    is_active=True
                )
                
                project2 = Project(
                    name='БЦ "Центральный"',
                    description='Бизнес-центр класса А в центре города',
                    location='пр. Центральный, 45',
                    start_date=datetime(2024, 2, 1),
                    end_date=datetime(2024, 10, 15),
                    is_active=True
                )

                project3 = Project(
                    name='Школа №25',
                    description='Реконструкция здания школы',
                    location='ул. Школьная, 67',
                    start_date=datetime(2024, 3, 1),
                    end_date=datetime(2024, 8, 31),
                    is_active=True
                )
                
                db.session.add_all([project1, project2, project3])
                db.session.commit()
                print("Тестовые проекты созданы")
                
                # Создание тестовых дефектов
                defects = [
                    Defect(
                        title='Трещина в несущей стене',
                        description='Обнаружена трещина шириной 2 см в несущей стене на 3 этаже. Требуется срочное устранение.',
                        status='in_progress',
                        priority='high',
                        creator_id=manager.id,
                        assignee_id=engineer1.id,
                        project_id=project1.id,
                        due_date=datetime(2024, 6, 15)
                    ),
                    Defect(
                        title='Протечка кровли',
                        description='Протечка в районе вентиляционной шахты после дождя. Необходима герметизация.',
                        status='review',
                        priority='medium',
                        creator_id=engineer1.id,
                        assignee_id=engineer2.id,
                        project_id=project2.id,
                        due_date=datetime(2024, 6, 20)
                    ),
                    Defect(
                        title='Неровная покраска стен',
                        description='Наблюдается неравномерное покрытие краской в коридорах 2 этажа.',
                        status='new',
                        priority='low',
                        creator_id=engineer2.id,
                        assignee_id=engineer1.id,
                        project_id=project3.id,
                        due_date=datetime(2024, 7, 10)
                    ),
                    Defect(
                        title='Неисправность электропроводки',
                        description='Отсутствует напряжение в розетках кабинета 305. Требуется проверка щитка.',
                        status='in_progress',
                        priority='high',
                        creator_id=manager.id,
                        assignee_id=engineer2.id,
                        project_id=project1.id,
                        due_date=datetime(2024, 6, 12)
                    ),
                    Defect(
                        title='Замена оконных блоков',
                        description='Требуется замена старых деревянных окон на пластиковые в восточном крыле.',
                        status='closed',
                        priority='medium',
                        creator_id=engineer1.id,
                        assignee_id=engineer1.id,
                        project_id=project2.id,
                        due_date=datetime(2024, 5, 30)
                    )
                ]
                
                db.session.add_all(defects)
                db.session.commit()
                print("Тестовые дефекты созданы")
                
                # Создание тестовых комментариев
                comments = [
                    Comment(
                        text='Фотографии трещины прикреплены к дефекту. Требуется оценка конструктора.',
                        author_id=manager.id,
                        defect_id=1
                    ),
                    Comment(
                        text='Выполнен preliminary осмотр. Трещина не критичная, но требует устранения в течение 2 недель.',
                        author_id=engineer1.id,
                        defect_id=1
                    ),
                    Comment(
                        text='Материалы для устранения протечки заказаны. Ожидаем поставку до конца недели.',
                        author_id=engineer2.id,
                        defect_id=2
                    )
                ]
                
                db.session.add_all(comments)
                db.session.commit()
                print("Тестовые комментарии созданы")
                
                print('\n' + '='*50)
                print('База данных инициализирована успешно!')
                print('='*50)
                print('Тестовые пользователи:')
                print('  Менеджер: manager@example.com / manager123')
                print('  Инженер 1: engineer1@example.com / engineer123')
                print('  Инженер 2: engineer2@example.com / engineer123')
                print('  Наблюдатель: observer@example.com / observer123')
                print('\nТестовые проекты: ЖК "Северный", БЦ "Центральный", Школа №25')
                print('Создано тестовых дефектов: 5')
                
            else:
                print("База данных уже содержит данные. Пропускаем создание тестовых данных.")
                
        except Exception as e:
            print(f"Ошибка при инициализации базы данных: {e}")
            db.session.rollback()

if __name__ == '__main__':
    init_database()