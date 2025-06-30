from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes import auth, note, folder
from config.db import db
import os

app = FastAPI(title="HelloNotes", description="A student-focused note-taking application")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth.auth, prefix="/auth", tags=["Authentication"])
app.include_router(note.note, tags=["Notes"])
app.include_router(folder.folder, tags=["Folders"])

# Templates
templates = Jinja2Templates(directory="templates")

# Create upload directory if it doesn't exist
os.makedirs("static/uploads", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Check if user is authenticated
    token = request.cookies.get("access_token")
    if token:
        try:
            from utils.auth import verify_token
            user_id = verify_token(token)
            if user_id:
                return RedirectResponse(url="/dashboard", status_code=302)
        except:
            pass
    
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_redirect(request: Request):
    return RedirectResponse(url="/auth/login", status_code=302)

@app.get("/register", response_class=HTMLResponse)
async def register_redirect(request: Request):
    return RedirectResponse(url="/auth/register", status_code=302)

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker and load balancers"""
    return {"status": "healthy", "service": "HelloNotes"}







