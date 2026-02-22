import bcrypt
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from .config import SECRET_KEY, ALGORITHM , ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import Depends ,HTTPException
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials

security = HTTPBearer()

# --- MONKEYPATCHES FOR BCRYPT COMPATIBILITY ---
# Fix for passlib looking for removed __about__ attribute
if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type('About', (object,), {'__version__': bcrypt.__version__})

_original_hashpw = bcrypt.hashpw

def _patched_hashpw(password, salt):
    if isinstance(password, str):
        password = password.encode("utf-8")
    if len(password) > 72:
        password = password[:72]
    return _original_hashpw(password, salt)

bcrypt.hashpw = _patched_hashpw

# --- PASSWORD HASHING ---
pwd_context = CryptContext(
    schemes = ["bcrypt"] , 
    deprecated = "auto"
)

def hash_pass(password : str ):
    """Hashes a plain text password."""
    return pwd_context.hash(password)

def verify_pass(plain_pass : str , hashed_pass : str):
    """Verifies a plain text password against a hash."""
    return pwd_context.verify(plain_pass , hashed_pass)

# --- JWT TOKEN LOGIC ---
def create_access_token(data : dict ):
    """Generates a JWT access token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)

def decode_access_token(token : str ):
    """Decodes and validates a JWT token."""
    try : 
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# --- DEPENDENCIES ---
def get_current_user(credentials : HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency used to protect routes. 
    Validates the Bearer token and returns the payload.
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None : 
        raise HTTPException(status_code=403 , detail="Invalid or expired token")
    return payload