import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os

# Конфигурация БД
DB_CONFIG = {
    'dbname': 'edu_platform',
    'user': 'user',
    'password': 'password',
    'host': '172.40.0.2',
    'port': 5432
}

def get_connection():
    """Получить соединение с базой данных"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"✗ Ошибка подключения к базе данных: {e}")
        raise

def create_tables():
    """Создать таблицы в базе данных"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                username VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица учебных материалов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_materials (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                content TEXT NOT NULL,
                material_type VARCHAR(50) NOT NULL,
                url VARCHAR(500),
                tags VARCHAR(255),
                owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица заданий
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                difficulty VARCHAR(20),
                solution TEXT,
                is_published BOOLEAN DEFAULT FALSE,
                owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        print("✓ Таблицы созданы успешно")
        
    except psycopg2.Error as e:
        print(f"✗ Ошибка при создании таблиц: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def test_connection():
    """Проверить подключение к БД"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✓ PostgreSQL версия: {version[0]}")
        
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()
        print(f"✓ Текущая база данных: {db_name[0]}")
        
    except psycopg2.Error as e:
        print(f"✗ Ошибка: {e}")
    finally:
        cursor.close()
        conn.close()
