from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FolderBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = "#007bff"

class FolderCreate(FolderBase):
    pass

class FolderUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None

class Folder(FolderBase):
    id: Optional[str] = None
    user_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    note_count: int = 0

class FolderInDB(Folder):
    pass 