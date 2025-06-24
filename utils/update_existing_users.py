#!/usr/bin/env python3
"""
Utility script to update existing users with email verification fields.
Run this once after implementing email verification to update existing users.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db import db

def update_existing_users():
    """Update existing users to have email verification fields"""
    load_dotenv()
    
    database = db.get_database()
    
    # Find all users that don't have is_verified field
    users_to_update = database.users.find({"is_verified": {"$exists": False}})
    
    update_count = 0
    for user in users_to_update:
        # Update user with verification fields
        result = database.users.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "is_verified": True,  # Mark existing users as verified
                    "verification_code": None,
                    "verification_code_expires": None
                }
            }
        )
        if result.modified_count > 0:
            update_count += 1
            print(f"Updated user: {user.get('email', 'Unknown')}")
    
    print(f"\nTotal users updated: {update_count}")
    print("Existing users have been marked as verified.")

if __name__ == "__main__":
    update_existing_users() 