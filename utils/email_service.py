import os
import random
import string
from datetime import datetime, timedelta
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import Optional

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "your-email@gmail.com"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "your-app-password"),
    MAIL_FROM=os.getenv("MAIL_FROM", "your-email@gmail.com"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

fastmail = FastMail(conf)

def generate_verification_code() -> str:
    """Generate a 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=6))

def generate_verification_expiry() -> datetime:
    """Generate expiry time for verification code (10 minutes from now)"""
    return datetime.utcnow() + timedelta(minutes=10)

async def send_verification_email(email: str, username: str, verification_code: str) -> bool:
    """Send verification email with 6-digit code"""
    try:
        html_content = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #007bff;">HelloNotes - Email Verification</h2>
                <p>Hi {username},</p>
                <p>Thank you for registering with HelloNotes! To complete your registration, please use the verification code below:</p>
                
                <div style="background-color: #f8f9fa; border: 2px solid #007bff; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0;">
                    <h1 style="color: #007bff; font-size: 32px; letter-spacing: 8px; margin: 0;">{verification_code}</h1>
                </div>
                
                <p><strong>This code will expire in 10 minutes.</strong></p>
                
                <p>If you didn't create an account with HelloNotes, please ignore this email.</p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 12px;">
                    This is an automated email from HelloNotes. Please do not reply to this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        message = MessageSchema(
            subject="HelloNotes - Email Verification",
            recipients=[email],
            body=html_content,
            subtype="html"
        )
        
        await fastmail.send_message(message)
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        # Fallback: Print verification code to console for testing
        print(f"\n{'='*50}")
        print(f"📧 EMAIL VERIFICATION CODE (TESTING MODE)")
        print(f"{'='*50}")
        print(f"To: {email}")
        print(f"Username: {username}")
        print(f"Verification Code: {verification_code}")
        print(f"Expires: {datetime.utcnow() + timedelta(minutes=10)}")
        print(f"{'='*50}\n")
        return False

async def send_reset_verification_email(email: str, username: str, verification_code: str) -> bool:
    """Send a new verification code for unverified users"""
    try:
        html_content = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #007bff;">HelloNotes - New Verification Code</h2>
                <p>Hi {username},</p>
                <p>You requested a new verification code for your HelloNotes account. Please use the code below:</p>
                
                <div style="background-color: #f8f9fa; border: 2px solid #007bff; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0;">
                    <h1 style="color: #007bff; font-size: 32px; letter-spacing: 8px; margin: 0;">{verification_code}</h1>
                </div>
                
                <p><strong>This code will expire in 10 minutes.</strong></p>
                
                <p>If you didn't request this code, please ignore this email.</p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 12px;">
                    This is an automated email from HelloNotes. Please do not reply to this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        message = MessageSchema(
            subject="HelloNotes - New Verification Code",
            recipients=[email],
            body=html_content,
            subtype="html"
        )
        
        await fastmail.send_message(message)
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        # Fallback: Print verification code to console for testing
        print(f"\n{'='*50}")
        print(f"📧 NEW VERIFICATION CODE (TESTING MODE)")
        print(f"{'='*50}")
        print(f"To: {email}")
        print(f"Username: {username}")
        print(f"New Verification Code: {verification_code}")
        print(f"Expires: {datetime.utcnow() + timedelta(minutes=10)}")
        print(f"{'='*50}\n")
        return False 