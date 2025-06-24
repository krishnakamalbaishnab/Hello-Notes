from fastapi import APIRouter, Request, HTTPException, status, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.note import NoteCreate, NoteUpdate, TodoItem
from models.folder import FolderCreate
from config.db import db
from utils.auth import get_current_user_id
from datetime import datetime
from bson import ObjectId
import os
import aiofiles
from typing import List, Optional
import uuid

note = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_user_from_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return get_current_user_id(token)

@note.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    
    database = db.get_database()
    
    # Get user info
    user = database.users.find_one({"_id": ObjectId(user_id)})
    
    # Get notes
    notes = list(database.notes.find({"user_id": user_id}).sort("updated_at", -1))
    
    # Get folders
    folders = list(database.folders.find({"user_id": user_id}).sort("name", 1))
    
    # Process notes for template
    processed_notes = []
    for note in notes:
        processed_notes.append({
            "id": str(note["_id"]),
            "title": note["title"],
            "content": note["content"][:100] + "..." if len(note["content"]) > 100 else note["content"],
            "folder_id": note.get("folder_id"),
            "is_important": note.get("is_important", False),
            "created_at": note["created_at"],
            "updated_at": note["updated_at"],
            "todo_count": len(note.get("todos", [])),
            "completed_todos": len([todo for todo in note.get("todos", []) if todo.get("completed", False)])
        })
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "notes": processed_notes,
        "folders": folders
    })

@note.get("/notes/new", response_class=HTMLResponse)
async def new_note_page(request: Request):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    
    database = db.get_database()
    folders = list(database.folders.find({"user_id": user_id}).sort("name", 1))
    
    return templates.TemplateResponse("notes/new.html", {
        "request": request,
        "folders": folders
    })

