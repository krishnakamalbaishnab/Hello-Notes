import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb+srv://krishnakamalbaishnab:Databaseaccount%4002@cluster0.i7n38c5.mongodb.net")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "hellonotes")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # File upload
    UPLOAD_DIR: str = "static/uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

settings = Settings() 