import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'bookrec_secret_key_2024_likhitha')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/book_recommendation')
    
    # Admin credentials
    ADMIN_USERNAME = 'Likhitha N M'
    ADMIN_EMAIL = 'likhithanm2004@gmail.com'
    ADMIN_PASSWORD = '7019162414'
    
    # Session config
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    
    # Cookie security – prevents session from being dropped by browser on redirect
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_HTTPONLY = True
