#!/usr/bin/env python3
"""
HelloNotes - Startup Script
A simple script to run the HelloNotes application
"""

import uvicorn
import os
from config.db import db

def main():
    """Main function to start the application"""
    print("🚀 Starting HelloNotes...")
    
    # Connect to database
    try:
        db.connect_to_database()
        print("✅ Database connected successfully")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    # Create uploads directory if it doesn't exist
    os.makedirs("static/uploads", exist_ok=True)
    print("✅ Uploads directory ready")
    
    # Start the server
    print("🌐 Starting web server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 