@note.post("/notes", response_class=HTMLResponse)
async def create_note(request: Request):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    except Exception as e:
        print(f"Error getting user from token: {e}")
        return RedirectResponse(url="/login", status_code=302)
    
    try:
        form = await request.form()
        
        title = form.get("title", "").strip()
        content = form.get("content", "").strip()
        folder_id = form.get("folder_id")
        is_important = form.get("is_important") == "on"
        tags = [tag.strip() for tag in form.get("tags", "").split(",") if tag.strip()]
        
        if not title:
            database = db.get_database()
            folders = list(database.folders.find({"user_id": user_id}).sort("name", 1))
            return templates.TemplateResponse("notes/new.html", {
                "request": request,
                "error": "Title is required",
                "folders": folders
            })
        
        # Process todos from form - handle both single and multiple values
        todos = []
        todo_texts = []
        
        # Check for multiple todo_text fields
        for key, value in form.items():
            if key == "todo_text":
                if isinstance(value, list):
                    todo_texts.extend(value)
                else:
                    todo_texts.append(value)
        
        for todo_text in todo_texts:
            if todo_text and todo_text.strip():
                todos.append({
                    "id": str(uuid.uuid4()),
                    "text": todo_text.strip(),
                    "completed": False,
                    "created_at": datetime.utcnow()
                })
        
        note_data = {
            "user_id": user_id,
            "title": title,
            "content": content,
            "folder_id": folder_id if folder_id else None,
            "tags": tags,
            "is_important": is_important,
            "todos": todos,
            "images": [],
            "links": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        print(f"Attempting to create note with data: {note_data}")
        
        database = db.get_database()
        result = database.notes.insert_one(note_data)
        
        print(f"Note created successfully with ID: {result.inserted_id}")
        
        return RedirectResponse(url=f"/notes/{result.inserted_id}", status_code=302)
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error creating note: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            database = db.get_database()
            folders = list(database.folders.find({"user_id": user_id}).sort("name", 1))
            return templates.TemplateResponse("notes/new.html", {
                "request": request,
                "error": f"Failed to create note: {str(e)}",
                "folders": folders
            })
        except:
            return templates.TemplateResponse("notes/new.html", {
                "request": request,
                "error": "Failed to create note. Please try again."
            })

@note.get("/notes/{note_id}", response_class=HTMLResponse)
async def view_note(request: Request, note_id: str):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    
    database = db.get_database()
    
    try:
        note = database.notes.find_one({"_id": ObjectId(note_id), "user_id": user_id})
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
    except:
        raise HTTPException(status_code=404, detail="Invalid note ID")
    
    folders = list(database.folders.find({"user_id": user_id}).sort("name", 1))
    
    return templates.TemplateResponse("notes/view.html", {
        "request": request,
        "note": note,
        "folders": folders
    })

@note.get("/notes/{note_id}/edit", response_class=HTMLResponse)
async def edit_note_page(request: Request, note_id: str):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    
    database = db.get_database()
    
    try:
        note = database.notes.find_one({"_id": ObjectId(note_id), "user_id": user_id})
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
    except:
        raise HTTPException(status_code=404, detail="Invalid note ID")
    
    folders = list(database.folders.find({"user_id": user_id}).sort("name", 1))
    
    return templates.TemplateResponse("notes/edit.html", {
        "request": request,
        "note": note,
        "folders": folders
    })

@note.post("/notes/{note_id}", response_class=HTMLResponse)
async def update_note(request: Request, note_id: str):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    
    form = await request.form()
    
    title = form.get("title", "").strip()
    content = form.get("content", "").strip()
    folder_id = form.get("folder_id")
    is_important = form.get("is_important") == "on"
    tags = [tag.strip() for tag in form.get("tags", "").split(",") if tag.strip()]
    
    if not title:
        database = db.get_database()
        folders = list(database.folders.find({"user_id": user_id}).sort("name", 1))
        note = database.notes.find_one({"_id": ObjectId(note_id), "user_id": user_id})
        return templates.TemplateResponse("notes/edit.html", {
            "request": request,
            "error": "Title is required",
            "note": note,
            "folders": folders
        })
    
    # Process todos from form
    todos = []
    todo_texts = []
    
    # Check for multiple todo_text fields
    for key, value in form.items():
        if key == "todo_text":
            if isinstance(value, list):
                todo_texts.extend(value)
            else:
                todo_texts.append(value)
    
    for todo_text in todo_texts:
        if todo_text and todo_text.strip():
            todos.append({
                "id": str(uuid.uuid4()),
                "text": todo_text.strip(),
                "completed": False,
                "created_at": datetime.utcnow()
            })
    
    update_data = {
        "title": title,
        "content": content,
        "folder_id": folder_id if folder_id else None,
        "tags": tags,
        "is_important": is_important,
        "todos": todos,
        "updated_at": datetime.utcnow()
    }
    
    try:
        database = db.get_database()
        result = database.notes.update_one(
            {"_id": ObjectId(note_id), "user_id": user_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Note not found")
        
        return RedirectResponse(url=f"/notes/{note_id}", status_code=302)
    except Exception as e:
        print(f"Error updating note: {e}")
        database = db.get_database()
        folders = list(database.folders.find({"user_id": user_id}).sort("name", 1))
        note = database.notes.find_one({"_id": ObjectId(note_id), "user_id": user_id})
        return templates.TemplateResponse("notes/edit.html", {
            "request": request,
            "error": "Failed to update note. Please try again.",
            "note": note,
            "folders": folders
        })

@note.post("/notes/{note_id}/delete")
async def delete_note(request: Request, note_id: str):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    
    database = db.get_database()
    result = database.notes.delete_one({"_id": ObjectId(note_id), "user_id": user_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return RedirectResponse(url="/dashboard", status_code=302)

@note.post("/notes/{note_id}/toggle-important")
async def toggle_important(request: Request, note_id: str):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    
    database = db.get_database()
    note = database.notes.find_one({"_id": ObjectId(note_id), "user_id": user_id})
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    new_important = not note.get("is_important", False)
    database.notes.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": {"is_important": new_important, "updated_at": datetime.utcnow()}}
    )
    
    return RedirectResponse(url=f"/notes/{note_id}", status_code=302)