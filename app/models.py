from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ========== User Schemas ==========
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "username": "john_doe",
                "is_active": True,
                "created_at": "2026-02-22T10:00:00"
            }
        }

# ========== StudyMaterial Schemas ==========
class StudyMaterialBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: str
    material_type: str  # article, video, pdf, etc.
    url: Optional[str] = None
    tags: Optional[str] = None  # CSV формат: "python,backend,devops"

class StudyMaterialCreate(StudyMaterialBase):
    owner_id: int

class StudyMaterialUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    material_type: Optional[str] = None
    url: Optional[str] = None
    tags: Optional[str] = None

class StudyMaterial(StudyMaterialBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Введение в Python",
                "description": "Основы программирования",
                "content": "Python - это высокоуровневый язык...",
                "material_type": "article",
                "url": None,
                "tags": "python,backend",
                "owner_id": 1,
                "created_at": "2026-02-22T10:00:00",
                "updated_at": "2026-02-22T10:00:00"
            }
        }

# ========== Task Schemas ==========
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    difficulty: Optional[str] = None  # easy, medium, hard
    solution: Optional[str] = None
    is_published: bool = False

class TaskCreate(TaskBase):
    owner_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    solution: Optional[str] = None
    is_published: Optional[bool] = None

class Task(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Задача на списки",
                "description": "Напишите функцию...",
                "difficulty": "medium",
                "solution": "def solution():...",
                "is_published": True,
                "owner_id": 1,
                "created_at": "2026-02-22T10:00:00",
                "updated_at": "2026-02-22T10:00:00"
            }
        }
