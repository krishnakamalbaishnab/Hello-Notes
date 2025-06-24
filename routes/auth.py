from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.user import UserCreate, UserLogin
from config.db import db
from utils.auth import get_password_hash, verify_password, create_access_token
from datetime import datetime
from bson import ObjectId

auth = APIRouter()
templates = Jinja2Templates(directory="templates")

@auth.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@auth.post("/register", response_class=HTMLResponse)
async def register(request: Request):
    form = await request.form()
    
    # Validate form data
    email = form.get("email")
    username = form.get("username")
    password = form.get("password")
    confirm_password = form.get("confirm_password")
    
    if not all([email, username, password, confirm_password]):
        return templates.TemplateResponse(
            "auth/register.html", 
            {"request": request, "error": "All fields are required"}
        )
    
    if password != confirm_password:
        return templates.TemplateResponse(
            "auth/register.html", 
            {"request": request, "error": "Passwords do not match"}
        )
    
    # Check if user already exists
    database = db.get_database()
    existing_user = database.users.find_one({"email": email})
    if existing_user:
        return templates.TemplateResponse(
            "auth/register.html", 
            {"request": request, "error": "Email already registered"}
        )
    
    # Create new user
    hashed_password = get_password_hash(password)
    user_data = {
        "email": email,
        "username": username,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    result = database.users.insert_one(user_data)
    
    # Redirect to login
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return response

@auth.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})

@auth.post("/login", response_class=HTMLResponse)
async def login(request: Request):
    form = await request.form()
    
    email = form.get("email")
    password = form.get("password")
    
    if not email or not password:
        return templates.TemplateResponse(
            "auth/login.html", 
            {"request": request, "error": "Email and password are required"}
        )
    
    # Find user
    database = db.get_database()
    user = database.users.find_one({"email": email})
    
    if not user or not verify_password(password, user["hashed_password"]):
        return templates.TemplateResponse(
            "auth/login.html", 
            {"request": request, "error": "Invalid email or password"}
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user["_id"])})
    
    # Redirect to dashboard with token
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=1800)
    return response

@auth.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response 