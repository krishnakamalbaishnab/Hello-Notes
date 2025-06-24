from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.user import UserCreate, UserLogin
from config.db import db
from utils.auth import get_password_hash, verify_password, create_access_token
from utils.email_service import generate_verification_code, generate_verification_expiry, send_verification_email, send_reset_verification_email
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
    
    # Generate verification code
    verification_code = generate_verification_code()
    verification_expires = generate_verification_expiry()
    
    # Create new user (unverified)
    hashed_password = get_password_hash(password)
    user_data = {
        "email": email,
        "username": username,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow(),
        "is_active": True,
        "is_verified": False,
        "verification_code": verification_code,
        "verification_code_expires": verification_expires
    }
    
    result = database.users.insert_one(user_data)
    
    # Send verification email
    email_sent = await send_verification_email(email, username, verification_code)
    
    if email_sent:
        # Redirect to verification page
        response = RedirectResponse(url=f"/verify-email?email={email}", status_code=status.HTTP_302_FOUND)
        return response
    else:
        # If email fails, delete the user and show error
        database.users.delete_one({"_id": result.inserted_id})
        return templates.TemplateResponse(
            "auth/register.html", 
            {"request": request, "error": "Failed to send verification email. Please try again."}
        )

@auth.get("/verify-email", response_class=HTMLResponse)
async def verify_email_page(request: Request):
    email = request.query_params.get("email")
    if not email:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse("auth/verify_email.html", {
        "request": request,
        "email": email
    })

@auth.post("/verify-email", response_class=HTMLResponse)
async def verify_email(request: Request):
    form = await request.form()
    
    email = form.get("email")
    verification_code = form.get("verification_code")
    
    if not email or not verification_code:
        return templates.TemplateResponse("auth/verify_email.html", {
            "request": request,
            "email": email,
            "error": "Email and verification code are required"
        })
    
    database = db.get_database()
    user = database.users.find_one({"email": email})
    
    if not user:
        return templates.TemplateResponse("auth/verify_email.html", {
            "request": request,
            "email": email,
            "error": "User not found"
        })
    
    if user.get("is_verified", False):
        return RedirectResponse(url="/login", status_code=302)
    
    # Check verification code
    if (user.get("verification_code") != verification_code or 
        user.get("verification_code_expires") < datetime.utcnow()):
        return templates.TemplateResponse("auth/verify_email.html", {
            "request": request,
            "email": email,
            "error": "Invalid or expired verification code"
        })
    
    # Mark user as verified
    database.users.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "is_verified": True,
                "verification_code": None,
                "verification_code_expires": None
            }
        }
    )
    
    return RedirectResponse(url="/login?verified=true", status_code=302)

@auth.post("/resend-verification", response_class=HTMLResponse)
async def resend_verification(request: Request):
    form = await request.form()
    email = form.get("email")
    
    if not email:
        return templates.TemplateResponse("auth/verify_email.html", {
            "request": request,
            "email": email,
            "error": "Email is required"
        })
    
    database = db.get_database()
    user = database.users.find_one({"email": email})
    
    if not user:
        return templates.TemplateResponse("auth/verify_email.html", {
            "request": request,
            "email": email,
            "error": "User not found"
        })
    
    if user.get("is_verified", False):
        return RedirectResponse(url="/login", status_code=302)
    
    # Generate new verification code
    verification_code = generate_verification_code()
    verification_expires = generate_verification_expiry()
    
    # Update user with new code
    database.users.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "verification_code": verification_code,
                "verification_code_expires": verification_expires
            }
        }
    )
    
    # Send new verification email
    email_sent = await send_reset_verification_email(email, user["username"], verification_code)
    
    if email_sent:
        return templates.TemplateResponse("auth/verify_email.html", {
            "request": request,
            "email": email,
            "success": "New verification code sent to your email"
        })
    else:
        return templates.TemplateResponse("auth/verify_email.html", {
            "request": request,
            "email": email,
            "error": "Failed to send verification email. Please try again."
        })

@auth.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    verified = request.query_params.get("verified")
    return templates.TemplateResponse("auth/login.html", {
        "request": request,
        "verified": verified == "true"
    })

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
    
    # Check if user is verified
    if not user.get("is_verified", False):
        return templates.TemplateResponse(
            "auth/login.html", 
            {"request": request, "error": "Please verify your email before logging in"}
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