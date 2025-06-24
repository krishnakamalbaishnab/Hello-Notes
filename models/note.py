from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class TodoItem(BaseModel):
    id: Optional[str] = None
    text: str
    completed: bool = False
    created_at: Optional[datetime] = None

class NoteBase(BaseModel):
    title: str
    content: str
    folder_id: Optional[str] = None
    tags: List[str] = []
    is_important: bool = False
    todos: List[TodoItem] = []
    images: List[str] = []
    links: List[str] = []

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    folder_id: Optional[str] = None
    tags: Optional[List[str]] = None
    is_important: Optional[bool] = None
    todos: Optional[List[TodoItem]] = None
    images: Optional[List[str]] = None
    links: Optional[List[str]] = None

class Note(NoteBase):
    id: Optional[str] = None
    user_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class NoteInDB(Note):
    pass
