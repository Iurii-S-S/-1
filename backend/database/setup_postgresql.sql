-- Создание пользователя и базы данных для системы управления дефектами

-- Создание пользователя (выполнить от имени postgres пользователя)
CREATE USER defect_user WITH PASSWORD 'defect_password';

-- Создание базы данных
CREATE DATABASE defect_management 
    WITH 
    OWNER = defect_user
    ENCODING = 'UTF8'
    LC_COLLATE = 'ru_RU.UTF-8'
    LC_CTYPE = 'ru_RU.UTF-8'
    TEMPLATE = template0;

-- Подключение к базе данных и выдача прав
\c defect_management;

-- Выдаем права пользователю
GRANT ALL PRIVILEGES ON DATABASE defect_management TO defect_user;
GRANT ALL ON SCHEMA public TO defect_user;

-- Создание расширения для полнотекстового поиска (опционально)
CREATE EXTENSION IF NOT EXISTS pg_trgm;