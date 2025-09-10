import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
ENCRYPTION_ALGORITHM = os.getenv("ENCRYPTION_ALGORITHM")
CHARACTER_CODE = os.getenv("CHARACTER_CODE")
EXPIRATION_TIME = int(os.getenv("EXPIRATION_TIME"))
UPLOADS_PATH = os.getenv("UPLOADS_PATH")