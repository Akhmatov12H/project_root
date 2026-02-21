#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
from database import get_connection, create_tables, test_connection

def add_user(email, username, password_hash):
    """Добавить пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s) RETURNING id",
            (email, username, password_hash)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        print(f"✓ Пользователь '{username}' добавлен с ID={user_id}")
        return user_id
    except psycopg2.Error as e:
        print(f"✗ Ошибка при добавлении пользователя: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_users():
    """Получить всех пользователей"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, username, email, created_at FROM users ORDER BY id")
        users = cursor.fetchall()
        
        if not users:
            print("⚠ Пользователей нет")
            return []
        
        print(f"\n{'ID':<5} {'Username':<20} {'Email':<30} {'Created At'}")
        print("-" * 80)
        for user in users:
            print(f"{user[0]:<5} {user[1]:<20} {user[2]:<30} {user[3]}")
        
        return users
    except psycopg2.Error as e:
        print(f"✗ Ошибка при получении пользователей: {e}")
    finally:
        cursor.close()
        conn.close()

def add_material(title, content, material_type, owner_id):
    """Добавить учебный материал"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO study_materials (title, content, material_type, owner_id) VALUES (%s, %s, %s, %s) RETURNING id",
            (title, content, material_type, owner_id)
        )
        material_id = cursor.fetchone()[0]
        conn.commit()
        print(f"✓ Материал '{title}' добавлен с ID={material_id}")
        return material_id
    except psycopg2.Error as e:
        print(f"✗ Ошибка при добавлении материала: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_materials():
    """Получить все материалы"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT sm.id, sm.title, sm.material_type, u.username, sm.created_at
            FROM study_materials sm
            LEFT JOIN users u ON sm.owner_id = u.id
            ORDER BY sm.id
        """)
        materials = cursor.fetchall()
        
        if not materials:
            print("⚠ Материалов нет")
            return []
        
        print(f"\n{'ID':<5} {'Title':<30} {'Type':<15} {'Owner':<20} {'Created At'}")
        print("-" * 100)
        for material in materials:
            print(f"{material[0]:<5} {material[1]:<30} {material[2]:<15} {material[3]:<20} {material[4]}")
        
        return materials
    except psycopg2.Error as e:
        print(f"✗ Ошибка при получении материалов: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    """Главное меню приложения"""
    print("=" * 60)
    print("  УЧЕБНАЯ ПЛАТФОРМА - Консольное приложение")
    print("=" * 60)
    
    # Создаём таблицы при первом запуске
    create_tables()
    
    while True:
        print("\n" + "=" * 60)
        print("Меню:")
        print("1. Проверить подключение к БД")
        print("2. Добавить пользователя")
        print("3. Показать всех пользователей")
        print("4. Добавить учебный материал")
        print("5. Показать все материалы")
        print("0. Выход")
        print("=" * 60)
        
        choice = input("\nВыберите действие (0-5): ").strip()
        
        if choice == '1':
            test_connection()
        
        elif choice == '2':
            email = input("Email: ").strip()
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            add_user(email, username, password)
        
        elif choice == '3':
            get_users()
        
        elif choice == '4':
            title = input("Название материала: ").strip()
            content = input("Содержание: ").strip()
            material_type = input("Тип (article/video/pdf): ").strip()
            owner_id = int(input("ID владельца: ").strip())
            add_material(title, content, material_type, owner_id)
        
        elif choice == '5':
            get_materials()
        
        elif choice == '0':
            print("\nДо свидания!")
            break
        
        else:
            print("⚠ Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
