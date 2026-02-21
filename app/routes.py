from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from psycopg2.extras import RealDictCursor
from app.database import get_connection
from app.models import (
    User, UserCreate,
    StudyMaterial, StudyMaterialCreate, StudyMaterialUpdate,
    Task, TaskCreate, TaskUpdate
)

router = APIRouter()

# ========== User Endpoints ==========

@router.get("/health")
async def health_check():
    """Проверка работоспособности сервиса"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": f"disconnected: {str(e)}"}

@router.post("/users/", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    """Создать нового пользователя"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (email, username, password_hash) VALUES (%s, %s, %s) RETURNING id, email, username, is_active, created_at",
            (user.email, user.username, user.password)
        )
        result = cursor.fetchone()
        conn.commit()
        
        return {
            "id": result[0],
            "email": result[1],
            "username": result[2],
            "is_active": result[3],
            "created_at": result[4]
        }
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Email или username уже существуют")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при создании пользователя: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/users/", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 100):
    """Получить список всех пользователей"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute(
            "SELECT id, email, username, is_active, created_at FROM users ORDER BY id LIMIT %s OFFSET %s",
            (limit, skip)
        )
        users = cursor.fetchall()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении пользователей: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Получить пользователя по ID"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute(
            "SELECT id, email, username, is_active, created_at FROM users WHERE id = %s",
            (user_id,)
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении пользователя: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# ========== StudyMaterial Endpoints ==========

@router.post("/materials/", response_model=StudyMaterial, status_code=201)
async def create_material(material: StudyMaterialCreate):
    """Создать новый учебный материал"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """INSERT INTO study_materials 
               (title, description, content, material_type, url, tags, owner_id) 
               VALUES (%s, %s, %s, %s, %s, %s, %s) 
               RETURNING id, title, description, content, material_type, url, tags, owner_id, created_at, updated_at""",
            (material.title, material.description, material.content, 
             material.material_type, material.url, material.tags, material.owner_id)
        )
        result = cursor.fetchone()
        conn.commit()
        
        return {
            "id": result[0],
            "title": result[1],
            "description": result[2],
            "content": result[3],
            "material_type": result[4],
            "url": result[5],
            "tags": result[6],
            "owner_id": result[7],
            "created_at": result[8],
            "updated_at": result[9]
        }
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Неверный owner_id или нарушение целостности данных")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при создании материала: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/materials/", response_model=List[StudyMaterial])
async def get_materials(skip: int = 0, limit: int = 100, owner_id: Optional[int] = None):
    """Получить список учебных материалов"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        if owner_id:
            cursor.execute(
                """SELECT id, title, description, content, material_type, url, tags, 
                          owner_id, created_at, updated_at 
                   FROM study_materials 
                   WHERE owner_id = %s 
                   ORDER BY id 
                   LIMIT %s OFFSET %s""",
                (owner_id, limit, skip)
            )
        else:
            cursor.execute(
                """SELECT id, title, description, content, material_type, url, tags, 
                          owner_id, created_at, updated_at 
                   FROM study_materials 
                   ORDER BY id 
                   LIMIT %s OFFSET %s""",
                (limit, skip)
            )
        materials = cursor.fetchall()
        return materials
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении материалов: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/materials/{material_id}", response_model=StudyMaterial)
async def get_material(material_id: int):
    """Получить материал по ID"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute(
            """SELECT id, title, description, content, material_type, url, tags, 
                      owner_id, created_at, updated_at 
               FROM study_materials 
               WHERE id = %s""",
            (material_id,)
        )
        material = cursor.fetchone()
        if not material:
            raise HTTPException(status_code=404, detail="Материал не найден")
        return material
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении материала: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.put("/materials/{material_id}", response_model=StudyMaterial)
async def update_material(material_id: int, material_update: StudyMaterialUpdate):
    """Обновить материал"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Собираем поля для обновления
        update_fields = []
        update_values = []
        
        if material_update.title is not None:
            update_fields.append("title = %s")
            update_values.append(material_update.title)
        if material_update.description is not None:
            update_fields.append("description = %s")
            update_values.append(material_update.description)
        if material_update.content is not None:
            update_fields.append("content = %s")
            update_values.append(material_update.content)
        if material_update.material_type is not None:
            update_fields.append("material_type = %s")
            update_values.append(material_update.material_type)
        if material_update.url is not None:
            update_fields.append("url = %s")
            update_values.append(material_update.url)
        if material_update.tags is not None:
            update_fields.append("tags = %s")
            update_values.append(material_update.tags)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="Нет полей для обновления")
        
        update_values.append(material_id)
        query = f"UPDATE study_materials SET {', '.join(update_fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING *"
        
        cursor.execute(query, update_values)
        updated_material = cursor.fetchone()
        conn.commit()
        
        if not updated_material:
            raise HTTPException(status_code=404, detail="Материал не найден")
        
        return updated_material
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении материала: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.delete("/materials/{material_id}")
async def delete_material(material_id: int):
    """Удалить материал"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM study_materials WHERE id = %s RETURNING id", (material_id,))
        deleted = cursor.fetchone()
        conn.commit()
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Материал не найден")
        
        return {"message": "Материал успешно удалён", "id": material_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении материала: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# ========== Task Endpoints ==========

@router.post("/tasks/", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):
    """Создать новое задание"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """INSERT INTO tasks 
               (title, description, difficulty, solution, is_published, owner_id) 
               VALUES (%s, %s, %s, %s, %s, %s) 
               RETURNING id, title, description, difficulty, solution, is_published, owner_id, created_at, updated_at""",
            (task.title, task.description, task.difficulty, 
             task.solution, task.is_published, task.owner_id)
        )
        result = cursor.fetchone()
        conn.commit()
        
        return {
            "id": result[0],
            "title": result[1],
            "description": result[2],
            "difficulty": result[3],
            "solution": result[4],
            "is_published": result[5],
            "owner_id": result[6],
            "created_at": result[7],
            "updated_at": result[8]
        }
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Неверный owner_id")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при создании задания: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/tasks/", response_model=List[Task])
async def get_tasks(skip: int = 0, limit: int = 100, published_only: bool = False):
    """Получить список заданий"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        if published_only:
            cursor.execute(
                """SELECT id, title, description, difficulty, solution, is_published, 
                          owner_id, created_at, updated_at 
                   FROM tasks 
                   WHERE is_published = TRUE 
                   ORDER BY id 
                   LIMIT %s OFFSET %s""",
                (limit, skip)
            )
        else:
            cursor.execute(
                """SELECT id, title, description, difficulty, solution, is_published, 
                          owner_id, created_at, updated_at 
                   FROM tasks 
                   ORDER BY id 
                   LIMIT %s OFFSET %s""",
                (limit, skip)
            )
        tasks = cursor.fetchall()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении заданий: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    """Получить задание по ID"""
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute(
            """SELECT id, title, description, difficulty, solution, is_published, 
                      owner_id, created_at, updated_at 
               FROM tasks 
               WHERE id = %s""",
            (task_id,)
        )
        task = cursor.fetchone()
        if not task:
            raise HTTPException(status_code=404, detail="Задание не найдено")
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении задания: {str(e)}")
    finally:
        cursor.close()
        conn.close()
