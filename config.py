import secrets
import os

class Config:
    SECRET_KEY = secrets.token_hex(16)  # You can also use a hardcoded string
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Sam@2004'  # Use your MySQL password
    MYSQL_DB = 'hostel_management'
    MYSQL_CURSORCLASS = 'DictCursor'
