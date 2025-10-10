"""
Authentication endpoints (simplified for demo)
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timedelta
import jwt
from core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class UserInfo(BaseModel):
    user_id: str
    username: str
    role: str
    permissions: list

# Mock user database (in production, use proper authentication)
MOCK_USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "permissions": ["read", "write", "admin"]
    },
    "analyst": {
        "password": "analyst123",
        "role": "analyst",
        "permissions": ["read", "write"]
    },
    "auditor": {
        "password": "auditor123",
        "role": "auditor",
        "permissions": ["read"]
    }
}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Authenticate user and return access token
    """
    try:
        logger.info(f"Login attempt for user: {request.username}")
        
        # Check if user exists
        if request.username not in MOCK_USERS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        user = MOCK_USERS[request.username]
        
        # Check password (in production, use proper password hashing)
        if user["password"] != request.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": request.username, "role": user["role"]},
            expires_delta=access_token_expires
        )
        
        logger.info(f"Successful login for user: {request.username}")
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.get("/me", response_model=UserInfo)
async def get_current_user(username: str = Depends(verify_token)):
    """
    Get current user information
    """
    try:
        if username not in MOCK_USERS:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user = MOCK_USERS[username]
        
        return UserInfo(
            user_id=username,
            username=username,
            role=user["role"],
            permissions=user["permissions"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )

@router.post("/logout")
async def logout(username: str = Depends(verify_token)):
    """
    Logout user (in production, implement token blacklisting)
    """
    try:
        logger.info(f"Logout for user: {username}")
        
        # In production, you would blacklist the token
        # For this demo, we just log the logout
        
        return {
            "message": "Successfully logged out",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )

@router.get("/health")
async def auth_health_check():
    """
    Health check for authentication service
    """
    return {
        "service": "Authentication",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
