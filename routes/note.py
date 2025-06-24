from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from models.note import Note
from config.db import connection
from schemas.note import notesEntity, noteEntity
from fastapi.templating import Jinja2Templates
from typing import Optional  # Add this import

note = APIRouter()
templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = connection.hellonotes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id": doc["_id"],
            "note": doc["note"]
        })
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})

@note.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):  # Fixed here
    return {"item_id": item_id, "q": q}
