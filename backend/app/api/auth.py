"""
Authentication API endpoints.

Handles user authentication, authorization, and token management
for the LegalTech MVP platform.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

router = APIRouter()
security = HTTPBearer()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserLogin(BaseModel):
    """User login request model."""
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """User registration request model."""
    email: EmailStr
    password: str
    full_name: str
    organization: Optional[str] = None


class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str
    expires_in: int


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.
    
    Generates a JWT token with user data and expiration time.
    Used for authenticating API requests.
    
    Args:
        data: User data to encode in token
        expires_delta: Custom expiration time (optional)
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash.
    
    Uses bcrypt to verify plain text password against stored hash.
    
    Args:
        plain_password: The plain text password
        hashed_password: The stored password hash
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash password using bcrypt.
    
    Creates secure password hash for storage.
    
    Args:
        password: Plain text password
        
    Returns:
        Bcrypt password hash
    """
    return pwd_context.hash(password)


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin) -> Token:
    """
    User login endpoint.
    
    Authenticates user credentials and returns JWT token.
    Currently uses demo credentials for MVP development.
    
    Args:
        user_data: User login credentials
        
    Returns:
        JWT token and metadata
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Demo authentication logic - replace with actual user database lookup
    demo_users = {
        "admin@legaltech.com": {
            "password_hash": get_password_hash("admin123"),
            "user_id": "1",
            "role": "admin",
            "full_name": "Admin User"
        },
        "lawyer@legaltech.com": {
            "password_hash": get_password_hash("lawyer123"),
            "user_id": "2", 
            "role": "lawyer",
            "full_name": "Legal Practitioner"
        }
    }
    
    user = demo_users.get(user_data.email)
    if not user or not verify_password(user_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user["user_id"],
            "email": user_data.email,
            "role": user["role"],
            "full_name": user["full_name"]
        },
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/register", response_model=Dict[str, str])
async def register(user_data: UserRegister) -> Dict[str, str]:
    """
    User registration endpoint.
    
    Registers new user account for the platform.
    Currently returns success message for MVP development.
    
    Args:
        user_data: User registration information
        
    Returns:
        Success message with user ID
    """
    # Demo registration logic - replace with actual user database creation
    hashed_password = get_password_hash(user_data.password)
    
    # In production, save to database:
    # - Check if email already exists
    # - Create user record with hashed password
    # - Send verification email
    # - Return user ID
    
    return {
        "message": "User registered successfully",
        "user_id": "demo_user_id",
        "email": user_data.email
    }


@router.get("/me")
async def get_current_user(token: str = Depends(security)) -> Dict[str, Any]:
    """
    Get current user information from token.
    
    Validates JWT token and returns user information.
    Used by frontend to get authenticated user details.
    
    Args:
        token: JWT token from Authorization header
        
    Returns:
        User information from token
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Extract token from Bearer format
        if hasattr(token, 'credentials'):
            token_str = token.credentials
        else:
            token_str = str(token)
            
        payload = jwt.decode(token_str, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "role": payload.get("role"),
            "full_name": payload.get("full_name"),
            "exp": payload.get("exp")
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )