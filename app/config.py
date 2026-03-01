import os 
from dotenv import load_dotenv

# Locate the .env file inside the 'app' directory relative to this file
base_dir = os.path.dirname(os.path.abspath(__file__))
# Load .env from app directory or project root (parent directory)
load_dotenv(os.path.join(base_dir, ".env"))
load_dotenv(os.path.join(base_dir, "..", ".env"))

# Security Configurations
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key") 
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

# Database Configurations
DATABASE_URL = os.getenv("DATABASE_URL")

# Validation to ensure critical variables are present
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set. Please set it in your .env file or environment.")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set.")
if not ALGORITHM:
    raise ValueError("ALGORITHM environment variable not set. Please set it in your .env file or environment.")