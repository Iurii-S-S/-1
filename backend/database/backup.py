import os
import subprocess
from datetime import datetime
from config import Config

def backup_database():
    """Создание резервной копии PostgreSQL базы данных"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'defect_management_backup_{timestamp}.sql'
    backup_path = os.path.join('backups', backup_filename)
    
    # Создаем папку для бэкапов если не существует
    os.makedirs('backups', exist_ok=True)
    
    # Команда для pg_dump
    cmd = [
        'pg_dump',
        '-h', Config.DB_HOST,
        '-p', Config.DB_PORT,
        '-U', Config.DB_USER,
        '-d', Config.DB_NAME,
        '-f', backup_path,
        '--verbose'
    ]
    
    # Устанавливаем переменную окружения для пароля
    env = os.environ.copy()
    env['PGPASSWORD'] = Config.DB_PASSWORD
    
    try:
        print(f"Создание резервной копии базы данных...")
        result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)
        print(f"Резервная копия создана: {backup_path}")
        return backup_path
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании резервной копии: {e}")
        print(f"Stderr: {e.stderr}")
        return None

def restore_database(backup_path):
    """Восстановление базы данных из резервной копии"""
    
    if not os.path.exists(backup_path):
        print(f"Файл резервной копии не найден: {backup_path}")
        return False
    
    # Команда для psql восстановления
    cmd = [
        'psql',
        '-h', Config.DB_HOST,
        '-p', Config.DB_PORT,
        '-U', Config.DB_USER,
        '-d', Config.DB_NAME,
        '-f', backup_path
    ]
    
    env = os.environ.copy()
    env['PGPASSWORD'] = Config.DB_PASSWORD
    
    try:
        print(f"Восстановление базы данных из {backup_path}...")
        result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)
        print("База данных восстановлена успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при восстановлении базы данных: {e}")
        print(f"Stderr: {e.stderr}")
        return False

if __name__ == '__main__':
    # Пример использования
    backup_path = backup_database()
    if backup_path:
        print(f"Backup created: {backup_path}")