from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.folder import FolderCreate, FolderUpdate
from config.db import db
from utils.auth import get_current_user_id
from datetime import datetime
from bson import ObjectId

folder = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_user_from_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return get_current_user_id(token)

@folder.get("/folders", response_class=HTMLResponse)
async def folders_page(request: Request):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    
    database = db.get_database()
    
    # Get folders with note counts
    folders = list(database.folders.find({"user_id": user_id}).sort("name", 1))
    
    for folder in folders:
        note_count = database.notes.count_documents({"user_id": user_id, "folder_id": str(folder["_id"])})
        folder["note_count"] = note_count
    
    return templates.TemplateResponse("folders/index.html", {
        "request": request,
        "folders": folders
    })

@folder.get("/folders/new", response_class=HTMLResponse)
async def new_folder_page(request: Request):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("folders/new.html", {"request": request})

@folder.post("/folders/create", response_class=HTMLResponse)
async def create_folder(request: Request):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    
    form = await request.form()
    
    name = form.get("name", "").strip()
    description = form.get("description", "").strip()
    color = form.get("color", "#007bff")
    
    if not name:
        return templates.TemplateResponse("folders/new.html", {
            "request": request,
            "error": "Folder name is required"
        })
    
    folder_data = {
        "user_id": user_id,
        "name": name,
        "description": description,
        "color": color,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "note_count": 0
    }
    
    database = db.get_database()
    result = database.folders.insert_one(folder_data)
    
    return RedirectResponse(url="/folders", status_code=302)

@folder.get("/folders/{folder_id}", response_class=HTMLResponse)
async def view_folder(request: Request, folder_id: str):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    
    database = db.get_database()
    
    try:
        folder = database.folders.find_one({"_id": ObjectId(folder_id), "user_id": user_id})
        if not folder:
            raise HTTPException(status_code=404, detail="Folder not found")
    except:
        raise HTTPException(status_code=404, detail="Invalid folder ID")
    
    # Get notes in this folder
    notes = list(database.notes.find({"user_id": user_id, "folder_id": folder_id}).sort("updated_at", -1))
    
    # Process notes for template
    processed_notes = []
    for note in notes:
        processed_notes.append({
            "id": str(note["_id"]),
            "title": note["title"],
            "content": note["content"][:100] + "..." if len(note["content"]) > 100 else note["content"],
            "is_important": note.get("is_important", False),
            "created_at": note["created_at"],
            "updated_at": note["updated_at"],
            "todo_count": len(note.get("todos", [])),
            "completed_todos": len([todo for todo in note.get("todos", []) if todo.get("completed", False)])
        })
    
    return templates.TemplateResponse("folders/view.html", {
        "request": request,
        "folder": folder,
        "notes": processed_notes
    })

@folder.get("/folders/{folder_id}/edit", response_class=HTMLResponse)
async def edit_folder_page(request: Request, folder_id: str):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    
    database = db.get_database()
    
    try:
        folder = database.folders.find_one({"_id": ObjectId(folder_id), "user_id": user_id})
        if not folder:
            raise HTTPException(status_code=404, detail="Folder not found")
    except:
        raise HTTPException(status_code=404, detail="Invalid folder ID")
    
    return templates.TemplateResponse("folders/edit.html", {
        "request": request,
        "folder": folder
    })

@folder.post("/folders/{folder_id}", response_class=HTMLResponse)
async def update_folder(request: Request, folder_id: str):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    
    form = await request.form()
    
    name = form.get("name", "").strip()
    description = form.get("description", "").strip()
    color = form.get("color", "#007bff")
    
    if not name:
        return templates.TemplateResponse("folders/edit.html", {
            "request": request,
            "error": "Folder name is required"
        })
    
    update_data = {
        "name": name,
        "description": description,
        "color": color,
        "updated_at": datetime.utcnow()
    }
    
    database = db.get_database()
    result = database.folders.update_one(
        {"_id": ObjectId(folder_id), "user_id": user_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Folder not found")
    
    return RedirectResponse(url=f"/folders/{folder_id}", status_code=302)

@folder.post("/folders/{folder_id}/delete")
async def delete_folder(request: Request, folder_id: str):
    try:
        user_id = get_user_from_token(request)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=302)
    
    database = db.get_database()
    
    # Check if folder has notes
    note_count = database.notes.count_documents({"user_id": user_id, "folder_id": folder_id})
    if note_count > 0:
        return templates.TemplateResponse("folders/view.html", {
            "request": request,
            "error": "Cannot delete folder with notes. Please move or delete all notes first."
        })
    
    result = database.folders.delete_one({"_id": ObjectId(folder_id), "user_id": user_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Folder not found")
    
    return RedirectResponse(url="/folders", status_code=302) 